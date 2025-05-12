import os
import pandas as pd
import math
import matplotlib.pyplot as plt

def calculate_assistance_stats(folder_path):
    assistance_stats = {
        '0%': {'scores': []},
        '10%': {'scores': []},
        '20%': {'scores': []}
    }

    for filename in os.listdir(folder_path):
        if "levelwalking_preferences_ranking" in filename and filename.endswith(".csv"):
            file_path = os.path.join(folder_path, filename)
            data = pd.read_csv(file_path)

            for _, row in data.iterrows():
                condition = row['Condition']
                score = row['Score']

                #adding all the scores in each level of applied assistance
                if 'S0' in condition:
                    assistance_stats['0%']['scores'].append(score)
                elif 'S1' in condition:
                    assistance_stats['10%']['scores'].append(score)
                elif 'S2' in condition:
                    assistance_stats['20%']['scores'].append(score)

    stats = {}
    for level, values in assistance_stats.items():
        scores = values['scores']
        if scores:
            mean = sum(scores) / len(scores)
            variance = sum((x - mean) ** 2 for x in scores) / len(scores)
            std_dev = math.sqrt(variance)
            stats[level] = {
                'average': mean,
                'std_dev': std_dev
            }
        else:
            stats[level] = {
                'average': 0,
                'std_dev': 0
            }
    
    return stats

def plot_assistance_stats(stats):
    assistanceLevels = list(stats.keys())
    averages = [stats[level]['average'] for level in assistanceLevels]
    std_devs = [stats[level]['std_dev'] for level in assistanceLevels]
    plt.figure(figsize=(8, 6))
    bar_positions = range(len(assistanceLevels))
    plt.bar(bar_positions, averages, yerr=std_devs, capsize=5, color=['#05D5FA', '#AD03DE', '#80EF80'], alpha=0.7)
    plt.xticks(bar_positions, assistanceLevels)
    plt.xlabel('Assistance Levels')
    plt.ylabel('Average Scores')
    plt.title('Average Scores with Standard Deviation for Each Assistance Level')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    folder_path = r'C:\Users\user\enterYourFolderPath'  #your folder path
    stats = calculate_assistance_stats(folder_path)
    
    print("Statistics for Each Assistance Level:")
    for level, stat in stats.items():
        print(f"{level} Assistance: Average = {stat['average']:.2f}, Standard Deviation = {stat['std_dev']:.2f}")
        
    plot_assistance_stats(stats)