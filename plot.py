import matplotlib.pyplot as plt
import csv

cycles = []
avgPayoffs = []

with open("avg_payoff4.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        cycles.append(int(row["cycle"]))
        avgPayoffs.append(float(row["avg_payoff"]))

plt.plot(cycles, avgPayoffs, marker='o')
plt.xlabel("Cycle")
plt.ylabel("Average Population Payoff")
plt.title("Evolution of Average Payoff Over Time")
plt.grid(True)
plt.ylim(0, 4)
plt.show()
