import math

# Case 1: hypothetical retention, not measured recall probability
for n in (0, 1, 3, 5, 10):
    trace = 0.85 ** n
    print(n, f"{trace:.6f}")

# Case 2: hypothetical failure residue and challenge probability
def probability(residue, resource):
    score = 1.2 + 0.9 * resource - 1.1 * residue
    return 1.0 / (1.0 + math.exp(-score))

residue = 0.0
for failures in range(6):
    high = probability(residue, 1.0)
    low = probability(residue, 0.3)
    print(failures, f"{residue:.6f}",
          f"{high:.6f}", f"{low:.6f}")
    residue = 0.8 * residue + 0.4

# Additional calculations in the expanded manuscript
import statistics
changes = [4, 2, 6, 2, 6]
print("mean", f"{statistics.mean(changes):.6f}")
print("sample_sd", f"{statistics.stdev(changes):.6f}")
print("mean_se", f"{statistics.stdev(changes) / math.sqrt(len(changes)):.6f}")
print("retention_0.95_at_10", f"{0.95 ** 10:.6f}")
print("fixed_point", f"{0.4 / (1 - 0.8):.6f}")
print("fixed_high", f"{probability(2.0, 1.0):.6f}")
print("fixed_low", f"{probability(2.0, 0.3):.6f}")
r = 0.0
for _ in range(5):
    r = 0.8 * r + 0.4
for _ in range(5):
    r = 0.8 * r
print("after_no_new_failure_5", f"{r:.6f}", f"{probability(r, 1.0):.6f}")

# A rescaled hidden trace can give identical observable probabilities
r1 = r2 = 0.0
max_difference = 0.0
for _ in range(6):
    p1 = probability(r1, 1.0)
    score2 = 1.2 + 0.9 - 0.55 * r2
    p2 = 1.0 / (1.0 + math.exp(-score2))
    max_difference = max(max_difference, abs(p1 - p2))
    r1 = 0.8 * r1 + 0.4
    r2 = 0.8 * r2 + 0.8
print("scale_change_max_difference", f"{max_difference:.6f}")
