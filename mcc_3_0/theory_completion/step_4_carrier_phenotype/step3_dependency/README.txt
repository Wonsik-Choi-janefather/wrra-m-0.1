WRRA 3.0 theory improvement Step3 reviewed v0.4
Current decision and limits: STEP3_REVIEW_KO.txt / STEP3_REVIEW_EN.txt.
Earlier reports preserve the comparison evidence.
Run from this directory, Python without -O, numpy 2.3.5 and scipy 1.17.0:
python structure_comparison.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python streaming_selection.py
python minimum_phase_state.py
python mode_comparison.py
python integration_review.py
34 computational checks; frozen dependency snapshots included.
phase_kernel.py is the reusable adopted kernel.
Equivalent execution preserves the model; reduced models change its readout.
No full-theory completion or universal physical minimum is asserted.
