# script to estimate parameters of an ACT-R model
#
# Estimating the following parameters:
#
#   Declarative:
#   - cue-stimulus similarity:   The similarity between the cue and stimulus chunks. By default,
#                                the range is from 0 to -1 with 0 being the most similar and -1 
#                                being the largest difference.
#
#   - latency factor (:lf):      The latency factor value, F, in the equation for retrieval times. 
#                                It can be set to any non-negative value and defaults to 1.0.
#
#   - activation noise s (:ans): Specifies the s value used to generate the instantaneous noise added
#                                to the activation equation if it is set to a positive number Recommended 
#                                values for the noise parameter are in the range [.2,.8].
#
#
#   Imaginal:
#   - (:imaginal-activation):    Amount of spreading activation from imaginal buffer.
#
#   - (:imaginal-delay):         Controls how long it takes a request or modification request 
#                                to the imaginal buffer to complete
#   
#   Utility:
#   - expected gain s (:egs):    Specifies the s parameter for the noise added to the utility values.
#
#
# Setting the following static parameters:
#
#   - max. assoc. str. s (:mas): Controls whether the spreading activation calculation is used, 
#                                and if so, what the S value in the Sji calculations will be
#
#   Productions:
#   - response production utility values

nModelIterations = 10

import actr
import csv
import numpy as np
from noisyopt import minimizeCompass
from scipy.optimize import minimize
from scipy.stats import zscore
        
def read_response_data (fName):
    outList = list()
    with open(fName) as csvfile:
        fReader = csv.reader(csvfile)
        for row in fReader:
            outList.append(row)
    return(outList)
        
        
def test_model ():
    actr.load_act_r_code("Z:\gp\ACTR-WM\code\devices\zeroBack-device.lisp")
    actr.call_command('test-model')
    actr.call_command('print-resp')
    
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

def runTask (cueStimSim, lf, ans, imgAct, egs):
    
    actr.load_act_r_model("Z:\gp\ACTR-WM\code\models\zeroBack\zeroBack-model-main.lisp")
    
    #set static parameters
    actr.call_command('spp', ['compare-retrieval-match', ':u', 0.1])
    actr.call_command('spp', ['compare-retrieval-mismatch', ':u', 0.1])
    actr.call_command('spp', ['compare-retrieval-mistaken-match', ':u', -0.1])
    actr.call_command('spp', ['compare-retrieval-mistaken-mismatch', ':u', -0.1])
    actr.set_parameter_value(":mas", 10) #set this directly to a very high value (maybe 10)
    actr.set_parameter_value(":imaginal-delay", 0.2) #currently set to the default
    
    #set parameters in process of being estimated
    actr.call_command('set-similarities', ['cue', 'stimulus', cueStimSim])
    actr.set_parameter_value(":lf", lf)
    actr.set_parameter_value(":ans", ans)
    actr.set_parameter_value(":imaginal-activation", imgAct)
    #actr.set_parameter_value(":imaginal-delay", imgDelay)
    actr.set_parameter_value(":egs", egs)
        
    #run the task
    actr.call_command('runTaskFromPython')
    
def compute_rmse (cueStimSim, lf, ans, imgAct, egs):
    
    global stimTiming
    
    #run the model with the specified parameter values
    runTask(cueStimSim, lf, ans, imgAct, egs)
    
    #get the model's responses and RTs
    tempModelResponses = actr.call_command('print-resp')
    
    #get the model responses and RTs, have to reverse the list
    tempResponses = [x[0] for x in tempModelResponses]
    tempResponses.reverse()
    tempRTs = [x[1] for x in tempModelResponses]
    tempRTs.reverse()
    
    #clean up responses/RTs into list of lists
    modelRespTimes = [round((i-j),3) if i is not None else i for i,j in zip(tempRTs,stimTiming.tolist())]
    modelResponses = [[i,j] for i,j in zip(tempResponses,modelRespTimes)]
    
    #get the participant's responses/RTs
    subjResponses = read_response_data("Z:\gp\ACTR-WM\data\sub-100307\zb_testResponses.csv")
    subjResponses = [x if x[0] != '' else [None,None] for x in subjResponses]
    
    #get model and participant RTs
    modelRTs = np.array([x[1] for x in modelResponses], dtype=np.float)
    subjRTs = np.array([float(x[1]) if x[1] is not None else None for x in subjResponses], dtype=np.float)
    
    #get model and participant accuracy
    correctResponses = read_response_data("Z:\gp\ACTR-WM\data\zeroBack_correctResponses.csv")
    correctResponses = [x[0] for x in correctResponses]
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


def compute_mean_rmse(cueStimSim, lf, ans, imgAct, egs):
    
    global nModelIterations
        
    print(cueStimSim)
    print(lf)
    print(ans)
    print(imgAct)
    print(egs)
    
    rmses = list()
    for i in range(nModelIterations):
        #print(i)
        rmses.append(compute_rmse(cueStimSim, lf, ans, imgAct, egs))
    
    meanRMSE = np.mean(rmses)
    print(meanRMSE)
    return(meanRMSE)
    
    
def target_func(x):
    return(compute_mean_rmse(x[0],  # similarity of cue and stimulus chunks
                             x[1],  # :lf
                             x[2],  # :ans
                             x[3],  # :imaginal-activation
                             x[4])) # :egs


def target_func2(x):
    return(compute_rmse(x[0],  # similarity of cue and stimulus chunks
                             x[1],  # :lf
                             x[2],  # :ans
                             x[3],  # :imaginal-activation
                             x[4])) # :egs



stimTiming = create_stim_timing()
actr.load_act_r_code("Z:\gp\ACTR-WM\code\devices\zeroBack-device.lisp")


init = np.array([-0.001, 0.7, 0.5, 1.0, 0.1])
bounds = [(-1,0), (0.05,1.1), (0.2,0.8), (0,2), (0,1)]

#minimize(target_func2, init, method = "Nelder-Mead", options = {"maxiter" : 2000})
#minimize(target_func2, init, method = "L-BFGS-B", bounds = bounds, options = {"maxiter" : 5})
#minimizeCompass(target_func2, bounds=bounds, x0=init, deltatol=0.1, paired=False, disp=True)
#minimizeCompass(target_func2, bounds=bounds, x0=init, deltatol=0.01, errorcontrol=False, paired=False, disp=True)
    

def printParamEstimates(paramEsts):
    params = ['cueStimSim           = ', ':lf                  = ', ':ans                 = ', ':imaginal-activation = ', ':imaginal-delay      = ', ':egs                 = ']
    for i in range(len(paramEsts)):
        print(params[i] + '{:f}'.format(paramEsts[i]))



def testParams (paramEsts):
    
    actr.load_act_r_model("Z:\gp\ACTR-WM\code\models\zeroBack\zeroBack-model-main.lisp")
    
    #set static parameters
    actr.call_command('spp', ['compare-retrieval-match', ':u', 0.1])
    actr.call_command('spp', ['compare-retrieval-mismatch', ':u', 0.1])
    actr.call_command('spp', ['compare-retrieval-mistaken-match', ':u', -0.1])
    actr.call_command('spp', ['compare-retrieval-mistaken-mismatch', ':u', -0.1])
    actr.set_parameter_value(":mas", 10) #set this directly to a very high value (maybe 10)
    
    #set parameters in process of being estimated
    actr.call_command('set-similarities', ['cue', 'stimulus', paramEsts[0]])
    actr.set_parameter_value(":lf", paramEsts[1])
    actr.set_parameter_value(":ans", paramEsts[2])
    actr.set_parameter_value(":imaginal-activation", paramEsts[3])
    actr.set_parameter_value(":imaginal-delay", paramEsts[4])
    actr.set_parameter_value(":egs", paramEsts[5])
    
    actr.call_command('runTaskFromPython')
    
    tempModelResponses = actr.call_command('print-resp')
    
    stimTiming = create_stim_timing()
    
    tempResponses = [x[0] for x in tempModelResponses]
    tempResponses.reverse()
    tempRTs = [x[1] for x in tempModelResponses]
    tempRTs.reverse()
    
    modelRespTimes = [round((i-j),3) if i is not None else i for i,j in zip(tempRTs,stimTiming.tolist())]
    modelResponses = [[i,j] for i,j in zip(tempResponses,modelRespTimes)]
    
    correctResponses = read_response_data("Z:\gp\ACTR-WM\data\zeroBack_correctResponses.csv")
    correctResponses = [x[0] for x in correctResponses]
    modelAcc = compute_acc(correctResponses, [x[0] for x in modelResponses])
    
    print('Model Accuracy: ' + str(np.mean(modelAcc)))
    print('Model meanRT:   ' + str(np.mean(modelRespTimes)))















































    
    
    