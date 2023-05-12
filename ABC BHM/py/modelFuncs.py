import csv
import actr
import numpy as np


def create_stim_timing():
    
    # timing of the first block of stimuli ("base timing")
    firstBlock = np.arange(2.5,27.5,2.5)
    # the timing of the second block is the time of the last stim of the first
    # block, plus the cue time (2.5), added to the base timing
    secondBlock = firstBlock[-1]+2.5+firstBlock
    
    # the timing of the third block is the time of the last stim of the second
    # block, plus the fix time (15), plus the cue time (2.5), added to the 
    # base timing
    thirdBlock = secondBlock[-1]+15+2.5+firstBlock
    
    # the timing of the fourth block is the time of the last stim of the third
    # block, plus the cue time (2.5), added to the base timing
    fourthBlock = thirdBlock[-1]+2.5+firstBlock
    
    ses1Timing = np.concatenate((firstBlock,secondBlock,thirdBlock,fourthBlock),axis=None)
    
    # 86400 instead of 15 to account for day-long break between session 1 and 2
    ses2Timing = ses1Timing[-1]+86400+2.5+ses1Timing
    
    stimTiming = np.concatenate((ses1Timing,ses2Timing), axis=None)
    
    return(stimTiming)

def compute_model_acc (correctCueChunks,chunkRetrievals):
    
    compVec = zip(correctCueChunks,chunkRetrievals)
    
    #calculate trial-by-trial accuracy
    accVec = [1 if i==j else 0 for i,j in compVec]
    
    return(accVec)

def compute_kp_acc(kpResp,correctResp):
    compVec = zip(kpResp,correctResp)
    accVec = [1 if i==j else 0 for i,j in compVec]
    return(accVec)


def run_model_with_params(modelFile,paramDict):
    
    # establish the "correct" chunk to retrieve on each trial
    correctCueChunks = np.array(['CUE0-0','CUE1-0','CUE2-0','CUE3-0','CUE4-0','CUE5-0','CUE6-0','CUE7-0'])
    correctCueChunks = np.repeat(correctCueChunks,10,axis=0).tolist()
    
    # get the correct keypresses and trial types
    correctRespTTs = []
    with open('Z:\\gp\\BCB-Modeling\\WM_ABCest\\model\\zeroBack_correctResponses.csv',newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            correctRespTTs.append(row)
    
    correct_kps = [i[0] for i in correctRespTTs]
    #trialTypes = [i[1] for i in correctRespTTs]
    
    # create the stimulus timing for the zero-back condition
    stimTiming = create_stim_timing()
    
    # load the ACT-R model
    actr.load_act_r_model(modelFile)
    
    for param in paramDict.keys():
        if param == 'css':
            actr.call_command('set-similarities', ['cue', 'stimulus', paramDict[param]])
        else:
            actr.set_parameter_value(param,paramDict[param])
            
    # run the task
    actr.call_command('runTaskFromPython')
        
    # retrieve the responses
    modelResponses = actr.call_command('print-resp')
    modelResponses.reverse()
    
    # get model's keypress responses, RTs, and retrieved chunks
    tempRTs = [x[1] for x in modelResponses]
    keypresses = [x[0] for x in modelResponses]
    
    chunkRetrievals = [x[2] for x in modelResponses]
    
    # compute RTs by subtracting the timing of the stimuli
    modelRespTimes = [round((i-j),3) if i is not None else i for i,j in zip(tempRTs,stimTiming.tolist())]
    
    # the model may have failed to retrieve on some trial, and subsequently there is no response for the trial
    modelRespTimes = [0 if x is None else x for x in modelRespTimes]
    keypresses = [0 if x is None else x for x in keypresses]
    
    # compute accuracies
    accVec = compute_model_acc(correctCueChunks,chunkRetrievals)
    kpAcc = compute_kp_acc(keypresses,correct_kps)
    
    outDict = {'RTs':modelRespTimes, 'chunkAcc':accVec, 'keypressAcc':kpAcc}
    
    return outDict



        
#def compute_participant_measures():
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    