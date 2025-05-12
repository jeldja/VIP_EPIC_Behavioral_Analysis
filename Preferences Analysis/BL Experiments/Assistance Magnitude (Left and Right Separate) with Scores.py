import pandas as pd
import matplotlib.pyplot as plt

#reading data (csv).
df = pd.read_csv("BLST05_preferences_ranking.csv")  #put actual file name here (same folder as this script)

#categories
categories = {
    "R1": df[df['Condition'].str.contains("R1", na=False)],
    "R2": df[df['Condition'].str.contains("R2", na=False)],
    "L1": df[df['Condition'].str.contains("L1", na=False)],
    "L2": df[df['Condition'].str.contains("L2", na=False)],
}

#computing average and standard deviation
averages = {key: value['Score'].mean() for key, value in categories.items()}
std_devs = {key: value['Score'].std() for key, value in categories.items()}

#making plot
plt.figure(figsize=(8, 6))
plt.bar(
    averages.keys(), 
    averages.values(), 
    yerr=std_devs.values(),  
    capsize=5,               
    color='purple'
)
plt.xlabel('Condition Categories', fontweight='bold')
plt.ylabel('Average Score', fontweight='bold')
plt.title('Average Score by Condition Category (R1, R2, L1, L2)', fontweight='bold')
plt.show()

