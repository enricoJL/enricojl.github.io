#!/usr/bin/env python3
"""Assemble poetry collection into a print-ready PDF."""

import os
import re
import subprocess
import sys

SOURCE_MD  = os.path.join(os.path.dirname(__file__), "recueil-de-mirage-a-abysmal.md")
OUTPUT_MD  = os.path.join(os.path.dirname(__file__), "_recueil.md")
OUTPUT_PDF = os.path.join(os.path.dirname(__file__), "entre l'image et la mer.pdf")

LATEX_HEADER = r"""---
title: "entre l'image et la mer"
author: "Enrico J. Lévesque"
date: ""
lang: fr
documentclass: book
classoption:
  - 12pt
  - openright
  - twoside
geometry: "inner=4.5cm, outer=3.5cm, top=4cm, bottom=4cm"
numbersections: false
colorlinks: true
linkcolor: black
urlcolor: black
header-includes:
  - \usepackage{setspace}
  - \setstretch{1.5}
  - \usepackage{microtype}
  - \usepackage{graphicx}
  - \usepackage{ragged2e}
  - \setlength{\parindent}{0pt}
  - \setlength{\parskip}{1\baselineskip}
  - \widowpenalty=10000
  - \clubpenalty=10000
  - \displaywidowpenalty=10000
---

"""

TITLE_PAGE = r"""
\newgeometry{margin=3cm}
\begin{titlepage}
\centering
\vspace*{4cm}
{\fontsize{30}{40}\selectfont\bfseries entre l'image et la mer}\\[1.4cm]
{\large\itshape Poèmes choisis — 1992–2026}\\[2.5cm]
{\large Enrico J. Lévesque}
\vfill
\end{titlepage}
\restoregeometry

\setcounter{tocdepth}{1}
\tableofcontents
\cleardoublepage

"""


def process_content(text):
    """Strip title block, extract epigraph, shift headings."""
    lines = text.splitlines(keepends=True)

    # Skip the opening title block: h1, subtitle, author, first ---
    i = 0
    while i < len(lines) and not lines[i].startswith("# "):
        i += 1
    i += 1  # skip # Mirage

    # Skip everything up to and including the first ---
    while i < len(lines) and lines[i].strip() != "---":
        i += 1
    i += 1  # skip the ---

    rest = "".join(lines[i:])

    # Shift heading levels: ## Phase → # (chapter), ### Poem → ## (section)
    # Order matters: shift phases first, then poems
    rest = re.sub(r"^## ", "# ", rest, flags=re.MULTILINE)
    rest = re.sub(r"^### ", "## ", rest, flags=re.MULTILINE)

    # Strip leading numbering from poem titles: ## 1. Titre → ## Titre
    # (Désactivé — les numéros ont été retirés du recueil source)
    # rest = re.sub(r"^(## )\d+\.\s+", r"\1", rest, flags=re.MULTILINE)

    # Each poem starts on a new page with extra top space
    rest = re.sub(r"^(## )", r"\\newpage\n\\vspace*{2cm}\n\n\1", rest, flags=re.MULTILINE)

    # Remove standalone date/year lines like *1992* or *25 mars 2025*
    rest = re.sub(r"^\*(?:\d{1,2}\s+\w+\s+)?\d{4}\*\n?", "", rest, flags=re.MULTILINE)

    # Remove horizontal rules (désactivé — déjà retirées du recueil source)
    # rest = re.sub(r"^---\n?", "", rest, flags=re.MULTILINE)

    # Colophon on a new page with top spacing
    rest = re.sub(r"(\*Mirage — \d+ poèmes)", r"\\newpage\n\\vspace*{2cm}\n\n\1", rest)

    return rest


def main():
    with open(SOURCE_MD, encoding="utf-8") as fh:
        raw = fh.read()

    body = process_content(raw)
    full_md = LATEX_HEADER + TITLE_PAGE + body

    with open(OUTPUT_MD, "w", encoding="utf-8") as fh:
        fh.write(full_md)
    print(f"Assembled markdown written to {OUTPUT_MD}")

    texlive_bin = "/usr/local/texlive/2026/bin/universal-darwin"
    env = os.environ.copy()
    env["PATH"] = texlive_bin + ":" + env.get("PATH", "")

    cmd = ["pandoc", OUTPUT_MD, "--pdf-engine=xelatex", "-o", OUTPUT_PDF]
    print("Running pandoc…")
    result = subprocess.run(cmd, env=env, capture_output=True, text=True)
    if result.returncode != 0:
        print("pandoc stderr:\n", result.stderr)
        sys.exit(result.returncode)
    print(f"PDF created: {OUTPUT_PDF}")


if __name__ == "__main__":
    main()
