"""One-shot FRAMEWORK.md -> FRAMEWORK.tex converter for hub-os.

Compile target: XeLaTeX (handles Unicode box-drawing chars natively via fontspec).
In Overleaf: Menu -> Settings -> Compiler: XeLaTeX, then Recompile twice for TOC.

This converter is scoped to the patterns FRAMEWORK.md actually uses:
  - ATX headings #, ##, ###, ####
  - Bold **x**, italic *x*, inline code `x`
  - Bullet lists with 2-space indent nesting
  - Numbered lists (1., 2., ...)
  - GFM tables (| ... | ... |)
  - Fenced code blocks (```lang ... ```)
  - Horizontal rules (--- on own line)
  - No hyperlinks, no images (verified via grep)

Not handled (not needed here): footnotes, HTML passthrough, reference links,
strikethrough, task lists.
"""

from __future__ import annotations

import re
from pathlib import Path

SRC = Path(r"FRAMEWORK.md")
DST = Path(r"FRAMEWORK.tex")


# ---------------------------------------------------------------------------
# Inline text processing: bold / italic / code / escape LaTeX specials
# ---------------------------------------------------------------------------

def escape_code_inner(s: str) -> str:
    """Escape content going inside \\texttt{...}."""
    s = s.replace("\\", r"\textbackslash{}")
    s = s.replace("{", r"\{")
    s = s.replace("}", r"\}")
    s = s.replace("&", r"\&")
    s = s.replace("%", r"\%")
    s = s.replace("$", r"\$")
    s = s.replace("#", r"\#")
    s = s.replace("_", r"\_")
    s = s.replace("~", r"\textasciitilde{}")
    s = s.replace("^", r"\textasciicircum{}")
    s = s.replace("<", r"\textless{}")
    s = s.replace(">", r"\textgreater{}")
    s = s.replace("|", r"\textbar{}")
    return s


def escape_prose(s: str) -> str:
    """Escape LaTeX specials in plain prose text (not bold/italic/code)."""
    s = s.replace("\\", r"\textbackslash{}")
    s = s.replace("{", r"\{")
    s = s.replace("}", r"\}")
    s = s.replace("&", r"\&")
    s = s.replace("%", r"\%")
    s = s.replace("$", r"\$")
    s = s.replace("#", r"\#")
    s = s.replace("_", r"\_")
    s = s.replace("~", r"\textasciitilde{}")
    s = s.replace("^", r"\textasciicircum{}")
    return s


PH = "\x00PH{}\x00"


def process_inline(text: str) -> str:
    """Convert markdown inline syntax to LaTeX; escape remaining specials."""
    placeholders: list[str] = []

    def store(s: str) -> str:
        placeholders.append(s)
        return PH.format(len(placeholders) - 1)

    # 1) Inline code: `x`  (contents are verbatim; escape inside \texttt{})
    def code_sub(m: re.Match) -> str:
        return store(r"\texttt{" + escape_code_inner(m.group(1)) + "}")

    text = re.sub(r"`([^`]+)`", code_sub, text)

    # 2) Bold: **x**
    def bold_sub(m: re.Match) -> str:
        return store(r"\textbf{" + escape_prose(m.group(1)) + "}")

    text = re.sub(r"\*\*([^*]+)\*\*", bold_sub, text)

    # 3) Italic: *x*  (asterisk-only, underscore-italic is unsafe for identifiers)
    def italic_sub(m: re.Match) -> str:
        return store(r"\emph{" + escape_prose(m.group(1)) + "}")

    text = re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", italic_sub, text)

    # 4) Escape any remaining prose specials
    text = escape_prose(text)

    # 5) Restore placeholders. Loop until stable: a bold replacement may contain
    #    an inline-code placeholder stored earlier, which only surfaces after
    #    the outer placeholder is restored.
    def restore(m: re.Match) -> str:
        return placeholders[int(m.group(1))]

    while "\x00PH" in text:
        text = re.sub(r"\x00PH(\d+)\x00", restore, text)
    return text


# ---------------------------------------------------------------------------
# Block-level processing
# ---------------------------------------------------------------------------

TABLE_ROW = re.compile(r"^\s*\|(.*)\|\s*$")
TABLE_SEP = re.compile(r"^\s*\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)+\|?\s*$")
HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
BULLET = re.compile(r"^(\s*)[-*]\s+(.*)$")
NUMBERED = re.compile(r"^(\s*)(\d+)\.\s+(.*)$")
FENCE = re.compile(r"^\s*```\s*([A-Za-z0-9_+-]*)\s*$")
HR = re.compile(r"^\s*---+\s*$")


def parse_table_row(line: str) -> list[str]:
    """Split a '| a | b | c |' row into ['a', 'b', 'c']."""
    body = line.strip()
    if body.startswith("|"):
        body = body[1:]
    if body.endswith("|"):
        body = body[:-1]
    return [cell.strip() for cell in body.split("|")]


def emit_table(header: list[str], rows: list[list[str]]) -> str:
    """Render a markdown table as a tabularx with L columns (raggedright X)."""
    n = len(header)
    # Normalize short rows (pad) and long rows (truncate)
    norm_rows = []
    for row in rows:
        if len(row) < n:
            row = row + [""] * (n - len(row))
        elif len(row) > n:
            row = row[:n]
        norm_rows.append(row)

    col_spec = " ".join(["L"] * n)
    out = [r"\begin{tabularx}{\linewidth}{" + col_spec + "}", r"\toprule"]
    head_cells = [r"\textbf{" + process_inline(c) + "}" for c in header]
    out.append(" & ".join(head_cells) + r" \\")
    out.append(r"\midrule")
    for row in norm_rows:
        cells = [process_inline(c) for c in row]
        out.append(" & ".join(cells) + r" \\")
    out.append(r"\bottomrule")
    out.append(r"\end{tabularx}")
    return "\n".join(out)


def pick_listings_lang(lang: str) -> str:
    lang = (lang or "").lower()
    if lang in ("yaml", "yml"):
        return "[language=YAMLish]"
    if lang in ("bash", "sh", "shell"):
        return "[language=bash]"
    # Everything else (markdown, plaintext, ascii art) -> no highlighting
    return ""


def emit_code_block(lang: str, body_lines: list[str]) -> str:
    opt = pick_listings_lang(lang)
    content = "\n".join(body_lines)
    # Safety: if the content happens to contain \end{lstlisting} (it won't in
    # this doc, but guard anyway), switch to a rarer delimiter.
    delim = "lstlisting"
    return f"\\begin{{{delim}}}{opt}\n{content}\n\\end{{{delim}}}"


# ---------------------------------------------------------------------------
# Main convert loop
# ---------------------------------------------------------------------------

def convert(md: str) -> str:
    lines = md.split("\n")
    out: list[str] = []

    i = 0
    n = len(lines)

    # State for open lists: stack of ("itemize" | "enumerate", indent_level)
    list_stack: list[tuple[str, int]] = []

    def close_lists_to(target_depth: int) -> None:
        """Close open list environments until stack depth <= target_depth."""
        while len(list_stack) > target_depth:
            kind, _ = list_stack.pop()
            out.append(r"\end{" + kind + "}")

    def close_all_lists() -> None:
        close_lists_to(0)

    # First heading (#) becomes the document title handled in main(); skip here.
    first_h1_consumed = False

    while i < n:
        line = lines[i]

        # --- Fenced code block ---
        m = FENCE.match(line)
        if m:
            close_all_lists()
            lang = m.group(1)
            body: list[str] = []
            i += 1
            while i < n and not FENCE.match(lines[i]):
                body.append(lines[i])
                i += 1
            # consume closing fence
            if i < n:
                i += 1
            out.append(emit_code_block(lang, body))
            out.append("")
            continue

        # --- Table (header row + separator row + body) ---
        if TABLE_ROW.match(line) and i + 1 < n and TABLE_SEP.match(lines[i + 1]):
            close_all_lists()
            header = parse_table_row(line)
            i += 2  # skip header + separator
            rows: list[list[str]] = []
            while i < n and TABLE_ROW.match(lines[i]):
                rows.append(parse_table_row(lines[i]))
                i += 1
            out.append(emit_table(header, rows))
            out.append("")
            continue

        # --- Heading ---
        m = HEADING.match(line)
        if m:
            close_all_lists()
            level = len(m.group(1))
            title_md = m.group(2).rstrip()
            # Strip leading section numbers ("3.", "3.1", "4.2.1 ") — LaTeX auto-numbers.
            title_md = re.sub(r"^\d+(\.\d+)*\.?\s+", "", title_md)

            # Skip the hand-written "Table of Contents" section; we use \tableofcontents.
            if level == 2 and title_md.strip().lower() == "table of contents":
                i += 1
                # Skip the TOC body until the next heading or HR
                while i < n:
                    if HEADING.match(lines[i]):
                        break
                    if HR.match(lines[i]) and not list_stack:
                        i += 1
                        break
                    i += 1
                continue

            title = process_inline(title_md)
            if level == 1:
                if not first_h1_consumed:
                    first_h1_consumed = True
                    # Handled by \maketitle; skip
                    i += 1
                    continue
                out.append(r"\section{" + title + "}")
            elif level == 2:
                out.append(r"\section{" + title + "}")
            elif level == 3:
                out.append(r"\subsection{" + title + "}")
            elif level == 4:
                out.append(r"\subsubsection{" + title + "}")
            else:
                out.append(r"\paragraph{" + title + "}")
            out.append("")
            i += 1
            continue

        # --- Horizontal rule ---
        if HR.match(line) and not list_stack:
            out.append(r"\medskip\noindent\rule{\linewidth}{0.3pt}\medskip")
            out.append("")
            i += 1
            continue

        # --- Bullet list ---
        m = BULLET.match(line)
        if m:
            indent = len(m.group(1))
            depth = indent // 2 + 1  # 0 -> 1, 2 -> 2, 4 -> 3
            content = m.group(2)

            # Close deeper lists than this level
            while list_stack and len(list_stack) > depth:
                kind, _ = list_stack.pop()
                out.append(r"\end{" + kind + "}")

            # If no list at this level, or mismatched type, open itemize
            if not list_stack or len(list_stack) < depth:
                out.append(r"\begin{itemize}")
                list_stack.append(("itemize", depth))
            elif list_stack[-1][0] != "itemize":
                kind, _ = list_stack.pop()
                out.append(r"\end{" + kind + "}")
                out.append(r"\begin{itemize}")
                list_stack.append(("itemize", depth))

            out.append(r"  \item " + process_inline(content))
            i += 1
            continue

        # --- Numbered list ---
        m = NUMBERED.match(line)
        if m:
            indent = len(m.group(1))
            depth = indent // 2 + 1
            content = m.group(3)

            while list_stack and len(list_stack) > depth:
                kind, _ = list_stack.pop()
                out.append(r"\end{" + kind + "}")

            if not list_stack or len(list_stack) < depth:
                out.append(r"\begin{enumerate}")
                list_stack.append(("enumerate", depth))
            elif list_stack[-1][0] != "enumerate":
                kind, _ = list_stack.pop()
                out.append(r"\end{" + kind + "}")
                out.append(r"\begin{enumerate}")
                list_stack.append(("enumerate", depth))

            out.append(r"  \item " + process_inline(content))
            i += 1
            continue

        # --- Blank line: close lists, paragraph break ---
        if line.strip() == "":
            close_all_lists()
            out.append("")
            i += 1
            continue

        # --- Paragraph text (possibly a continuation of a list item) ---
        # Close lists first if we're not indented into one
        close_all_lists()
        out.append(process_inline(line))
        i += 1

    close_all_lists()
    return "\n".join(out)


# ---------------------------------------------------------------------------
# Document preamble and driver
# ---------------------------------------------------------------------------

PREAMBLE = r"""% !TEX program = xelatex
% hub-os FRAMEWORK - auto-generated from FRAMEWORK.md
% Compiler: XeLaTeX (required for Unicode box-drawing glyphs in 3.3 Visual)
% In Overleaf: Menu -> Settings -> Compiler: XeLaTeX. Recompile twice for TOC.

\documentclass[11pt,a4paper]{article}

% --- XeLaTeX fonts & Unicode ---
\usepackage{fontspec}
\setmainfont{Latin Modern Roman}
\setsansfont{Latin Modern Sans}
\setmonofont{DejaVu Sans Mono}[Scale=0.92]
\usepackage{microtype}

% --- Layout ---
\usepackage[a4paper,margin=2.3cm,headheight=14pt]{geometry}
\usepackage{parskip}
\usepackage{setspace}
\setstretch{1.06}

% --- Typography ---
\usepackage{titlesec}
\titleformat{\section}{\Large\bfseries\sffamily}{\thesection}{0.7em}{}
\titleformat{\subsection}{\large\bfseries\sffamily}{\thesubsection}{0.6em}{}
\titleformat{\subsubsection}{\normalsize\bfseries\sffamily}{\thesubsubsection}{0.5em}{}
\titlespacing*{\section}{0pt}{1.6em}{0.6em}
\titlespacing*{\subsection}{0pt}{1.2em}{0.4em}
\titlespacing*{\subsubsection}{0pt}{0.9em}{0.3em}

% --- Lists ---
\usepackage{enumitem}
\setlist[itemize]{leftmargin=1.3em, itemsep=2pt, topsep=3pt}
\setlist[enumerate]{leftmargin=1.7em, itemsep=2pt, topsep=3pt}

% --- Tables ---
\usepackage{tabularx}
\usepackage{booktabs}
\usepackage{array}
\usepackage{ragged2e}
\newcolumntype{L}{>{\RaggedRight\arraybackslash}X}

% --- Code ---
\usepackage{xcolor}
\definecolor{codebg}{RGB}{246,247,249}
\definecolor{coderule}{RGB}{220,222,228}
\definecolor{codekw}{RGB}{106,27,154}
\definecolor{codestr}{RGB}{27,94,32}
\definecolor{codecom}{RGB}{120,120,120}

\usepackage{listings}
\lstdefinestyle{plain}{
  basicstyle=\ttfamily\small,
  backgroundcolor=\color{codebg},
  frame=single,
  rulecolor=\color{coderule},
  framesep=6pt,
  xleftmargin=8pt,
  xrightmargin=8pt,
  breaklines=true,
  columns=fullflexible,
  keepspaces=true,
  showstringspaces=false,
  upquote=true,
  extendedchars=true,
  inputencoding=utf8
}
\lstdefinelanguage{YAMLish}{
  keywords={type,kill_by,domain,task_shape,artifact,confidence,evidence_log,date,source,event,status,id,incident,rule,why,layer,source_hub,enforcement},
  keywordstyle=\color{codekw}\bfseries,
  sensitive=true,
  comment=[l]{\#},
  commentstyle=\color{codecom}\itshape,
  morestring=[b]',
  stringstyle=\color{codestr},
}
\lstset{style=plain}

% --- Headers & footers ---
\usepackage{fancyhdr}
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\small\sffamily hub-os}
\fancyhead[R]{\small\sffamily\leftmark}
\fancyfoot[C]{\small\thepage}
\renewcommand{\headrulewidth}{0.3pt}

% --- Hyperlinks & TOC ---
\usepackage{hyperref}
\hypersetup{
  colorlinks=true,
  linkcolor=black,
  urlcolor=blue!60!black,
  pdftitle={hub-os Framework for Cognitive-Operational Hubs},
  pdfauthor={Gabriel Lindberg},
  bookmarksnumbered=true
}

\title{\sffamily\textbf{\Huge hub-os} \\[0.4em]
  \Large Framework for Cognitive-Operational Hubs}
\author{Gabriel Lindberg}
\date{Source: \texttt{FRAMEWORK.md} \ \textbullet\ \ Generated \today}

\begin{document}
\maketitle
\thispagestyle{empty}

\vspace{1.5em}
{\small\tableofcontents}
\newpage
"""

POSTAMBLE = "\n\\end{document}\n"


def main() -> None:
    md = SRC.read_text(encoding="utf-8")
    body = convert(md)
    tex = PREAMBLE + "\n" + body + POSTAMBLE
    DST.write_text(tex, encoding="utf-8")
    print(f"Wrote {DST} ({len(tex):,} chars)")


if __name__ == "__main__":
    main()
