#!/usr/bin/env python3
"""Assemble the image arc into a print-ready PDF."""

import os
import re
import subprocess
import sys

POSTS_DIR  = os.path.join(os.path.dirname(__file__), "_posts")
OUTPUT_MD  = os.path.join(os.path.dirname(__file__), "recueil-image.md")
OUTPUT_PDF = os.path.join(os.path.dirname(__file__), "LEVESQUE_Enrico_entre_l'image_et_la_mer.pdf")

# Arc structure: (section title, [exact filenames])
ARC = [
    ("Phase I — Mirage", [
        "1992-05-01-premier-baiser.md",
        "2006-10-25-la-docilite-du-reve.md",
        "2020-05-10-vertige.md",
        "2013-07-20-a-lenvers-du-decor.md",
        "2013-07-20-la-montagne-den-face.md",
        "2013-07-20-en-chute-libre.md",
        "2013-07-20-gravure.md",
        "2013-07-20-si-fragile.md",
        "2013-07-20-elle.md",
    ]),
    ("Phase II — Prison", [
        "2018-02-27-ici-et-maintenant.md",
        "2019-05-01-temple-fondements-babeurre.md",
        "2020-05-11-passe-moi-un-film.md",
        "2020-12-23-belles-choses-a-dire.md",
        "2026-04-08-surprise.md",
        "2026-04-20-mascarade.md",
        "2023-07-04-inquietude.md",
        "2026-06-07-le-coeur-a-ses-raisons.md",
        "2021-04-02-le-choc-des-titans.md",
        "2026-06-12-dialogue.md",
        "2024-06-09-pointderencontre.md",
        "2021-02-27-prison.md",
        "2021-01-24-bang.md",
    ]),
    ("Phase III — Transparence", [
        "2023-07-14-demolition.md",
        "2023-01-02-au-travers-du-dernier-mur.md",
        "2021-03-11-dun-univers-a-lautre.md",
        "2020-06-12-inextricable-beaute.md",
        "2023-01-13-beaute.md",
        "2023-02-21-épitaphe.md",
        "2024-06-04-entre-limage-et-la-mer.md",
        "2024-12-08-cristal.md",
        "2013-08-18-ce-qui-nous-arrive.md",
        "2024-08-09-perception.md",
        "2025-03-25-bulles-fragiles.md",
        "2025-03-26-imagination.md",
        "2025-03-26-restitution.md",
        "2025-03-26-sans-image.md",
        "2025-08-13-be-water.md",
        "2026-01-18-sans-frontiere.md",
        "2023-01-03-plongeon-dans-le-ciel.md",
        "2013-07-20-je-marche-avec-lui.md",
        "2025-08-27-semblable.md",
        "2026-03-04-plongee.md",
        "2026-06-13-la-mer.md",
        "2026-05-30-abyssal.md",
    ]),
]

LATEX_HEADER = r"""---
title: "entre l'image et la mer"
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
{\fontsize{30}{40}\selectfont\bfseries entre l'image et la mer}\\[1.4cm]
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
\\begin{quote}
\\textit{Je marche à côté d'une joie} \\\\
\\textit{D'une joie qui n'est pas à moi} \\\\
--- Hector de Saint-Denys Garneau, \\textit{Accompagnement}
\\end{quote}
\\vspace*{1.5cm}
\\begin{quote}
\\textit{Toute vie véritable est rencontre. La relation au Tu est immédiate. Entre Je et Tu ne s'intercale aucun but, aucun savoir et aucune imagination.} \\\\
--- Martin Buber, \\textit{Je et Tu}
\\end{quote}
\\clearpage
```

"""


def parse_post(filepath):
    """Return (title, date, content) from a Jekyll post."""
    with open(filepath, encoding="utf-8") as fh:
        raw = fh.read()

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
    lines.append("# entre l'image et la mer\n")
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

    lines.append(f"\n---\n\n*Entre l'image et la mer — {poem_count} poèmes*\n")
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
        r"(\*Entre l'image et la mer)",
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
