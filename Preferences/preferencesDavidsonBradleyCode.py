import pandas as pd
import numpy as np
from scipy.optimize import minimize

#Reading data (csv).
data = pd.read_csv('BLST05_Preference.csv') #change folder path here :))))


conditions = set(data['C1']).union(set(data['C2']))
conditions = list(conditions)
n = len(conditions)

#create a mapping from condition name to an index (will be ultilized later for indexing scores :D )
condition_to_idx = {condition: i for i, condition in enumerate(conditions)}

initial_scores = np.ones(n + 1) 

def davidson_log_likelihood(params, data, condition_to_idx):
    scores = params[:-1]  # Condition scores
    delta = params[-1]  # Tie parameter
    
    log_likelihood = 0
    for _, row in data.iterrows():
        idx1 = condition_to_idx[row['C1']]
        idx2 = condition_to_idx[row['C2']]
        
        score1 = scores[idx1]
        score2 = scores[idx2]
        
        denom = score1 + score2 # + tau
        prob1 = score1 / denom
        prob2 = score2 / denom
        prob_tie = delta*(np.sqrt(score1*score2) / denom) 

        if row['Relative'] == 1:
            log_likelihood += np.log(prob2)  #Condition 2 was preferred.
        elif row['Relative'] == -1:
            log_likelihood += np.log(prob1)  #Condition 1 was preferred.
        elif row['Relative'] == 0:
            log_likelihood += np.log(prob_tie)  #tie breaker

    # Return negative log likelihood for minimization
    return -log_likelihood

result = minimize(
    davidson_log_likelihood, 
    initial_scores, 
    args=(data, condition_to_idx), 
    method='BFGS', options={'maxiter': 100}
)


final_scores = result.x[:-1]
delta = result.x[-1]

#dataframe with conditions and scores.
scores_df = pd.DataFrame({
    'Condition': conditions,
    'Score': final_scores
})

#sorting scores
scores_df = scores_df.sort_values(by='Score', ascending=False).reset_index(drop=True)
normalized_scores_df = scores_df.copy()

max_score = np.max(scores_df['Score'])
min_score = np.min(scores_df['Score'])
normalized_scores_df['Score'] = np.round(100*(scores_df['Score'] - min_score)/(max_score - min_score),3)
print(scores_df)
print(normalized_scores_df)
print(f"Delta (tie parameter): {delta}")
normalized_scores_df.to_csv('BLST05_preferences_ranking.csv', index=False) #change the file name to what you want