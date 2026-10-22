#!/bin/sh
set -eu
cd "$(dirname "$0")/.."
for lang in KO EN; do
pandoc "MCC_3_0_Full_Book_${lang}_v0.28-r1.md" -f markdown+autolink_bare_uris-implicit_figures -s --pdf-engine=xelatex --resource-path=. --lua-filter=review/fitmath.lua -H review/header.tex -V 'mainfont=Noto Sans CJK KR' -V geometry:margin=22mm -V fontsize=10pt -V documentclass=report -o "MCC_3_0_Full_Book_${lang}_v0.28-r1.pdf"
done
