
import json
import numpy as np

###################################################################################################################
#estimation results

with open('/home/pjrice/gp/ACTR-WM/data/parEstResults/Powell/bounded/fivePar/fivePar_estCSS_modelMeanRT_Acc.json', 'r') as fp: 
    fiveParEst = json.load(fp)
    


meanRTDiff = [abs(i-j) for i,j in zip(fiveParEst['model_meanRT'],fiveParEst['subj_meanRT'])]
meanAccDiff = [abs(i-j) for i,j in zip(fiveParEst['model_meanAcc'],fiveParEst['subj_meanAcc'])]

meanDiffs = [np.mean([i,j]) for i,j in zip(meanRTDiff,meanAccDiff)]

idx = meanDiffs.index(min(meanDiffs))

print(fiveParEst['css'][idx])
print(fiveParEst['ga'][idx])
print(fiveParEst['ia'][idx])
print(fiveParEst['lf'][idx])
print(fiveParEst['bll'][idx])


###################################################################################################################
#estimation results

with open('/home/pjrice/gp/ACTR-WM/data/parEstResults/twoBack/parEst_exp.json', 'r') as fp: 
    parEstExp = json.load(fp)
    
meanRTDiff = [abs(i-j) for i,j in zip(parEstExp['model_meanRT'],parEstExp['subj_meanRT'])]
meanAccDiff = [abs(i-j) for i,j in zip(parEstExp['model_meanAcc'],parEstExp['subj_meanAcc'])]

meanDiffs = [np.mean([i,j]) for i,j in zip(meanRTDiff,meanAccDiff)]

idx = meanDiffs.index(min(meanDiffs))

#this part is in the bad trial parts list...
newMeanDiffs = meanDiffs[:]
newMeanDiffs.pop(idx)

newIdx = meanDiffs.index(min(newMeanDiffs))

print(parEstExp['ga'][newIdx])
print(parEstExp['ia'][newIdx])
print(parEstExp['lf'][newIdx])
print(parEstExp['bll'][newIdx])