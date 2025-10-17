import matplotlib.pyplot as plt
import re

# Paste your population text here
text = """Agent { p_after_CC=1.00, p_after_CD=0.21, p_after_DC=0.05, p_after_DD=0.35, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=1.00, p_after_CD=0.21, p_after_DC=0.05, p_after_DD=0.30, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=1.00, p_after_CD=0.21, p_after_DC=0.05, p_after_DD=0.30, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=1.00, p_after_CD=0.16, p_after_DC=0.05, p_after_DD=0.40, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=1.00, p_after_CD=0.31, p_after_DC=0.10, p_after_DD=0.25, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=1.00, p_after_CD=0.16, p_after_DC=0.05, p_after_DD=0.35, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=1.00, p_after_CD=0.21, p_after_DC=0.05, p_after_DD=0.25, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=1.00, p_after_CD=0.21, p_after_DC=0.05, p_after_DD=0.30, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=1.00, p_after_CD=0.26, p_after_DC=0.00, p_after_DD=0.30, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=1.00, p_after_CD=0.16, p_after_DC=0.05, p_after_DD=0.35, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=1.00, p_after_CD=0.26, p_after_DC=0.00, p_after_DD=0.30, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=1.00, p_after_CD=0.26, p_after_DC=0.00, p_after_DD=0.30, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=1.00, p_after_CD=0.21, p_after_DC=0.00, p_after_DD=0.30, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=1.00, p_after_CD=0.31, p_after_DC=0.10, p_after_DD=0.25, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=0.95, p_after_CD=0.21, p_after_DC=0.05, p_after_DD=0.25, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=1.00, p_after_CD=0.21, p_after_DC=0.00, p_after_DD=0.30, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=1.00, p_after_CD=0.26, p_after_DC=0.00, p_after_DD=0.30, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=1.00, p_after_CD=0.26, p_after_DC=0.00, p_after_DD=0.30, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=1.00, p_after_CD=0.26, p_after_DC=0.00, p_after_DD=0.30, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=1.00, p_after_CD=0.21, p_after_DC=0.05, p_after_DD=0.35, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=1.00, p_after_CD=0.21, p_after_DC=0.05, p_after_DD=0.30, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=1.00, p_after_CD=0.26, p_after_DC=0.00, p_after_DD=0.30, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=1.00, p_after_CD=0.16, p_after_DC=0.05, p_after_DD=0.35, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=1.00, p_after_CD=0.31, p_after_DC=0.15, p_after_DD=0.25, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=1.00, p_after_CD=0.31, p_after_DC=0.10, p_after_DD=0.25, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=1.00, p_after_CD=0.21, p_after_DC=0.05, p_after_DD=0.30, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=1.00, p_after_CD=0.16, p_after_DC=0.05, p_after_DD=0.35, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=1.00, p_after_CD=0.26, p_after_DC=0.00, p_after_DD=0.30, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=1.00, p_after_CD=0.26, p_after_DC=0.00, p_after_DD=0.30, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=1.00, p_after_CD=0.21, p_after_DC=0.00, p_after_DD=0.25, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=0.95, p_after_CD=0.21, p_after_DC=0.05, p_after_DD=0.25, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=1.00, p_after_CD=0.16, p_after_DC=0.05, p_after_DD=0.35, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=1.00, p_after_CD=0.21, p_after_DC=0.00, p_after_DD=0.35, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=1.00, p_after_CD=0.21, p_after_DC=0.05, p_after_DD=0.25, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=1.00, p_after_CD=0.26, p_after_DC=0.00, p_after_DD=0.30, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=1.00, p_after_CD=0.26, p_after_DC=0.00, p_after_DD=0.30, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=1.00, p_after_CD=0.26, p_after_DC=0.00, p_after_DD=0.30, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=1.00, p_after_CD=0.21, p_after_DC=0.05, p_after_DD=0.25, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=1.00, p_after_CD=0.26, p_after_DC=0.00, p_after_DD=0.30, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=0.95, p_after_CD=0.16, p_after_DC=0.05, p_after_DD=0.35, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=1.00, p_after_CD=0.21, p_after_DC=0.00, p_after_DD=0.25, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=1.00, p_after_CD=0.21, p_after_DC=0.05, p_after_DD=0.35, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=1.00, p_after_CD=0.16, p_after_DC=0.05, p_after_DD=0.35, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=1.00, p_after_CD=0.31, p_after_DC=0.10, p_after_DD=0.25, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=1.00, p_after_CD=0.26, p_after_DC=0.00, p_after_DD=0.30, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=1.00, p_after_CD=0.21, p_after_DC=0.00, p_after_DD=0.25, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=1.00, p_after_CD=0.21, p_after_DC=0.05, p_after_DD=0.25, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=1.00, p_after_CD=0.26, p_after_DC=0.00, p_after_DD=0.30, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=1.00, p_after_CD=0.16, p_after_DC=0.05, p_after_DD=0.35, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=1.00, p_after_CD=0.16, p_after_DC=0.05, p_after_DD=0.35, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=1.00, p_after_CD=0.26, p_after_DC=0.00, p_after_DD=0.30, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=1.00, p_after_CD=0.31, p_after_DC=0.10, p_after_DD=0.25, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=1.00, p_after_CD=0.16, p_after_DC=0.05, p_after_DD=0.35, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=1.00, p_after_CD=0.21, p_after_DC=0.05, p_after_DD=0.35, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=1.00, p_after_CD=0.26, p_after_DC=0.00, p_after_DD=0.30, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=1.00, p_after_CD=0.26, p_after_DC=0.00, p_after_DD=0.30, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=1.00, p_after_CD=0.31, p_after_DC=0.10, p_after_DD=0.25, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=1.00, p_after_CD=0.16, p_after_DC=0.05, p_after_DD=0.35, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=1.00, p_after_CD=0.31, p_after_DC=0.10, p_after_DD=0.25, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=1.00, p_after_CD=0.21, p_after_DC=0.05, p_after_DD=0.30, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=1.00, p_after_CD=0.26, p_after_DC=0.00, p_after_DD=0.30, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=1.00, p_after_CD=0.21, p_after_DC=0.05, p_after_DD=0.30, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=1.00, p_after_CD=0.16, p_after_DC=0.05, p_after_DD=0.35, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=1.00, p_after_CD=0.31, p_after_DC=0.15, p_after_DD=0.25, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=1.00, p_after_CD=0.21, p_after_DC=0.00, p_after_DD=0.25, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=1.00, p_after_CD=0.21, p_after_DC=0.05, p_after_DD=0.30, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=1.00, p_after_CD=0.26, p_after_DC=0.00, p_after_DD=0.30, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=1.00, p_after_CD=0.31, p_after_DC=0.10, p_after_DD=0.25, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=1.00, p_after_CD=0.16, p_after_DC=0.05, p_after_DD=0.35, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=1.00, p_after_CD=0.21, p_after_DC=0.05, p_after_DD=0.25, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=1.00, p_after_CD=0.31, p_after_DC=0.10, p_after_DD=0.25, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=1.00, p_after_CD=0.21, p_after_DC=0.05, p_after_DD=0.35, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=1.00, p_after_CD=0.21, p_after_DC=0.05, p_after_DD=0.35, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=1.00, p_after_CD=0.26, p_after_DC=0.00, p_after_DD=0.30, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=1.00, p_after_CD=0.21, p_after_DC=0.00, p_after_DD=0.30, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=1.00, p_after_CD=0.21, p_after_DC=0.05, p_after_DD=0.30, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=1.00, p_after_CD=0.21, p_after_DC=0.05, p_after_DD=0.30, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=1.00, p_after_CD=0.31, p_after_DC=0.10, p_after_DD=0.25, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=1.00, p_after_CD=0.31, p_after_DC=0.10, p_after_DD=0.25, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=1.00, p_after_CD=0.21, p_after_DC=0.00, p_after_DD=0.25, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=1.00, p_after_CD=0.26, p_after_DC=0.00, p_after_DD=0.30, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=1.00, p_after_CD=0.21, p_after_DC=0.05, p_after_DD=0.25, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=1.00, p_after_CD=0.31, p_after_DC=0.10, p_after_DD=0.25, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=1.00, p_after_CD=0.26, p_after_DC=0.00, p_after_DD=0.30, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=1.00, p_after_CD=0.31, p_after_DC=0.10, p_after_DD=0.25, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=1.00, p_after_CD=0.31, p_after_DC=0.10, p_after_DD=0.25, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=1.00, p_after_CD=0.16, p_after_DC=0.05, p_after_DD=0.35, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=1.00, p_after_CD=0.21, p_after_DC=0.00, p_after_DD=0.30, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=1.00, p_after_CD=0.21, p_after_DC=0.05, p_after_DD=0.35, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=1.00, p_after_CD=0.21, p_after_DC=0.00, p_after_DD=0.25, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=1.00, p_after_CD=0.21, p_after_DC=0.05, p_after_DD=0.30, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=1.00, p_after_CD=0.31, p_after_DC=0.10, p_after_DD=0.25, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=1.00, p_after_CD=0.16, p_after_DC=0.05, p_after_DD=0.35, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=1.00, p_after_CD=0.31, p_after_DC=0.10, p_after_DD=0.25, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=1.00, p_after_CD=0.21, p_after_DC=0.05, p_after_DD=0.30, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=1.00, p_after_CD=0.26, p_after_DC=0.00, p_after_DD=0.30, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=1.00, p_after_CD=0.21, p_after_DC=0.05, p_after_DD=0.25, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=1.00, p_after_CD=0.31, p_after_DC=0.10, p_after_DD=0.25, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=1.00, p_after_CD=0.31, p_after_DC=0.10, p_after_DD=0.25, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
Agent { p_after_CC=1.00, p_after_CD=0.21, p_after_DC=0.00, p_after_DD=0.35, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }
"""

# Extract values using regex
pattern = r"p_after_CC=(\d\.\d+), p_after_CD=(\d\.\d+), p_after_DC=(\d\.\d+), p_after_DD=(\d\.\d+)"
matches = re.findall(pattern, text)

# Convert to float
pCC, pCD, pDC, pDD = zip(*[(float(a), float(b), float(c), float(d)) for a,b,c,d in matches])

# Compute averages
avg_values = [
    sum(pCC)/len(pCC),
    sum(pCD)/len(pCD),
    sum(pDC)/len(pDC),
    sum(pDD)/len(pDD),
]
labels = ['CC', 'CD', 'DC', 'DD']

# Plot
plt.figure(figsize=(6,4))
plt.bar(labels, avg_values)
plt.ylim(0, 1)
plt.title("Average Probability of Cooperation After Each Outcome (Cycle 6000)")
plt.ylabel("p (Probability of Cooperation)")
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

# Print numeric results
for lbl, val in zip(labels, avg_values):
    print(f"{lbl}: {val:.2f}")
