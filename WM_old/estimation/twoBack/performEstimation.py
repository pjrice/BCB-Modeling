#  two-back model estimation

import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '/home/pjrice/gp/ACTR-WM/code/estimation/twoBack')
from modelEstimationFunctions import *

import os
import json

#results,badSubjs = estPars_byPart('/home/pjrice/gp/ACTR-WM/')
#with open('/home/pjrice/gp/ACTR-WM/data/parEstResults/twoBack/initalEstimations.json', 'w') as fp: 
#    json.dump(results,fp)
    
    
#with open('/home/pjrice/gp/ACTR-WM/data/parEstResults/twoBack/initalEstimations.json', 'r') as fp:
#    results = json.load(fp)

#resultsExp = expandEstResults_bootstrap(results)
#with open('/home/pjrice/gp/ACTR-WM/data/parEstResults/twoBack/parEst_exp.json', 'w') as fp: 
#    json.dump(resultsExp,fp)


with open('/home/pjrice/gp/ACTR-WM/data/parEstResults/twoBack/parEst_exp.json', 'r') as fp:
    resultsExp = json.load(fp)
    
dLOO_results = parameterVarExp_dLOO(resultsExp)
with open('/home/pjrice/gp/ACTR-WM/data/parEstResults/twoBack/dLOO_results.json', 'w') as fp: 
    json.dump(dLOO_results,fp) 