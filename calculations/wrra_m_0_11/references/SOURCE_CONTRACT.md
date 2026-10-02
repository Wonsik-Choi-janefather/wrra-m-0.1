# Calibration provenance and scope

- Frozen downstream baseline: commit `24707c512c3994f2b19a96d6f257ef7d1249dab3`,
  `calculations/wrra_m_0_10/parameters.json`. Its canonical input hash is
  checked before computation; no baseline source is edited by 0.11.
- MCC 2.3.2: commit `21daec110c0cbecb228c445d587eac8302e7f767`,
  `gitbook/english-edition/part-iv/chapter-23-mass-charge-and-mixing.md`.
  The adopted electron-mode relation is `m0=m_e/23`; this is an
  observation-guided construction, not a universal integer-mass theorem.
  Charge and mass labels remain distinct. Neutrino fine grids and physical
  mode-boundary identification are subsequent work.
- User calibration workbook: `WRRA_M_Calibration_Candidates.xlsx`, SHA256
  `f7ccd9636b7d3b1e9aa6d81fe7e20a14400e41303bf3e6ade4b5e5d6cf2eff32`.
  First-sheet rows 12–16 define the ordered five anchors. Rows 22–33 give
  reference outputs and structural choices; rows 38–65 describe sequential
  fixing and residual freedoms. `calibration_sheet_selected_rows.json`
  records selected rows read from the workbook without editing it. The
  complete candidate list is not treated as simultaneous calibration data.
- G: NIST 2022 CODATA, https://physics.nist.gov/cuu/pdf/wall_2022.pdf.
- Electron rest energy: NIST 2022 CODATA, same table and
  https://physics.nist.gov/cgi-bin/cuu/Value?mec2mev%7Csearch_for=all%21.
- H0: Planck 2018 base-LambdaCDM adopted benchmark,
  https://doi.org/10.1051/0004-6361/201833910.
- f_phi and f_c: rounded inherited downstream physical energy reference.
  They are separate from 0.9 arithmetic targets.

In this release, unqualified address alpha/beta are interpreted using the
actual 0.9 implementation: alpha_addr is the power-law exponent and beta_eff
the derived effective odd-composite admission. Electromagnetic alpha is not
identified by that arithmetic re-expression. This distinction is stated in
both editions and the executable ledger.
