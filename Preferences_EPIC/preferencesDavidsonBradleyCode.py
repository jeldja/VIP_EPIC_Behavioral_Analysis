import pandas as pd
import numpy as np
from scipy.optimize import minimize

# Reading data (csv).
data = pd.read_csv('IRLHEAB06_levelwalking_preference.csv') # change correct path if needed

# getting unique condtions
conditions = set(data['C1']).union(set(data['C2']))
conditions = list(conditions)
n = len(conditions)

# Create a mapping from condition name to an index (will be ultilized later for indexing scores :D )
condition_to_idx = {condition: i for i, condition in enumerate(conditions)}

# Initialize an array of scores for each condition and the tie parameter, (n + 1) to account for tau.
initial_scores = np.ones(n + 1) 

def davidson_log_likelihood(params, data, condition_to_idx):
    scores = params[:-1]  # Condition scores
    tau = params[-1]  # Tie parameter
    
    log_likelihood = 0
    for _, row in data.iterrows():
        idx1 = condition_to_idx[row['C1']]
        idx2 = condition_to_idx[row['C2']]
        
        score1 = scores[idx1]
        score2 = scores[idx2]
        
        denom = score1 + score2 + tau
        prob1 = score1 / denom
        prob2 = score2 / denom
        prob_tie = tau / denom

        if row['Relative'] == 1:
            log_likelihood += np.log(prob2)  # Condition 2 was preferred.
        elif row['Relative'] == -1:
            log_likelihood += np.log(prob1)  # Condition 1 was preferred.
        elif row['Relative'] == 0:
            log_likelihood += np.log(prob_tie)  # if there was no preference between the two conditions.

    # Return negative log likelihood for minimization
    return -log_likelihood

# for estimating scores that maximize likelihood 
result = minimize(
    davidson_log_likelihood, 
    initial_scores, 
    args=(data, condition_to_idx), 
    method='BFGS', options={'maxiter': 100}
)

# getting optimized scores and tau
final_scores = result.x[:-1]
tau = result.x[-1]

# dataframe with conditions and scores.
scores_df = pd.DataFrame({
    'Condition': conditions,
    'Score': final_scores
})

# Sorting the scores for the preferences rank.
scores_df = scores_df.sort_values(by='Score', ascending=False).reset_index(drop=True)
print(scores_df)
print(f"Tau (tie parameter): {tau}")
