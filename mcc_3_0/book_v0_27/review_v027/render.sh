#!/bin/sh
set -eu
book_root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$book_root"
for lang in KO EN; do
  pandoc "MCC_3_0_Full_Book_${lang}_v0.27.md" \
    -f markdown+autolink_bare_uris-implicit_figures -s --pdf-engine=xelatex \
    --lua-filter=review_v026/fitmath.lua -H review_v026/header.tex \
    -V 'mainfont=Noto Sans CJK KR' -V geometry:margin=22mm \
    -V fontsize=10pt -V documentclass=report \
    -o "MCC_3_0_Full_Book_${lang}_v0.27.pdf"
done
