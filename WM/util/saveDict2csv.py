
import json

#with open('/home/pjrice/gp/ACTR-WM/data/parEstResults/Powell/bounded/fivePar/fivePar_estCSS_modelMeanRT_Acc.json', 'r') as fp: 
#    resultsExp = json.load(fp)
    
with open('/home/pjrice/gp/ACTR-WM/data/parEstResults/twoBack/parEst_exp.json', 'r') as fp:
    resultsExp = json.load(fp)


rtDiffs = [abs(i-j) for i,j in zip(resultsExp['model_meanRT'],resultsExp['subj_meanRT'])]

accDiffs = [abs(i-j) for i,j in zip(resultsExp['model_meanAcc'],resultsExp['subj_meanAcc'])]

diffMeans = [np.mean([i,j]) for i,j in zip(rtDiffs,accDiffs)]

minVal = min(diffMeans)

diffMeans.index(minVal)


import pandas as pd

df = pd.DataFrame.from_dict(resultsExp,orient='index').transpose()
print(df)
#df.to_csv('/home/pjrice/gp/ACTR-WM/data/parEstResults/Powell/bounded/fivePar/fivePar_resultsExp.csv',index=False)
df.to_csv('/home/pjrice/gp/ACTR-WM/data/parEstResults/twoBack/twoBack_resultsExp.csv',index=False)