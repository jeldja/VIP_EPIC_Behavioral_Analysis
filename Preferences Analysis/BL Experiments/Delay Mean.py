import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#Read the CSV data
data = pd.read_csv('BLST05_preferences_ranking.csv')


data['Dx'] = data['Condition'].str.extract(r'(D\d)')
dx_values = sorted(data['Dx'].dropna().unique(), key=lambda x: int(x[1]))

#Calculate means and standard deviations
means = []
stds = []
for dx in dx_values:
    group_scores = data[data['Dx'] == dx]['Score']
    means.append(group_scores.mean())
    stds.append(group_scores.std())

#plotting with error bars
fig, ax = plt.subplots(figsize=(10, 6))
x = np.arange(len(dx_values))
width = 0.4  
ax.bar(x, means, width, yerr=stds, capsize=5, color='blue', alpha=0.8)
#plot
ax.set_xlabel('Timing Delay (Dx)', fontweight='bold', fontsize=16)
ax.set_ylabel('Average Score', fontweight='bold', fontsize=16)
ax.set_title('Average Scores by Timing Delay (Mean ± Std Dev)', fontweight='bold', fontsize=16)
ax.set_xticks(x)
ax.set_xticklabels(dx_values)

plt.tight_layout()
plt.show()
