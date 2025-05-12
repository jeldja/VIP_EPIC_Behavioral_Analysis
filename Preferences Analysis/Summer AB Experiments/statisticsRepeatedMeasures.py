import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import pingouin as pg
import os

file_path = "Example_Coding_For_ANOVA.csv"  
data = pd.read_csv(file_path)


#Identify dependent variables (columns after 'TimingDelay')
dependent_variables = data.columns[3:]  #3 columns are SubjectID, AssistanceMagnitude, and TimingDelay

output_folder = os.path.dirname(file_path)  #output folder 

#perform RM-ANOVA
for variable in dependent_variables:
    anova_data = data.melt(
        id_vars=["SubjectID", "AssistanceMagnitude", "TimingDelay"],
        value_vars=[variable],
        var_name="DependentVariable",
        value_name="Value"
    )
    
    #repeat measures ANOVA
    anova_results = pg.rm_anova(
        data=anova_data,
        dv="Value",
        within=["AssistanceMagnitude", "TimingDelay"],
        subject="SubjectID",
        detailed=True
    )
    
    #save the ANOVA results to a CSV file
    output_file_name = f"{variable}_anova_results.csv"
    output_file_path = os.path.join(output_folder, output_file_name)
    anova_results.to_csv(output_file_path, index=False)
    print(f"ANOVA results for {variable} saved to: {output_file_path}")

    #creating figures
    plt.figure(figsize=(10, 6))
    sns.boxplot(
        x="TimingDelay",
        y="Value",
        hue="AssistanceMagnitude",
        data=anova_data,
        palette="pastel"
    )
    plt.title(f"Box Plot of {variable} by Timing Delay and Assistance Magnitude")
    plt.xlabel("Timing Delay", weight='bold', size=14)
    plt.ylabel(variable, weight='bold', size=14)
    plt.xticks(weight='bold')
    plt.yticks(weight='bold')
    plt.tight_layout()

    #automatically saves the plot in the same folder as the CSV file
    plot_file_name = f"{variable}_boxplot.png"
    plot_file_path = os.path.join(output_folder, plot_file_name)
    plt.savefig(plot_file_path)
    print(f"Boxplot for {variable} saved to: {plot_file_path}")
    plt.close()  