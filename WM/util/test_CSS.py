import os
import actr
import csv
import numpy as np
import matplotlib.pyplot as plt
#from noisyopt import minimizeCompass
from scipy.optimize import minimize
from scipy.stats import zscore

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]  

def read_correct_responses (fName):
    outList = list()
    with open(fName) as csvfile:
        fReader = csv.reader(csvfile)
        for row in fReader:
            outList.append(row)
    return(outList)

def read_participant_data (fName):
    outList = list()
    with open(fName) as csvfile:
        fReader = csv.reader(csvfile)
        for row in fReader:
            outList.append(row)
    outList = [x if x[0] != '' else [None,None,x[2]] for x in outList]
    return(outList)

def compute_acc (correctResponses,responses):
    
    #remove RTs from responses
    responses = [[x[0],x[2]] for x in responses]
    
    #calculate total accuracy
    totAcc_CR = [x[0] for x in correctResponses]
    totAcc_SR = [x[0] for x in responses]
    totAccVec = [1 if i==j else 0 for i,j in zip(totAcc_CR,totAcc_SR)]
    
    #calculate target accuracy
    tarAcc_CR = [x[0] for x in correctResponses if x[1]=='target']
    tarAcc_SR = [x[0] for x in responses if x[1]=='target']
    tarAccVec = [1 if i==j else 0 for i,j in zip(tarAcc_CR,tarAcc_SR)]
    
    #calculate lure accuracy
    lurAcc_CR = [x[0] for x in correctResponses if x[1]=='lure']
    lurAcc_SR = [x[0] for x in responses if x[1]=='lure']
    lurAccVec = [1 if i==j else 0 for i,j in zip(lurAcc_CR,lurAcc_SR)]
    
    #calculate nonlure accuracy
    nlrAcc_CR = [x[0] for x in correctResponses if x[1]=='nonlure']
    nlrAcc_SR = [x[0] for x in responses if x[1]=='nonlure']
    nlrAccVec = [1 if i==j else 0 for i,j in zip(nlrAcc_CR,nlrAcc_SR)]
    
    
    return([totAccVec, tarAccVec, lurAccVec, nlrAccVec])

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

def runTask (css, mas, ga, ia):
    
    stimTiming = create_stim_timing()
    
    actr.load_act_r_model("Z:\gp\ACTR-WM\code\models\zeroBack\zeroBack-model-main.lisp")
    #actr.load_act_r_model("/home/pjrice/gp/ACTR-WM/code/models/zeroBack/zeroBack-model-main.lisp")
    
    
    actr.call_command('set-similarities', ['cue', 'stimulus', css])
    
    #set parameters in process of being estimated
    #actr.set_parameter_value(":lf", lf)
    #actr.set_parameter_value(":egs", egs)
    
    actr.set_parameter_value(":mas", mas)
    actr.set_parameter_value(":ga", ga)
    actr.set_parameter_value(":imaginal-activation", ia)
        
    #run the task
    actr.call_command('runTaskFromPython')
    
    tempModelResponses = actr.call_command('print-resp')
    tempModelResponses.reverse()
    
    tempResponses = [x[0] for x in tempModelResponses]
    tempRTs = [x[1] for x in tempModelResponses]
    #clean up responses/RTs into list of lists
    modelRespTimes = [round((i-j),3) if i is not None else i for i,j in zip(tempRTs,stimTiming.tolist())]
    modelResponses = [[i,j] for i,j in zip(tempResponses,modelRespTimes)]
    
    return(modelResponses)

def check_parVal_4part (css, mas, ga, ia):
    
    #correctResponses = read_correct_responses("/home/pjrice/gp/ACTR-WM/data/zeroBack_correctResponses.csv")
    correctResponses = read_correct_responses("Z:\gp\ACTR-WM\data\zeroBack_correctResponses.csv")
    targetTypes = [x[1] for x in correctResponses]

    #subjResponses = read_participant_data('/home/pjrice/gp/ACTR-WM/data/beh/zb/'+part+'/zbResp.csv')
    subjResponses = read_participant_data('Z:\gp\ACTR-WM\data\sub-100307\zb_testResponses.csv')
    
    tempModelResponses = runTask(css,mas,ga,ia)
    modelResponses = [[i[0],i[1],j] for i,j in zip(tempModelResponses,targetTypes)]
    
    #modelAcc = np.mean(compute_acc(correctResponses, [x[0] for x in modelResponses]))
    #partAcc = np.mean(compute_acc(correctResponses, [x[0] for x in subjResponses]))
    
    [model_totAcc,model_tarAcc,model_lurAcc,model_nlrAcc] = compute_acc(correctResponses,modelResponses)
    [part_totAcc,part_tarAcc,part_lurAcc,part_nlrAcc] = compute_acc(correctResponses,subjResponses)
    
    results = dict(totAcc=dict(model=np.mean(model_totAcc),part=np.mean(part_totAcc)),
                   tarAcc=dict(model=np.mean(model_tarAcc),part=np.mean(part_tarAcc)),
                   lurAcc=dict(model=np.mean(model_lurAcc),part=np.mean(part_lurAcc)),
                   nlrAcc=dict(model=np.mean(model_nlrAcc),part=np.mean(part_nlrAcc)))
    
    blocks = range(1,9)
    
    modelAcc_byBlock = [np.mean(x) for x in chunks(model_totAcc,10)]
    partAcc_byBlock = [np.mean(x) for x in chunks(part_totAcc,10)]
    
    fig, ax = plt.subplots(figsize=(12,6))
    
    ax.plot(modelAcc_byBlock, color='blue', label='model')
    ax.plot(partAcc_byBlock, color='black', label='part')
    ax.legend()
    
    plt.ylim(0,1.1)
    plt.title('Model and participant accuracies by block')
    
    plt.show()
    
    return(results)

    
    

actr.load_act_r_code("Z:\gp\ACTR-WM\code\models\zeroBack\zeroBack-device.lisp")
#actr.load_act_r_code("/home/pjrice/gp/ACTR-WM/code/devices/zeroBack-device.lisp")