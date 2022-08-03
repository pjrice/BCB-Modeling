# ***FIVE*** parameter zero-back model estimation

import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '/home/pjrice/gp/ACTR-WM/code/estimation/zeroBack/fiveParEst')
from modelEstimationFunctions import *

import os
import json

results,badSubjs = estPars_byPart('/home/pjrice/gp/ACTR-WM/')

resultsExp = expandEstResults_bootstrap(results)
with open('/home/pjrice/gp/ACTR-WM/data/parEstResults/Powell/bounded/fivePar/fivePar_estCSS_modelMeanRT_Acc.json', 'w') as fp: 
    json.dump(resultsExp,fp)


#subjMeasures,modelPredictions = parameterVarExp(fiveParEst)
#with open('/home/pjrice/gp/ACTR-WM/data/parEstResults/Powell/bounded/fivePar/subjMeasures.json', 'w') as fp: json.dump(subjMeasures,fp)    
#with open('/home/pjrice/gp/ACTR-WM/data/parEstResults/Powell/bounded/fivePar/modelPredictions.json', 'w') as fp: json.dump(modelPredictions,fp)

#modelSubjCorrs = parameterVarExp_perPart(fiveParEst)
#with open('/home/pjrice/gp/ACTR-WM/data/parEstResults/Powell/bounded/fivePar/modelSubjCorrs.json', 'w') as fp: json.dump(modelSubjCorrs,fp) 

#corrResults = parameterVarExp(fiveParEst)
#with open('/home/pjrice/gp/ACTR-WM/data/parEstResults/Powell/bounded/fivePar/group_and_perPar_corrData.json', 'w') as fp: json.dump(corrResults,fp) 

#looCorrs = parameterVarExp_LOO(fiveParEst)
#with open('/home/pjrice/gp/ACTR-WM/data/parEstResults/Powell/bounded/fivePar/looCorrs.json', 'w') as fp: json.dump(looCorrs,fp) 

dLOO_results = parameterVarExp_dLOO(fiveParEst)
with open('/home/pjrice/gp/ACTR-WM/data/parEstResults/Powell/bounded/fivePar/dLOO_results-new.json', 'w') as fp: json.dump(dLOO_results,fp) 


#allModels_results = allModelPredictions(fiveParEst)
#with open('/home/pjrice/gp/ACTR-WM/data/parEstResults/Powell/bounded/fivePar/allModels_results.json', 'w') as fp: json.dump(allModels_results,fp) 
