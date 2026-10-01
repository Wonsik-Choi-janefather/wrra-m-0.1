# WRRA-M 0.5 reproduction

From the repository root:

```bash
python -m pip install -r calculations/wrra_m_0_5/requirements.txt
python calculations/wrra_m_0_5/compute.py --out calculations/wrra_m_0_5/results
```

Inputs are editable in `parameters.json`. The recorded output is in
`results/results.json`. See `README.txt` for model scope and limits.

The optional document builder `build_report.py` also requires `python-docx`
and the `pandoc` executable. It uses its own directory and writes native
Word math to a `deliverables` directory. The supplied Korean PDF and DOCX
are in [the paper directory](../../paper).

Author: Wonsik Choi / 최원식 · CC BY 4.0.

