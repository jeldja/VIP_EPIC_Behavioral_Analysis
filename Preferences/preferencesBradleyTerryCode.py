import pandas as pd
import numpy as np
from scipy.optimize import minimize

#reading data (csv).
data = pd.read_csv('IRLHEAB06_levelwalking_preference.csv') #change file path if needed.

conditions = set(data['C1']).union(set(data['C2']))
conditions = list(conditions)
n = len(conditions)

#Create a mapping from condition name to an index (will be ultilized later for indexing scores :D )
condition_to_idx = {condition: i for i, condition in enumerate(conditions)}

initial_scores = np.ones(n)

def bradley_terry_log_likelihood(scores, data, condition_to_idx):
    log_likelihood = 0
    for _, row in data.iterrows():
        #Get indices of the two conditions in this comparison
        idx1 = condition_to_idx[row['C1']]
        idx2 = condition_to_idx[row['C2']]

        # print(idx1, idx2) , for debugging 
        
        score1 = scores[idx1]
        score2 = scores[idx2]
        prob1 = score1 / (score1 + score2)
        prob2 = score2 / (score1 + score2)

        #print(f"score 1 {score1}, row['Relative'] {row['Relative']}, idx {idx1}"), for debugging
        
        if row['Relative'] == 1:
            log_likelihood += np.log(prob2)  # Condition 2 was preferred.
        elif row['Relative'] == -1:
            log_likelihood += np.log(prob1)  # Condition 1 was preferred.

    # Return negative log likelihood for minimization
    return -log_likelihood

# bradley_terry_log_likelihood(initial_scores, data, condition_to_idx) , debugging testing

# estimating the scores that maximize likelihood
result = minimize(
    bradley_terry_log_likelihood, 
    initial_scores, 
    args=(data, condition_to_idx), 
    method='BFGS', options={'maxiter':2}
)

# Get the optimized scores
final_scores = result.x

# dataframe with conditions and scores.
scores_df = pd.DataFrame({
    'Condition': conditions,
    'Score': final_scores
})

# Sorting the scores for the preferences rank.
scores_df = scores_df.sort_values(by='Score', ascending=False).reset_index(drop=True)
print(scores_df)