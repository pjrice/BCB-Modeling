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

def runTask (lf):
    
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
    actr.call_command('set-similarities', ['cue', 'stimulus', 0])
    
    #set parameters in process of being estimated
    actr.set_parameter_value(":lf", lf)
    #actr.set_parameter_value(":egs", egs)
        
    #run the task
    actr.call_command('runTaskFromPython')
    
    modelResponses = actr.call_command('print-resp')
    modelResponses.reverse()
    
    return(modelResponses)
    

def compute_rmse (lf, stimTiming, correctResponses, subjResponses):
    
    #global stimTiming
    
    #run the model with the specified parameter values
    tempModelResponses = runTask(lf)
    
    #get the model's responses and RTs
    #tempModelResponses = actr.call_command('print-resp')
    
    #get the model responses and RTs, have to reverse the list
    tempResponses = [x[0] for x in tempModelResponses]
    tempRTs = [x[1] for x in tempModelResponses]
    
    #clean up responses/RTs into list of lists
    modelRespTimes = [round((i-j),3) if i is not None else i for i,j in zip(tempRTs,stimTiming.tolist())]
    modelResponses = [[i,j] for i,j in zip(tempResponses,modelRespTimes)]
    
    #get model and participant RTs
    modelRTs = np.array([x[1] for x in modelResponses], dtype=np.float)
    subjRTs = np.array([float(x[1]) if x[1] is not None else None for x in subjResponses], dtype=np.float)
    
    #get model and participant accuracy
    modelAcc = compute_acc(correctResponses, [x[0] for x in modelResponses])
    subjAcc = compute_acc(correctResponses, [x[0] for x in subjResponses])
    
    #standardize subject and model RTs
    norm_subjModelRTs = zscore_wrt(subjRTs,modelRTs)
    normSubjRTs = norm_subjModelRTs[0]
    normModelRTs = norm_subjModelRTs[1]
    
    #standardize subject and model RTs
    norm_subjModelAcc = zscore_wrt(subjAcc,modelAcc)
    normSubjAcc = norm_subjModelAcc[0]
    normModelAcc = norm_subjModelAcc[1]
    
    #create singleton vectors of combined responses/RTs for model and participant
    normSubjResponses = np.array([val for pair in zip(normSubjAcc,normSubjRTs) for val in pair], dtype=np.float)
    normModelResponses = np.array([val for pair in zip(normModelAcc,normModelRTs) for val in pair], dtype=np.float)
    
    #replace NaNs with a large (normalized) value - NaNs occur where either the model or participant did not respond
    np.nan_to_num(normModelResponses,copy=False,nan=10)
    np.nan_to_num(normSubjResponses,copy=False,nan=10)
    
    #compute rmse
    RMSE = np.sqrt(np.mean((normSubjResponses-normModelResponses)**2))
    
    return(RMSE)

def objective_func (x, stimTiming, correctResponses, subjResponses):
    return(compute_rmse(x[0], stimTiming, correctResponses, subjResponses))


#actr.load_act_r_code("Z:\gp\ACTR-WM\code\devices\zeroBack-device.lisp")
#actr.load_act_r_code("/home/pjrice/gp/ACTR-WM/code/devices/zeroBack-device.lisp")


#minimize(objective_func, x0=init, args=(stimTiming), method = "Nelder-Mead", options = {"maxiter" : 200})
#minimize(objective_func, x0=init, method = "L-BFGS-B", options = {"maxiter" : 25})
#minimizeCompass(objective_func, bounds=bounds, x0=init, deltatol=0.1, errorcontrol=False, paired=False, disp=True)

def estPars_byPart (rootDataDir):
    
    stimTiming = create_stim_timing()
    correctResponses = read_correct_responses("/home/pjrice/gp/ACTR-WM/data/zeroBack_correctResponses.csv")
    
    partList = os.listdir(rootDataDir)
    
    init = [0.7]
    #bounds = [(0.01, 1.5)]
    
    actr.load_act_r_code("/home/pjrice/gp/ACTR-WM/code/devices/zeroBack-device.lisp")
    
    results = dict(parts=list(), lfVals=list(), RMSEs=list(), modelAcc=list(), partAcc=list(), modelmRT=list(), partmRT=list())
    for part in partList:
        
        print(part)
        
        subjResponses = read_participant_data('/home/pjrice/gp/ACTR-WM/data/beh/zb/'+part+'/zbResp.csv')
        
        parEst = minimize(objective_func, x0=init, args=(stimTiming, correctResponses, subjResponses), method = "Nelder-Mead", options = {"maxiter" : 200})
        
        tempModelResponses = runTask(parEst.x[0])
        tempResponses = [x[0] for x in tempModelResponses]
        tempRTs = [x[1] for x in tempModelResponses]
        #clean up responses/RTs into list of lists
        modelRespTimes = [round((i-j),3) if i is not None else i for i,j in zip(tempRTs,stimTiming.tolist())]
        modelResponses = [[i,j] for i,j in zip(tempResponses,modelRespTimes)]
        
        results['parts'].append(part)
        results['lfVals'].append(parEst.x[0])
        results['RMSEs'].append(parEst.fun)
        results['modelAcc'].append(np.mean(compute_acc(correctResponses, [x[0] for x in modelResponses])))
        results['partAcc'].append(np.mean(compute_acc(correctResponses, [x[0] for x in subjResponses])))
        results['modelmRT'].append(np.nanmean(np.array([x[1] for x in modelResponses], dtype=np.float)))
        results['partmRT'].append(np.nanmean(np.array([float(x[1]) if x[1] is not None else None for x in subjResponses], dtype=np.float)))
        
    return(results)
    
    
def check_parVal_4part (lf, part):
    
    stimTiming = create_stim_timing()
    correctResponses = read_correct_responses("/home/pjrice/gp/ACTR-WM/data/zeroBack_correctResponses.csv")
    
    results = dict(lfVals=list(), RMSEs=list(), modelAcc=list(), partAcc=list(), modelmRT=list(), partmRT=list())
    
    subjResponses = read_participant_data('/home/pjrice/gp/ACTR-WM/data/beh/zb/'+part+'/zbResp.csv')
    
    tempModelResponses = runTask(lf)
    tempResponses = [x[0] for x in tempModelResponses]
    tempRTs = [x[1] for x in tempModelResponses]
    #clean up responses/RTs into list of lists
    modelRespTimes = [round((i-j),3) if i is not None else i for i,j in zip(tempRTs,stimTiming.tolist())]
    modelResponses = [[i,j] for i,j in zip(tempResponses,modelRespTimes)]
    
    rmse = compute_rmse(lf, stimTiming, correctResponses, subjResponses)
    
    results['lfVals'].append(lf)
    results['RMSEs'].append(rmse)
    results['modelAcc'].append(np.mean(compute_acc(correctResponses, [x[0] for x in modelResponses])))
    results['partAcc'].append(np.mean(compute_acc(correctResponses, [x[0] for x in subjResponses])))
    results['modelmRT'].append(np.nanmean(np.array([x[1] for x in modelResponses], dtype=np.float)))
    results['partmRT'].append(np.nanmean(np.array([float(x[1]) if x[1] is not None else None for x in subjResponses], dtype=np.float)))
    
    return(results)
    
    
    
    
def makeplots(results):
    
    n, bins, patches = plt.hist(results['lfVals'])
    plt.xlim(0,3.5)
    plt.xlabel(':lf estimated value')
    plt.ylabel('Frequency')
    plt.title(':lf histogram - RT+Acc')
    plt.show()
    
    test = [x for x in results['RMSEs'] if not math.isinf(x)]
    n, bins, patches = plt.hist(test)
    plt.xlabel('RMSE')
    plt.ylabel('Frequency')
    plt.title('RMSE histogram - RT+Acc')
    plt.show()
    
    n, bins, patches = plt.hist(results['modelAcc'])
    plt.xlabel('Model Accuracies')
    plt.ylabel('Frequency')
    plt.title('Model Accuracy histogram - RT+Acc')
    plt.show()
    
    n, bins, patches = plt.hist(results['partAcc'])
    plt.xlabel('Participant Accuracies')
    plt.ylabel('Frequency')
    plt.title('Participant Accuracy histogram')
    plt.show()
    
    n, bins, patches = plt.hist(results['modelmRT'])
    plt.xlabel('Model mean RT')
    plt.ylabel('Frequency')
    plt.title('Model mean RT histogram - RT+Acc')
    plt.show()
    
    n, bins, patches = plt.hist(results['partmRT'])
    plt.xlabel('Participant mean RT')
    plt.ylabel('Frequency')
    plt.title('Participant mean RT histogram')
    plt.show()
    
    n, bins, patches = plt.hist([i-j for i,j in zip(results['partmRT'],results['modelmRT'])])
    plt.xlabel('Difference in mean RTs')
    plt.ylabel('Frequency')
    plt.title('Difference between participant mean RTs and model mean RTs - RT+Acc')
    plt.show()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    