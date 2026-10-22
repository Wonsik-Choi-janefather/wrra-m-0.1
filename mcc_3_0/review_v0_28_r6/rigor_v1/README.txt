KZF mathematical/computational rigor audit v1.0
Authors: Wonsik Choi and Jeongin Choi. Date: 2026-10-22.

Install requirements.txt, then run: python reproduce.py
This reconstructs the saved ledger and executes originals, normal checks and isolated corruption tests. The initial recorded run executed these commands individually; reproduce.py is the convenience orchestrator, not an additional counted run.

python original/code/compute.py
python build.py
python verify.py
python test_contract.py
python test_corruption.py
python check_em.py

core.py: hardened finite address construction, strict spectrum boundary, input rejection and numerical budget.
verify.py: separate saved-ledger reader, no core import; independent Boolean sieve and direct-power weights.
results/ledger.npz: all 1,015,000 address rows, coordinates, class, weight. No pickle. Read with numpy.load(..., allow_pickle=False).
original/: preserved source and original historical result; replay output is original/results/results.json.
runs/: actual stdout/stderr; results/: actual machine-readable outputs.
REPORT_KO.html: review in input -> WRRA transformation -> outputs -> falsification -> conclusion order.
BOOK_38C_KO.txt: proposed book insertion; not yet merged into the published complete book.

The package retains earlier calibrated inputs. It is not a new derivation of harmonic29, cosmic topology, or a zero-count proof independent of the mpmath library. No external publication is claimed by this package. New implementation is available for reuse under the repository's existing license; original authors and provenance are preserved.
