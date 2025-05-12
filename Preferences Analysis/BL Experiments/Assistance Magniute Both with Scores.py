import pandas as pd
import matplotlib.pyplot as plt

#reading data (csv)
# Note: Make sure to replace the file name with the actual file name you are using.
df = pd.read_csv('BLST05_preferences_ranking.csv')

#categorizing conditions (assistance magnitudes)
def categorize_condition(condition):
    if 'R1L1' in condition:
        return 'C1'
    elif 'R1L2' in condition:
        return 'C2'
    elif 'R2L1' in condition:
        return 'C3'
    elif 'R2L2' in condition:
        return 'C4'
    else:
        return 'Other'

df['Category'] = df['Condition'].apply(categorize_condition)

#filter out rows that do not belong to the defined categories
df = df[df['Category'].isin(['C1', 'C2', 'C3', 'C4'])]

# Calculate average scores and standard deviations
avg_scores = df.groupby('Category')['Score'].mean()
std_devs = df.groupby('Category')['Score'].std()

#plotting with error bars
plt.figure(figsize=(8, 6))
plt.bar(
    avg_scores.index, 
    avg_scores.values, 
    yerr=std_devs.values,  #Add standard deviation as error bars
    capsize=5,             #Add caps to error bars
    color=['red', 'orange', 'purple', 'blue']
)
plt.title('Average Scores by Assistance Magnitude Category',  fontweight='bold', fontsize=16)
plt.xlabel('Assistance Magnitude (R1L1, R1L2, R2L1, R2L2)',  fontweight='bold', fontsize=16)
plt.ylabel('Average Score',  fontweight='bold')
plt.xticks(rotation=0)
# plt.grid(axis='y')  # Uncomment if you want a grid
plt.tight_layout()
plt.show()

