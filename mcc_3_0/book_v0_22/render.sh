#!/bin/sh
set -eu
for lang in KO EN; do
  pandoc "MCC_3_0_Full_Book_${lang}_v0.22.md" -f markdown+autolink_bare_uris -s --pdf-engine=xelatex --lua-filter=fitmath.lua -H header.tex -V mainfont='Noto Sans CJK KR' -V geometry:margin=22mm -V fontsize=10pt -V documentclass=report -o "MCC_3_0_Full_Book_${lang}_v0.22.pdf"
done
