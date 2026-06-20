#!/usr/bin/env python3
"""Assemble the accompaniment arc into a print-ready PDF."""

import os
import re
import subprocess
import sys

POSTS_DIR  = os.path.join(os.path.dirname(__file__), "_posts")
OUTPUT_MD  = os.path.join(os.path.dirname(__file__), "recueil-accompagnement.md")
OUTPUT_PDF = os.path.join(os.path.dirname(__file__), "LEVESQUE_Enrico_le_chemin_de_la_presence.pdf")

# Arc structure: (section title, [exact filenames])
ARC = [
    ("I. L'Appel et l'Engagement", [
        "2013-07-19-dans-une-falaise.md",
        "2020-05-11-je-te-suivrai.md",
        "2024-12-15-dans-la-tempête.md",
        "2025-04-19-cahier.md",
    ]),
    ("II. La Descente dans la Nuit", [
        "2023-06-04-coma.md",
        "2024-11-02-senliser.md",
        "2025-08-16-fracture.md",
        "2013-07-20-si-fragile.md",
        "2020-05-11-accroche-toi.md",
        "2025-03-25-solitudes.md",
        "2025-04-12-accompagnement.md",
        "2025-04-12-bienveillance.md",
        "2025-04-24-femmes.md",
        "2025-06-10-fenetre-ouverte.md",
        "2004-05-25-lintimite.md",
        "2025-03-22-givrés.md",
    ]),
    ("III. La Main qui Relève", [
        "2024-12-15-sans-appui.md",
        "2020-05-11-la-rose-et-le-jardinier.md",
        "2020-05-15-ma-lumiere.md",
        "2021-01-24-lumiere-du-matin.md",
        "2026-02-07-guerison.md",
        "2013-07-20-au-pied-dun-arbre.md",
        "2024-03-24-tombe.md",
    ]),
    ("IV. La Transmutation", [
        "2020-09-12-le-soleil-sest-leve.md",
        "2025-03-29-langage-des-racines.md",
        "2024-05-11-decision.md",
        "2014-10-05-3-jours-de-jeune-dans-la-jungle-sur-lile-de-vancouver.md",
        "2020-08-20-loiseau-delicat.md",
        "2025-04-13-purification.md",
        "2025-04-05-resurrection.md",
    ]),
    ("V. L'Ouverture", [
        "2023-03-04-tendre-vers-lautre.md",
        "2026-04-20-miracle.md",
        "2023-01-27-au-bon-moment.md",
        "2024-09-29-a-table.md",
    ]),
    ("VI. La Métamorphose en Silence", [
        "2013-08-18-ce-qui-nous-arrive.md",
        "2021-02-13-de-passage.md",
        "2021-02-13-en-voyage.md",
        "2020-05-29-metamorphose.md",
        "2023-05-15-mes-amours.md",
        "2026-06-17-desir-ardent.md",
        "2021-03-08-ou-sont-mes-reves.md",
        "2025-05-31-recommencer.md",
        "2026-06-16-offrande.md",
    ]),
]

LATEX_HEADER = r"""---
title: "le chemin de la présence"
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
{\fontsize{30}{40}\selectfont\bfseries le chemin de la présence}\\[1.4cm]
{\large\itshape Poèmes — 1992–2026}\\[2.5cm]
{\large Enrico Lévesque}
\vfill
\end{titlepage}
\restoregeometry

\setcounter{tocdepth}{1}
\tableofcontents
\cleardoublepage

"""

EPIGRAPH = """> *Je marche à côté d'une joie*
> *D'une joie qui n'est pas à moi*
> — Hector de Saint-Denys Garneau, *Accompagnement*

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
    lines.append("# le chemin de la présence\n")
    lines.append("\n*Poèmes — 1992–2026*\n")
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

    lines.append(f"\n---\n\n*Le chemin de la présence — {poem_count} poèmes*\n")
    return "".join(lines), poem_count


def process_content(text):
    """Strip title block and shift headings for PDF rendering."""
    lines = text.splitlines(keepends=True)

    # Skip opening title block up to first ---
    i = 0
    while i < len(lines) and not lines[i].startswith("# "):
        i += 1
    i += 1  # skip # le chemin de la présence

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
        r"(\*Le chemin de la présence)",
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
