#estimating lf only


# cd /home/pjrice/Downloads/ACT-R/tutorial/python

import os
import actr
import csv
import numpy as np
import matplotlib.pyplot as plt
#from noisyopt import minimizeCompass
from scipy.optimize import minimize
from scipy.stats import zscore

def read_correct_responses (fName):
    outList = list()
    with open(fName) as csvfile:
        fReader = csv.reader(csvfile)
        for row in fReader:
            outList.append(row)
    outList = [x[0] for x in outList]
    return(outList)

def read_participant_data (fName):
    outList = list()
    with open(fName) as csvfile:
        fReader = csv.reader(csvfile)
        for row in fReader:
            outList.append(row)
    outList = [x if x[0] != '' else [None,None] for x in outList]
    return(outList)

def compute_acc (correctResponses,responses):
    
    accVec = [1 if i==j else 0 for i,j in zip(correctResponses,responses)]
    return(accVec)

def zscore_wrt (signal1, signal2):
    """zscores signal 1, and zscores signal 2 with respect to signal 1 (that is, uses signal1's mean/std to zscore signal2)."""
    
    normSig1 = zscore(signal1, nan_policy='omit')
    
    meanSig1 = np.nanmean(signal1)
    stdSig1 = np.nanstd(signal1)
    
    normSig2 = (signal2 - meanSig1)/stdSig1
    
    return(normSig1,normSig2)

def create_stim_timing():
    
    #timing of the first block of stimuli ("base timing")
    firstBlock = [round(x,2) for x in np.arange(2.5,27.5,2.5)]
    firstBlock = np.arange(2.5,27.5,2.5)
    #the timing of the second block is the time of the last stim of the first
    #block, plus the cue time (2.5), added to the base timing
    secondBlock = firstBlock[-1]+2.5+firstBlock
    
    #the timing of the third block is the time of the last stim of the second
    #block, plus the fix time (15), plus the cue time (2.5), added to the 
    #base timing
    thirdBlock = secondBlock[-1]+15+2.5+firstBlock
    
    #the timing of the fourth block is the time of the last stim of the third
    #block, plus the cue time (2.5), added to the base timing
    fourthBlock = thirdBlock[-1]+2.5+firstBlock
    
    ses1Timing = np.concatenate((firstBlock,secondBlock,thirdBlock,fourthBlock),axis=None)
    
    
    ses2Timing = ses1Timing[-1]+15+2.5+ses1Timing
    
    stimTiming = np.concatenate((ses1Timing,ses2Timing), axis=None)
    
    return(stimTiming)

def runTask (egs):
    
    #actr.load_act_r_model("Z:\gp\ACTR-WM\code\models\zeroBack\zeroBack-model-main.lisp")
    actr.load_act_r_model("/home/pjrice/gp/ACTR-WM/code/models/zeroBack/zeroBack-model-main.lisp")
    
    #set static parameters
    actr.call_command('spp', ['compare-retrieval-match', ':u', 0.1])
    actr.call_command('spp', ['compare-retrieval-mismatch', ':u', 0.1])
    actr.call_command('spp', ['compare-retrieval-mistaken-match', ':u', -0.1])
    actr.call_command('spp', ['compare-retrieval-mistaken-mismatch', ':u', -0.1])
    #actr.set_parameter_value(":mas", 10) #set this directly to a very high value (maybe 10)
    #actr.set_parameter_value(":imaginal-delay", 0.2) #currently set to the default
    #actr.set_parameter_value(":egs", 0.01)
    
    
    #set parameters in process of being estimated
    actr.set_parameter_value(":egs", egs)
        
    #run the task
    actr.call_command('runTaskFromPython')
    
    modelResponses = actr.call_command('print-resp')
    modelResponses.reverse()
    
    return(modelResponses)
    

def compute_lle (egs, subjResponses, nModelRuns):
    
    #global stimTiming
    
    #run the model with the specified parameter values
    tempModelResponses = runTask(egs)
    
    #modelResponsesList will be a list nModelRuns long with the responses of each model run in sublists
    #but will then be reshaped
    modelResponsesList = list()
    for n in range(nModelRuns):
        temp = runTask(egs)
        tempModelResponses = [x[0] for x in temp]
        modelResponsesList.append(tempModelResponses)
    
    #after this, modelResponsesList will contain a number of lists with the response of the model from each run
    #so, the first list contains the first response of the model across the runs, the second list the second response, and so on
    modelResponsesList = [list(x) for x in zip(*modelResponsesList)]
    
    probsList = list()
    for n in range(len(modelResponsesList)):
        
        subjResp = subjResponses[n][0]
        modelRespList = modelResponsesList[n]
        
        modelCopyProb = np.mean([1 if subjResp==x else 0 for x in modelRespList])
        probsList.append(modelCopyProb)
    
    probsList = [x if x!=0.0 else 0.00001 for x in probsList]
    
    LLE = np.sum(np.log(probsList))
    LLE = -1 * LLE
            
    return(LLE)

def objective_func (x, subjResponses, nModelRuns):
    return(compute_lle(x[0], subjResponses, nModelRuns))


#actr.load_act_r_code("Z:\gp\ACTR-WM\code\devices\zeroBack-device.lisp")
#actr.load_act_r_code("/home/pjrice/gp/ACTR-WM/code/devices/zeroBack-device.lisp")


#minimize(objective_func, x0=init, args=(stimTiming), method = "Nelder-Mead", options = {"maxiter" : 200})
#minimize(objective_func, x0=init, method = "L-BFGS-B", options = {"maxiter" : 25})
#minimizeCompass(objective_func, bounds=bounds, x0=init, deltatol=0.1, errorcontrol=False, paired=False, disp=True)

def estPars_byPart (rootDataDir):
    
    stimTiming = create_stim_timing()
    correctResponses = read_correct_responses("/home/pjrice/gp/ACTR-WM/data/zeroBack_correctResponses.csv")
    
    partList = os.listdir(rootDataDir)
    
    nModelRuns = 10
    
    init = [0.1]
    #bounds = [(0.01, 1.5)]
    
    actr.load_act_r_code("/home/pjrice/gp/ACTR-WM/code/devices/zeroBack-device.lisp")
    
    results = dict(parts=list(), egsVals=list(), RMSEs=list(), modelAcc=list(), partAcc=list(), modelmRT=list(), partmRT=list())
    for part in partList:
        
        print(part)
        
        subjResponses = read_participant_data('/home/pjrice/gp/ACTR-WM/data/beh/zb/'+part+'/zbResp.csv')
        
        parEst = minimize(objective_func, x0=init, args=(subjResponses, nModelRuns), method = "Nelder-Mead", options = {"maxiter" : 200})
        
        tempModelResponses = runTask(parEst.x[0])
        tempResponses = [x[0] for x in tempModelResponses]
        tempRTs = [x[1] for x in tempModelResponses]
        #clean up responses/RTs into list of lists
        modelRespTimes = [round((i-j),3) if i is not None else i for i,j in zip(tempRTs,stimTiming.tolist())]
        modelResponses = [[i,j] for i,j in zip(tempResponses,modelRespTimes)]
        
        results['parts'].append(part)
        results['egsVals'].append(parEst.x[0])
        results['RMSEs'].append(parEst.fun)
        results['modelAcc'].append(np.mean(compute_acc(correctResponses, [x[0] for x in modelResponses])))
        results['partAcc'].append(np.mean(compute_acc(correctResponses, [x[0] for x in subjResponses])))
        results['modelmRT'].append(np.nanmean(np.array([x[1] for x in modelResponses], dtype=np.float)))
        results['partmRT'].append(np.nanmean(np.array([float(x[1]) if x[1] is not None else None for x in subjResponses], dtype=np.float)))
        
    return(results)
    
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    