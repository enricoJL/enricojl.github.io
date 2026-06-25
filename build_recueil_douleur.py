#!/usr/bin/env python3
"""Assemble the pain traversal arc into a print-ready PDF."""

import os
import re
import subprocess
import sys

POSTS_DIR  = os.path.join(os.path.dirname(__file__), "_posts")
OUTPUT_MD  = os.path.join(os.path.dirname(__file__), "recueil-douleur.md")
OUTPUT_PDF = os.path.join(os.path.dirname(__file__), "LEVESQUE_Enrico_la_traversee_de_la_douleur.pdf")

# Arc structure: (section title, [exact filenames])
ARC = [
    ("la descente", [
        "2026-05-29-gouffre.md",
        "2026-05-28-y.md",
        "2025-08-09-funambule.md",
        "2024-11-02-senliser.md",
        "2020-08-20-le-silence-des-pierres.md",
        "2026-06-23-tourbillon.md",
        "2025-08-16-insouciance.md",
    ]),
    ("le fond", [
        "2013-07-19-le-puits.md",
        "2019-03-03-la-mort-a-petit-feu.md",
        "2021-02-14-disparu.md",
        "2025-08-01-anonyme.md",
        "2025-08-10-tragedie.md",
        "2013-07-20-au-pied-dun-arbre.md",
        "2020-06-24-a-lagonie.md",
        "2024-12-15-sans-appui.md",
        "2025-06-10-degout.md",
        "2025-07-17-inassouvi.md",
        "2025-08-16-fracture.md",
        "2025-11-22-passager.md",
        "2025-03-27-dans-la-nuit.md",
    ]),
    ("le pivot", [
        "2024-12-15-dans-la-tempête.md",
        "2025-01-01-chardons.md",
        "2025-05-19-slap.md",
        "2023-03-15-blessure.md",
        "2025-08-30-assainir.md",
        "2026-02-28-fixation.md",
        "2021-01-26-le-colporteur.md",
        "2021-03-13-la-mort-mon-handicap.md",
    ]),
    ("la remontée", [
        "2024-03-24-debout.md",
        "2025-10-10-acceptance.md",
        "2026-02-07-guerison.md",
        "2026-06-17-desir-ardent.md",
        "2026-06-20-probleme.md",
        "2021-02-04-assis-par-terre.md",
        "2021-03-05-je-reviens-a-la-vie.md",
        "2023-06-04-coma.md",
        "2024-02-11-intention.md",
        "2025-03-18-chambranlant.md",
        "2025-03-29-instabilite.md",
        "2025-04-24-femmes.md",
    ]),
    ("de l'autre côté", [
        "2020-05-11-la-rose-et-le-jardinier.md",
        "2023-04-02-elixir.md",
        "2025-04-05-resurrection.md",
        "2025-06-10-fenetre-ouverte.md",
        "2026-06-16-offrande.md",
        "2026-06-20-dragon.md",
        "2020-05-11-serment.md",
        "2018-10-28-etrange.md",
        "2018-12-22-cycle-de-vie.md",
    ]),
]

LATEX_HEADER = r"""---
title: "la traversée de la douleur"
author: "Enrico Lévesque"
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
{\fontsize{30}{40}\selectfont\bfseries la traversée de la douleur}\\[1.4cm]
{\large\itshape Poèmes choisis — 1992–2026}\\[2.5cm]
{\large Enrico Lévesque}
\vfill
\end{titlepage}
\restoregeometry

\setcounter{tocdepth}{1}
\tableofcontents
\cleardoublepage

"""

EPIGRAPH = """```{=latex}
\\vspace*{3cm}
\\textit{entrer dans le gouffre, pour en ressortir de l'autre côté}
\\clearpage
```

"""


def parse_post(filepath):
    """Return (title, date, content) from a Jekyll post."""
    with open(filepath, encoding="utf-8") as fh:
        raw = fh.read()

    # Strip YAML frontmatter
    if raw.startswith("---"):
        parts = raw.split("---", 2)
        frontmatter = parts[1]
        content = parts[2].strip()
    else:
        frontmatter = ""
        content = raw.strip()

    title_match = re.search(r'^title:\s*["\']?(.+?)["\']?\s*$', frontmatter, re.MULTILINE)
    date_match  = re.search(r'^date:\s*["\']?(\d{4})["\']?', frontmatter, re.MULTILINE)

    title = title_match.group(1).strip() if title_match else os.path.basename(filepath)
    date  = date_match.group(1).strip() if date_match else ""

    return title, date, content


def assemble_markdown():
    lines = []
    lines.append("# la traversée de la douleur\n")
    lines.append("\n*Poèmes choisis — 1992–2026*\n")
    lines.append("\n**Enrico Lévesque**\n")
    lines.append("\n---\n\n")
    lines.append(EPIGRAPH)

    poem_count = 0
    for section_title, filenames in ARC:
        lines.append(f"\n## {section_title}\n")
        for fname in filenames:
            fpath = os.path.join(POSTS_DIR, fname)
            if not os.path.exists(fpath):
                print(f"AVERTISSEMENT : fichier introuvable : {fname}", file=sys.stderr)
                continue
            title, date, content = parse_post(fpath)
            lines.append(f"\n### {title}\n\n")
            lines.append(content)
            lines.append("\n")
            if date:
                lines.append(f"\n*{date}*\n")
            poem_count += 1

    lines.append(f"\n---\n\n*La traversée de la douleur — {poem_count} poèmes*\n")
    return "".join(lines), poem_count


def process_content(text):
    """Strip title block and shift headings for PDF rendering."""
    lines = text.splitlines(keepends=True)

    # Skip opening title block up to first ---
    i = 0
    while i < len(lines) and not lines[i].startswith("# "):
        i += 1
    i += 1  # skip # title

    while i < len(lines) and lines[i].strip() != "---":
        i += 1
    i += 1  # skip the ---

    rest = "".join(lines[i:])

    # Shift headings: ## Section → # (chapter), ### Poem → ## (section)
    rest = re.sub(r"^## ", "# ", rest, flags=re.MULTILINE)
    rest = re.sub(r"^### ", "## ", rest, flags=re.MULTILINE)

    # Each poem on a new page with top spacing
    rest = re.sub(r"^(## )", r"\\newpage\n\\vspace*{2cm}\n\n\1", rest, flags=re.MULTILINE)

    # Remove standalone year lines like *2013*
    rest = re.sub(r"^\*\d{4}\*\n?", "", rest, flags=re.MULTILINE)

    # Colophon on new page
    rest = re.sub(
        r"(\*La traversée de la douleur)",
        r"\\newpage\n\\vspace*{2cm}\n\n\1",
        rest,
    )

    return rest


def main():
    source_md, count = assemble_markdown()

    with open(OUTPUT_MD, "w", encoding="utf-8") as fh:
        fh.write(source_md)
    print(f"Recueil assemblé : {OUTPUT_MD} ({count} poèmes)")

    body = process_content(source_md)
    full_md = LATEX_HEADER + TITLE_PAGE + body

    tmp_md = OUTPUT_MD.replace(".md", "_processed.md")
    with open(tmp_md, "w", encoding="utf-8") as fh:
        fh.write(full_md)

    cmd = ["pandoc", tmp_md, "--pdf-engine=xelatex", "-o", OUTPUT_PDF]
    print("Génération du PDF…")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("Erreur pandoc :\n", result.stderr)
        sys.exit(result.returncode)
    print(f"PDF créé : {OUTPUT_PDF}")


if __name__ == "__main__":
    main()
