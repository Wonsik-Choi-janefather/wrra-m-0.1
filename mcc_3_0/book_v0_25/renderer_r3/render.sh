#!/bin/sh
set -eu
for lang in KO EN; do
 pandoc "MCC_3_0_Full_Book_${lang}_v0.25.md" -f markdown+autolink_bare_uris-implicit_figures -s --pdf-engine=xelatex --lua-filter=renderer_r3/fitmath.lua -H renderer_r3/header.tex -V "mainfont=Noto Sans CJK KR" -V geometry:margin=22mm -V fontsize=10pt -V documentclass=report -o "MCC_3_0_Full_Book_${lang}_v0.25.pdf"
done
