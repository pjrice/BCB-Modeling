
    
    
def scatter_dLOO (subjMeasures,modelPredictions,measure):
    
    if measure=='acc':
        subjMeas = 'subjMeanAcc'
        modelMeas = 'meanAcc'
        xAxisTitle = 'subj mean accuracy'
        yAxisTitle = 'model mean acc (over 100 runs)'
    elif measure=='rt':
        subjMeas = 'subjMeanRTs'
        modelMeas = 'meanRT'
        xAxisTitle = 'subj mean RT'
        yAxisTitle = 'model mean RT (over 100 runs)'
    else:
        print('"measure" arg must be either "acc" or "rt"')
        
    fig, axarr = plt.subplots(5,4, constrained_layout=True, sharex='col', sharey='col')
    
    modelKeys = list(modelPredictions.keys())
    
    rowIndicies = [0,1,2,3,4,0,1,2,3,0,1,2,0,1]
    rowIdx = 0
    for modelKey in modelKeys:
        if len(modelKey.split(','))==4:
            colIdx = 0
        elif len(modelKey.split(','))==3:
            colIdx = 1
        elif len(modelKey.split(','))==2:
            colIdx = 2
        elif len(modelKey.split(','))==1:
            colIdx = 3
            
        axarr[rowIndicies[rowIdx],colIdx].scatter(subjMeasures[subjMeas],modelPredictions[modelKey][modelMeas])
        m,b = np.polyfit(subjMeasures[subjMeas],modelPredictions[modelKey][modelMeas],1)
        axarr[rowIndicies[rowIdx],colIdx].plot(subjMeasures[subjMeas], m*np.array(subjMeasures[subjMeas])+b)
        plotAnno = 'r = '+str(round(scipy.stats.pearsonr(subjMeasures[subjMeas],modelPredictions[modelKey][modelMeas])[0],2))
        axarr[rowIndicies[rowIdx],colIdx].text(np.min(subjMeasures[subjMeas]), np.max(modelPredictions[modelKey][modelMeas]),plotAnno)
        axarr[rowIndicies[rowIdx],colIdx].set_xlabel(xAxisTitle)
        axarr[rowIndicies[rowIdx],colIdx].set_ylabel(yAxisTitle)
        axarr[rowIndicies[rowIdx],colIdx].set_title(modelKey)
        
        rowIdx = rowIdx+1
        
    plt.show()
            





import json

###################################################################################################################
#estimation results

#zero-back
with open('/home/pjrice/gp/ACTR-WM/data/parEstResults/Powell/bounded/fivePar/fivePar_estCSS.json', 'r') as fp: 
    fiveParEst = json.load(fp)
        
keys2remove = ['converged', 'allRT_rmse', 'allAcc_rmse', 'bbRT_rmse', 'bbAcc_rmse', 'tarRT_rmse', 'lurRT_rmse', 'nlrRT_rmse', 'tarAcc_rmse', 'lurAcc_rmse', 'nlrAcc_rmse', 'model_tarRT_mean', 'model_lurRT_mean', 'model_nlrRT_mean', 'subj_tarRT_mean', 'subj_lurRT_mean', 'subj_nlrRT_mean', 'model_tarAcc_mean', 'model_lurAcc_mean', 'model_nlrAcc_mean', 'subj_tarAcc_mean', 'subj_lurAcc_mean', 'subj_nlrAcc_mean', 'rtDiff_mean']
    
[fiveParEst.pop(key) for key in keys2remove]

import csv


with open('/home/pjrice/gp/ACTR-WM/data/parEstResults/Powell/bounded/fivePar/fiveParEstResults.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(fiveParEst.keys())
    writer.writerows(zip(*fiveParEst.values()))
    
    
#two-back
with open('/home/pjrice/gp/ACTR-WM/data/parEstResults/twoBack/parEst_exp.json', 'r') as fp:
    resultsExp = json.load(fp)
    
keys2remove = ['converged', 'allRT_rmse', 'allAcc_rmse', 'bbRT_rmse', 'bbAcc_rmse', 'tarRT_rmse', 'lurRT_rmse', 'nlrRT_rmse', 'tarAcc_rmse', 'lurAcc_rmse', 'nlrAcc_rmse', 'model_tarRT_mean', 'model_lurRT_mean', 'model_nlrRT_mean', 'subj_tarRT_mean', 'subj_lurRT_mean', 'subj_nlrRT_mean', 'model_tarAcc_mean', 'model_lurAcc_mean', 'model_nlrAcc_mean', 'subj_tarAcc_mean', 'subj_lurAcc_mean', 'subj_nlrAcc_mean', 'rtDiff_mean', 'model_meanRT', 'model_meanAcc', 'subj_meanRT', 'subj_meanAcc']

[resultsExp.pop(key) for key in keys2remove]

with open('/home/pjrice/gp/ACTR-WM/data/parEstResults/twoBack/twoBack_parEstResults.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(resultsExp.keys())
    writer.writerows(zip(*resultsExp.values()))
    
###################################################################################################################
#dLOO results

#zero-back
with open('/home/pjrice/gp/ACTR-WM/data/parEstResults/Powell/bounded/fivePar/dLOO_results.json', 'r') as fp: 
    dLOO_results = json.load(fp)
    
subjData = dLOO_results['subj']

with open('/home/pjrice/gp/ACTR-WM/data/parEstResults/Powell/bounded/fivePar/subjMeasures.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(subjData.keys())
    writer.writerows(zip(*subjData.values()))
    
keys2remove = ['RT_corr', 'RT_pval', 'Acc_corr', 'Acc_pval', 'cwAcc_corr', 'cwAcc_pval']
modelKeys = list(dLOO_results['models'].keys())
for modelKey in modelKeys:
    [dLOO_results['models'][modelKey].pop(key) for key in keys2remove]
    
import pandas as pd

test = pd.json_normalize(dLOO_results['models'],sep='_')

test1 = test.to_dict(orient='records')[0]

with open('/home/pjrice/gp/ACTR-WM/data/parEstResults/Powell/bounded/fivePar/modelPreds.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(test1.keys())
    writer.writerows(zip(*test1.values()))
    
##################################################################################################
#two-back
with open('/home/pjrice/gp/ACTR-WM/data/parEstResults/twoBack/dLOO_results.json', 'r') as fp: 
    dLOO_results = json.load(fp)
    
subjData = dLOO_results['subj']

with open('/home/pjrice/gp/ACTR-WM/data/parEstResults/twoBack/subjMeasures.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(subjData.keys())
    writer.writerows(zip(*subjData.values()))
    
keys2remove = ['RT_corr', 'RT_pval', 'Acc_corr', 'Acc_pval', 'cwAcc_corr', 'cwAcc_pval']
modelKeys = list(dLOO_results['models'].keys())

for modelKey in modelKeys:
    [dLOO_results['models'][modelKey].pop(key) for key in keys2remove]
    
import pandas as pd

test = pd.json_normalize(dLOO_results['models'],sep='_')

test1 = test.to_dict(orient='records')[0]


with open('/home/pjrice/gp/ACTR-WM/data/parEstResults/twoBack/modelPreds.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(test1.keys())
    writer.writerows(zip(*test1.values()))


















































