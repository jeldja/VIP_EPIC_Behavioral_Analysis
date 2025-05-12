import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#Read the CSV data
data = pd.read_csv('BLST05_preferences_ranking.csv')

data['Dx'] = data['Condition'].str.extract(r'(D\d)')

# Group by Delay mode :)
dx_values = sorted(data['Dx'].dropna().unique(), key=lambda x: int(x[1]))


base_labels = ['R1L1', 'R1L2', 'R2L1', 'R2L2']

fig, ax = plt.subplots(figsize=(14, 6))
width = 0.15  # width of each bar
x = np.arange(len(dx_values))

#plot bars for each base label
for i, base in enumerate(base_labels):
    scores = []
    for dx in dx_values:
        match = data[(data['Dx'] == dx) & (data['Condition'].str.startswith(base))]
        score = match['Score'].values[0] if not match.empty else 0
        scores.append(score)
    ax.bar(x + i * width, scores, width, label=base)

#Calculate means and standard deviations for each Dx
means = []
stds = []
for dx in dx_values:
    group_scores = data[data['Dx'] == dx]['Score']
    means.append(group_scores.mean())
    stds.append(group_scores.std())

#plot mean with error bars
mean_pos = x + len(base_labels) * width
ax.bar(mean_pos, means, width, yerr=stds, capsize=5, label='Mean ± Std', color='gray', alpha=0.8)

#plot 
ax.set_xlabel('Timing Delay', fontweight='bold', fontsize=16)
ax.set_ylabel('Score', fontweight='bold', fontsize=16)
ax.set_title('Scores by Timing Delay', fontweight='bold', fontsize=16)
ax.set_xticks(x + 2 * width)
ax.set_xticklabels(dx_values)
ax.legend()

plt.tight_layout()
plt.show()

