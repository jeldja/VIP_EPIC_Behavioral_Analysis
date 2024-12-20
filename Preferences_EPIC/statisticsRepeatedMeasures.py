import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import pingouin as pg

file_path = "Example_Coding_For_ANOVA.csv"  
data = pd.read_csv(file_path)


data = data[data["SubjectID"].between(3, 8)]

anova_data = data.melt(
    id_vars=["SubjectID", "AssistanceMagnitude", "TimingDelay"], 
    value_vars=["Score"], 
    var_name="DependentVariable", 
    value_name="Value"
)

anova_results = pg.rm_anova(
    data=anova_data, 
    dv="Value", 
    within=["AssistanceMagnitude", "TimingDelay"], 
    subject="SubjectID", 
    detailed=True
)
print(anova_results)

plt.figure(figsize=(10, 6))
sns.boxplot(
    x="TimingDelay", 
    y="Value", 
    hue="AssistanceMagnitude", 
    data=anova_data, 
    palette="pastel"
)

plt.title("Box Plot of Scores by Timing Delay and Assistance Magnitude")
plt.xlabel("Delay", weight = 'bold', size = 14)
plt.ylabel("Score", weight = 'bold', size = 14)
plt.xticks(weight = 'bold')
plt.yticks(weight = 'bold')
plt.title("Assistance Magnitude", size = 16, weight = 'bold')
#plt.legend(title="Assistance Magnitude")
plt.tight_layout()
plt.show()



#Assistance level
plt.figure(figsize = (4,6))
sns.boxplot(
    x = "AssistanceMagnitude",
    y = "Value",
    data = anova_data,
)

plt.title("Box Plot Assistance Magnitude")
plt.xlabel("Assistance", weight = 'bold')
plt.ylabel("Score", weight = 'bold')
plt.title("Assistance Magnitude", size = 14, weight = 'bold')
plt.xticks(weight = 'bold')
plt.yticks(weight = 'bold')
#plt.legend(title="Assistance Magnitude")
plt.tight_layout()
plt.show()