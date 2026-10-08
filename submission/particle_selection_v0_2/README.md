# From Number Structure to Particle Selection

**A Possible Readout and Its Energy–Pressure Constraints in a Finite WRRA Toy Model**

Wonsik Choi and Jeongin Choi · v0.2 · 8 October 2026

## Files

- [English manuscript (PDF)](output/WRRA_Address_Particle_Interface_v0_2_EN.pdf)
- [English manuscript (Word)](output/WRRA_Address_Particle_Interface_v0_2_EN.docx)
- [한국어 해설 (PDF)](output/WRRA_Address_Particle_Interface_v0_2_KO_Guide.pdf)
- [Complete reproducibility package](output/WRRA_Address_Particle_Interface_v0_2_Package.zip)
- [Astra medium internal AI re-review](source/Astra_Medium_ReReview_KO.txt)
- [Revision response](source/Revision_Response_KO.txt)
- [Final conclusion clarification](source/Conclusion_Clarification.txt)

## Verified inputs → WRRA transformation → outputs → failure conditions

- Inputs: archived finite r11 preparation parameters, known electron/muon rest energies, declared routing and volume-law assumptions. The phenotype 0.05 is recalculated; D=0.268 and R=0.682 are inherited inputs.
- Transformation: prime-factor occurrence collision statistic → conditional particle-pair selection → one rest/kinetic energy budget → volume derivative and pressure.
- Outputs: four distinct conditional electron-pair probabilities, energy closure and a general sectorwise energy/derivative compatibility criterion. 47/47 implementation checks pass; these are not 47 empirical confirmations.
- Failure conditions: inconsistent phenotype reconstruction, channel normalization/positivity, output-state accounting or pressure differentiation. Testing the physical interpretation additionally requires a specified preparation and coupling.

The arithmetic-to-particle assignment is one possible component of a finite toy model, not a physically verified interaction. Particle properties are inputs. The artistic origin is personal research motivation, not cosmological evidence. Frozen occupation excludes decay, creation and annihilation, so the formal expansion diagnostic is not a present-universe prediction.

## Reproduce

Requires Python 3, numpy and scipy. From this directory:

```bash
python source/reproduce.py
```

Expected: 47/47 checks pass. See [execution notes](source/README.txt).

## Publication status

Public research preprint materials; not journal accepted. Astra medium PASS is an internal AI review, not journal peer review. The final wording-only conclusion clarification follows that review and is recorded separately.

Zenodo registration: pending; no new DOI has yet been issued. The manuscript retains its preparation-stage availability statement; this README will record the release DOI once registration succeeds.

Prior r11 record: https://doi.org/10.5281/zenodo.23237629

License: CC BY 4.0, consistent with this repository. Correspondence: janefather@gmail.com. Wonsik Choi ORCID: https://orcid.org/0009-0001-4263-9772
