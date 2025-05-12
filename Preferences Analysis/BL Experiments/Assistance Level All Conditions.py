
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the CSV file
df = pd.read_csv('BLST05_preferences_ranking.csv')

# Function to categorize condition
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

# Apply the categorization
df['Category'] = df['Condition'].apply(categorize_condition)

# Filter only relevant categories
df = df[df['Category'].isin(['C1', 'C2', 'C3', 'C4'])]

# Extract Dx number from the condition string
df['Dx'] = df['Condition'].str.extract(r'D(\d)', expand=False)
df['Dx'] = 'D' + df['Dx']  # Add 'D' prefix for clarity

# Plot
plt.figure(figsize=(12, 6))

# Bar positions
categories = ['C1', 'C2', 'C3', 'C4']
x = np.arange(len(categories))
width = 0.1  # bar width
dx_values = ['D0', 'D1', 'D2', 'D3', 'D4', 'D5']

# Calculate category means and standard deviations
category_means = df.groupby('Category')['Score'].mean()
category_stds = df.groupby('Category')['Score'].std()

# Plot bars for each Dx value
for i, dx in enumerate(dx_values):
    # Filter data for this specific Dx
    dx_data = df[df['Dx'] == dx]
    
    # Calculate mean score for each category for this Dx
    dx_means = dx_data.groupby('Category')['Score'].mean()
    
    # Plot bars for this Dx
    plt.bar(x + i*width - 3*width, 
            [dx_means.get(cat, 0) for cat in categories],  # Get mean or 0 if not present
            width, 
            label=dx)

# Plot mean with error bars
plt.bar(x + 3*width, category_means, width, yerr=category_stds, capsize=5, label='Mean', color='skyblue')

# Formatting
plt.xticks(x, categories)
plt.xlabel('Assistance Magnitude Categories (R1L1, R1L2, R2L1, R2L2)', fontweight='bold')
plt.ylabel('Average Score', fontweight='bold')
plt.title('Scores by Assistance Magnitude', fontweight='bold')
plt.tight_layout()
plt.show()