From Number Structure to Particle Selection — version 0.2
Date: 2026-10-08

This package is a research draft, not a submitted or peer-reviewed article.
No new-author approval is inferred from approval of the previous r11 paper.

Reproduction
1. Use Python 3 with numpy and scipy.
2. Run python source/reproduce.py from the extracted package root.
3. Inspect source/results.json. Expected: 47/47 implementation checks pass.
No network is needed. The source r11 control JSON is included verbatim.

Main baseline
Conditional electron-pair probability 0.7390664036122881.
Mean pair rest energy 55.89496412886883 MeV.
Mean pair kinetic energy 155.4217868711312 MeV.
Reference total pair energy 211.316751 MeV.
All are model results under the declared routing law; not measured abundances.

Input provenance
r11_controls.json: prior r11 phase_control_comparison_results.json.
Prior public record: https://doi.org/10.5281/zenodo.23237629
Electron energy: NIST CODATA 2022, 0.51099895069 MeV.
Muon energy: NIST CODATA 2022, 105.6583755 MeV.
NIST URLs are in manuscript references.

Scope
The routing chi = sum(nu_p^2)/(sum(nu_p))^2 is a declared new rule.
Electron, muon masses, charges and spin are supplied physical identifications.
Muon pair at threshold is an idealized kinematic label, not a production rate.
The volume derivative keeps occupations fixed and ignores decay/annihilation.
Its q-like number is a formal instantaneous diagnostic, not present-day cosmology.
The 15-channel Hamiltonian and a unique particle grammar are not implemented.
No public DOI or external review exists for this extension.

Document reconstruction (optional)
Requires python-docx and pandoc. Create an output/ folder next to source/.
Run in order: source/build.py, source/polish.py, source/math_format.py,
source/flow.py, source/retitle.py, source/table_layout.py, source/ko_layout.py, source/final_clarity.py. DOCX files are generated under output/.
The delivered PDFs were rendered with LibreOffice and visually inspected.

A separate Astra (medium reasoning) internal AI review accompanies this draft.
It is not journal peer review or acceptance. Scientific findings refer to the reviewed v0.2.

Verification scope: phenotype 0.05 and address-9 admissions are recalculated; D=0.268 and R=0.682 are inherited r11 energy-law inputs, not freshly reconstructed filters.
Reversed and constant routing are explicitly checked for each of four controls.
The arithmetic-to-species rule is one possible component of a toy model, not a physically verified mechanism.
Artistic motivation is personal research history, not physical evidence.
