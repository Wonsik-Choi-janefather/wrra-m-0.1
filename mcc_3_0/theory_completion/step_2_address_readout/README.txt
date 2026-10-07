WRRA 3.0 theory improvement — Step 2 v0.4, scoped review
Read STEP2_REVIEW_KO.txt / STEP2_REVIEW_EN.txt for the current scope judgment.
Earlier reports preserve their milestone-specific status.
Replay in order:
python address_structure.py
python readout_ledger.py
python connection_replay.py
python channel_bridge.py
Dependencies: numpy==2.3.5 scipy==1.17.0; use Python without -O.
52 computational checks; outputs in four result JSON files.
Pinned Step1 dependencies and connection sources are included.
Full theory completion and channel-specific interacting dynamics are not asserted.
