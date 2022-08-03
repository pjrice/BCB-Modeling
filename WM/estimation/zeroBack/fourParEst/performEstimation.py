# ***FOUR*** parameter zero-back model estimation


import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '/home/pjrice/gp/ACTR-WM/code/estimation/zeroBack/fourParEst')
from modelEstimationFunctions import *

import os
import json

results,badSubjs = estPars_byPart('/home/pjrice/gp/ACTR-WM/')

resultsExp = expandEstResults_bootstrap(results)
with open('/home/pjrice/gp/ACTR-WM/data/parEstResults/Powell/bounded/fourPar/fourPar_staticCSS.json', 'w') as fp: 
    json.dump(resultsExp,fp)


#subjMeasures,modelPredictions = parameterVarExp(fourParEst)
#modelMSEs_perPart = parameterVarExp_perPart(test)
#with open('/home/pjrice/gp/ACTR-WM/data/parEstResults/Powell/bounded/fourPar/subjMeasures.json', 'w') as fp: json.dump(subjMeasures,fp)    
#with open('/home/pjrice/gp/ACTR-WM/data/parEstResults/Powell/bounded/fourPar/modelPredictions.json', 'w') as fp: json.dump(modelPredictions,fp)

corrResults = parameterVarExp(fourParEst)
with open('/home/pjrice/gp/ACTR-WM/data/parEstResults/Powell/bounded/fourPar/group_and_perPar_corrData.json', 'w') as fp: json.dump(corrResults,fp) 