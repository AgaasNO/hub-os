#!/usr/bin/env python3
"""SessionStart hook: the hub's minimum instrument (FRAMEWORK.md Section 4.8).

WHY THIS IS A HOOK AND NOT A LINE IN CLAUDE.md
----------------------------------------------
Session-end step 1 (reconcile the proposal queue) is declared in CLAUDE.md. In the
hub this framework was extracted from, that declaration was read every session and
skipped 80 times across eleven weeks. It was the expensive step in a list of cheap
ones, and nothing checked. A skipped instruction is not fixed by another instruction
(R-009). So the check runs here, whether or not the coordinator remembers.

Do not "fix" a finding from this hook by adding a sentence to CLAUDE.md.

CONTRACT
--------
- Read-only. Opens nothing for writing, runs no mutating command.
- Prints `{}` when there is nothing to say. Silence has to mean "clean"; a hook
  that talks every session turns into wallpaper within a week.
- Otherwise prints SessionStart JSON with a short `additionalContext`.
- Never exits non-zero. A broken instrument must go quiet and get fixed, not
  block the session.
- Every finding names the files it came from, and the hook refuses to call a
  reading clean when it can't justify it (R-010).

WHAT FIRES (R-011)
------------------
- SELF-FEEDING: most open rows cite another row's id, so the queue is generating
  its own follow-up work.
- DEFERRAL: high-priority open rows are older on average than the rest, so the
  queue is doing the easy rows first.
- UNRECONCILED?: the hub has been committing but nothing was resolved in the window.
  Either session end isn't reconciling, or resolutions are recorded somewhere this
  hook doesn't read.

WHAT DELIBERATELY DOES NOT FIRE
-------------------------------
Arrivals outnumbering resolutions. The source fleet's first instrument fired on
that and was wrong: in a research hub, filing a row *is* the output, so the rule
would have fired on the day that hub closed its most valuable row. The metrics
above don't depend on why a row was filed.

SCOPE
-----
Backlog shape (self-feeding, deferral) is read from the queue of record
(QUEUE_FILE) only. Resolutions are counted from every *.yaml under QUEUE_DIR, so
rows archived to a second file still count as served.
"""
from __future__ import annotations

import datetime as dt
import json
import os
import re
import subprocess
import sys
from pathlib import Path

HUB = Path(os.environ.get("CLAUDE_PROJECT_DIR") or Path(__file__).resolve().parents[2])
QUEUE_DIR = HUB / "kanban" / "proposals"
QUEUE_FILE = QUEUE_DIR / "pending.yaml"

WINDOW_DAYS = 7
SELF_FEED_PCT = 60      # share of open rows citing another row
SELF_FEED_FLOOR = 20    # too small a queue to mean anything
INVERSION_DAYS = 2.0    # high-priority rows older than the rest by this many days
INVERSION_FLOOR = 5     # too few high-priority rows to mean anything
COMMITS_FLOOR = 10      # commits in the window with zero resolutions = suspect

OPEN = {"open", "pending", "approved", "in_progress"}
HIGH = {"high", "critical", "urgent"}
CREATED = ("created_date", "date")
RESOLVED = ("resolved_date", "closed_date")

try:
    import yaml
except ImportError:
    yaml = None


def strings(node):
    """Every string value anywhere in a nested row (keys and numbers excluded)."""
    if isinstance(node, str):
        yield node
    elif isinstance(node, dict):
        for v in node.values():
            yield from strings(v)
    elif isinstance(node, (list, tuple)):
        for v in node:
            yield from strings(v)


def load_rows(path: Path) -> list[dict]:
    """Rows as dicts, each with a `_body` string used for citation matching.

    There is deliberately no regex fallback for a missing PyYAML. One was tried; on
    a real queue it read 57% where the true figure was 60%, turning a real finding
    into silence. That is the reassuring-direction failure R-010 exists to prevent."""
    doc = yaml.safe_load(path.read_text(encoding="utf-8", errors="replace"))
    if isinstance(doc, dict):
        doc = next((v for v in doc.values() if isinstance(v, list)), [])
    rows = [r for r in (doc or []) if isinstance(r, dict) and r.get("id") is not None]
    for r in rows:
        r["id"] = str(r["id"])
        r["_body"] = " ".join(strings({k: v for k, v in r.items() if k != "id"}))
    return rows


def as_date(row: dict, fields: tuple[str, ...]) -> dt.date | None:
    for f in fields:
        v = row.get(f)
        if isinstance(v, dt.date):
            return v
        try:
            return dt.date.fromisoformat(str(v)[:10])
        except ValueError:
            continue
    return None


def commits_in_window() -> int | None:
    """Commits touching this hub's own directory. Path-limited on purpose: a hub
    that lives inside a larger repo must not count its neighbours' commits."""
    try:
        out = subprocess.run(
            ["git", "-C", str(HUB), "rev-list", "--count", f"--since={WINDOW_DAYS}.days", "HEAD", "--", "."],
            capture_output=True, text=True, timeout=10,
        )
        return int(out.stdout.strip()) if out.returncode == 0 else None
    except (OSError, ValueError, subprocess.SubprocessError):
        return None


def findings() -> list[str]:
    rel = lambda p: p.relative_to(HUB).as_posix()  # noqa: E731
    if yaml is None:
        return ["PyYAML is not installed, so this hub is unmeasured. Run `pip install pyyaml`."]
    if not QUEUE_FILE.is_file():
        return [f"No queue at {rel(QUEUE_FILE)}. This hook can't see this hub's state. "
                "Point QUEUE_FILE at it."]

    queue = load_rows(QUEUE_FILE)
    all_files = sorted(QUEUE_DIR.rglob("*.yaml"))
    served_rows = [r for f in all_files for r in (queue if f == QUEUE_FILE else load_rows(f))]
    today = dt.date.today()
    since = today - dt.timedelta(days=WINDOW_DAYS)

    open_rows = [r for r in queue if str(r.get("status", "open")).lower() in OPEN]
    ids = {r["id"] for r in queue}
    out = []

    if len(open_rows) >= SELF_FEED_FLOOR:
        citing = sum(
            1 for r in open_rows
            if any(re.search(rf"(?<![\w-]){re.escape(i)}(?![\w-])", r["_body"]) for i in ids - {r["id"]})
        )
        pct = round(100 * citing / len(open_rows))
        if pct >= SELF_FEED_PCT:
            out.append(f"SELF-FEEDING: {pct}% of {len(open_rows)} open rows cite another row. "
                       "The queue is generating its own successor work. Triage against current "
                       "priorities before adding rows.")

    high, rest = [], []
    for r in open_rows:
        if (d := as_date(r, CREATED)) is not None:
            (high if str(r.get("priority", "")).lower() in HIGH else rest).append((today - d).days)
    if len(high) >= INVERSION_FLOOR and rest:
        gap = round(sum(high) / len(high) - sum(rest) / len(rest), 1)
        if gap >= INVERSION_DAYS:
            out.append(f"DEFERRAL: high-priority open rows are {gap} days older on average than the "
                       f"rest (n={len(high)}). The queue is doing the easy rows first.")

    served = sum(1 for r in served_rows if (as_date(r, RESOLVED) or dt.date.min) >= since)
    commits = commits_in_window()
    if commits is not None and commits >= COMMITS_FLOOR and served == 0 and open_rows:
        out.append(f"UNRECONCILED?: {commits} commits in {WINDOW_DAYS} days but 0 rows resolved. "
                   "Either session end isn't reconciling the queue, or resolutions are recorded "
                   "somewhere this hook doesn't read.")

    if out:
        out.append(f"(backlog from {rel(QUEUE_FILE)}; resolutions from "
                   f"{len(all_files)} file(s) under {rel(QUEUE_DIR)}/)")
    return out


def main() -> None:
    try:
        lines = findings()
    except Exception as exc:  # the instrument must never block a session
        first = (str(exc).strip().splitlines() or [""])[0]
        lines = [f"session-start hook failed ({type(exc).__name__}: {first}). It needs fixing; "
                 "until then this hub is unmeasured."]
    if not lines:
        print("{}")
        return
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "SessionStart",
        "additionalContext": "HUB INSTRUMENT (read-only):\n  " + "\n  ".join(lines),
    }}))


if __name__ == "__main__":
    main()
    sys.exit(0)
