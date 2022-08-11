import os
import csv
import numpy as np

os.chdir('/home/ausmanpa/actr7.x/tutorial/python')
import actr

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


def getModelPreds(numRuns):
    
    # load the device
    actr.load_act_r_code('/home/ausmanpa/gp/BCB-Modeling/WM_ABCest/model/zeroBack-device.lisp')
    
    # establish the "correct" chunk to retrieve on each trial
    correctCueChunks = np.array(['CUE0-0','CUE1-0','CUE2-0','CUE3-0','CUE4-0','CUE5-0','CUE6-0','CUE7-0'])
    correctCueChunks = np.repeat(correctCueChunks,10,axis=0).tolist()
    
    # get the correct keypresses and trial types
    correctRespTTs = []
    with open('/home/ausmanpa/gp/BCB-Modeling/WM_ABCest/model/zeroBack_correctResponses.csv',newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            correctRespTTs.append(row)
    
    correct_kps = [i[0] for i in correctRespTTs]
    trialTypes = [i[1] for i in correctRespTTs]
    
    # create the stimulus timing for the zero-back condition
    stimTiming = create_stim_timing()
    
    # establish "participants" to test
    # only vary goal buffer spreading activation; set all other values to mean
    # of values estimated across participants
    gaVals = np.random.normal(0.93,0.33,numRuns)
    ia = 0.69
    bll = 0.52
    lf = 2.49
    css = -0.43
    
    resultsDict = {}
    runNum = 1
    for ga in gaVals:
                
        # load the zero-back ACT-R model
        actr.load_act_r_model('/home/ausmanpa/gp/BCB-Modeling/WM_ABCest/model/zeroBack-model-main.lisp')
        
        # set parameters in process of being estimated
        actr.call_command('set-similarities', ['cue', 'stimulus', css])
        actr.set_parameter_value(':ga', ga)
        actr.set_parameter_value(':imaginal-activation', ia)
        actr.set_parameter_value(':lf', lf)
        actr.set_parameter_value(':bll', bll)
        
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
        
        # compute accuracies
        accVec = compute_model_acc(correctCueChunks,chunkRetrievals)
        print('Model accuracy: '+str(np.mean(accVec)))
        
        kpAcc = compute_kp_acc(keypresses,correct_kps)
        
        runResults = {}
        runResults['gaVal'] = ga
        runResults['trialTypes'] = trialTypes
        runResults['RTs'] = modelRespTimes
        runResults['Keypresses'] = keypresses
        runResults['kpAcc'] = kpAcc
        runResults['Retrievals'] = chunkRetrievals
        runResults['retAcc'] = accVec
        
        resultsDict['Run'+str(runNum)] = runResults
        
        runNum += 1
    
    return(resultsDict)


def writeResults2csv(resultsDict,savePath):
    
    results2write = [['runNum','gaVal','tNum','tType','rt','kp','kpAcc','ret','retAcc']]
    for runNum in list(resultsDict.keys()):
        gaVal = resultsDict[runNum]['gaVal']
        trialTypes = resultsDict[runNum]['trialTypes']
        rts = resultsDict[runNum]['RTs']
        kps = resultsDict[runNum]['Keypresses']
        kpAcc = resultsDict[runNum]['kpAcc']
        ret = resultsDict[runNum]['Retrievals']
        retAcc = resultsDict[runNum]['retAcc']
        
        tNum = range(1,len(resultsDict[runNum]['RTs'])+1)
        
        runResults = [[runNum,gaVal,tNum[i],trialTypes[i],rts[i],kps[i],kpAcc[i],ret[i],retAcc[i]] for i in range(0,len(tNum))]
        
        for tResult in runResults:
            results2write.append(tResult)
            
    with open(savePath,'w',newline='') as f:
        writer = csv.writer(f)
        writer.writerows(results2write)
            
    
        
        
        
    
        
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    