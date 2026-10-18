#!/bin/sh
set -eu
for lang in KO EN; do
 pandoc "WRRA_Alternating_Output_Conjugate_Conversion_${lang}_v1.0.md" --from=markdown-implicit_figures --pdf-engine=xelatex -V 'mainfont=Noto Sans CJK KR' -V fontsize=10pt -V geometry:margin=24mm -V colorlinks=true -V urlcolor=blue -H layout.tex -o "WRRA_Alternating_Output_Conjugate_Conversion_${lang}_v1.0.pdf"
done
