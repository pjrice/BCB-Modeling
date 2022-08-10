#trial-by-trial scaled RTs, targetType accuracies and block-by-block accuracies

import os
import actr
import csv
import json
import numpy as np
#from noisyopt import minimizeCompass
#from scipy.optimize import minimize
import scipy.optimize
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
    "Computes accuracy of the participant by comparing the participant's list of responses ('j'==nontarget; 'f'==target) to the list of correct responses"
    
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

def compute_model_acc (correctCueChunks,modelResponses):
    """Computes the accuracy of the model by determining if a cue chunk was retrieved or not.
       If the cue chunk was retrieved, there are no other sources of noise/error in the model 
       and so the response the model makes (whether the stimulus is target or nontarget) will
       be correct. However, if a stimulus chunk was retrieved, this is counted as incorrect
       (i.e., the "mind" made an error), even though the response may seem to be correct
       (such as in the case the stimulus chunk that was retrieved does not match the current 
        nontarget stimulus)"""
    
    #get chunk retrievals and target types from modelResponses
    responses = [[i,j[2],j[3]] for i,j in zip(correctCueChunks,modelResponses)]
    
    #calculate total accuracy
    totAccVec = [1 if x[0]==x[1] else 0 for x in responses]
    
    #calculate target accuracy
    tarAccVec = [1 if x[0]==x[1] else 0 for x in responses if x[2]=='target']
    
    #calculate lure accuracy
    lurAccVec = [1 if x[0]==x[1] else 0 for x in responses if x[2]=='lure']

    #calculate nonlure accuracy
    nlrAccVec = [1 if x[0]==x[1] else 0 for x in responses if x[2]=='nonlure']

    
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
    
    # 86400 instead of 15 to account for day-long break between session 1 and 2
    #ses2Timing = ses1Timing[-1]+15+2.5+ses1Timing
    ses2Timing = ses1Timing[-1]+86400+2.5+ses1Timing
    
    stimTiming = np.concatenate((ses1Timing,ses2Timing), axis=None)
    
    return(stimTiming)

def runTask (css, ga, ia, lf, bll, stimTiming):
        
    #actr.load_act_r_model("Z:\gp\ACTR-WM\code\models\zeroBack\zeroBack-model-main.lisp")
    actr.load_act_r_model("/home/pjrice/gp/ACTR-WM/code/models/zeroBack/zeroBack-model-main.lisp")
    
    #set parameters in process of being estimated
    actr.call_command('set-similarities', ['cue', 'stimulus', css])
    actr.set_parameter_value(":ga", ga)
    actr.set_parameter_value(":imaginal-activation", ia)
    actr.set_parameter_value(":lf", lf)
    actr.set_parameter_value(":bll", bll)    
    
    #run the task
    actr.call_command('runTaskFromPython')
    
    tempModelResponses = actr.call_command('print-resp')
    tempModelResponses.reverse()
    
    tempResponses = [x[0] for x in tempModelResponses]
    tempRTs = [x[1] for x in tempModelResponses]
    tempChunkRetrievals = [x[2] for x in tempModelResponses]
    #clean up responses/RTs into list of lists
    modelRespTimes = [round((i-j),3) if i is not None else i for i,j in zip(tempRTs,stimTiming.tolist())]
    modelResponses = [[i,j,k] for i,j,k in zip(tempResponses,modelRespTimes,tempChunkRetrievals)]
    
    return(modelResponses)

def compute_rmse(css, ga, ia, lf, bll, stimTiming, correctCueChunks, correctResponses, subjResponses, targetTypes):
    
    #run model, add targetTypes to model responses
    tempModelResponses = runTask(css, ga, ia, lf, bll, stimTiming)
    modelResponses = [[i[0],i[1],i[2],j] for i,j in zip(tempModelResponses,targetTypes)]
    
    #get model/participant RTs
    modelRTs = np.array([x[1] for x in modelResponses], dtype=np.float)
    subjRTs = np.array([x[1] for x in subjResponses], dtype=np.float)
    
    #replace nans (missing RTs) with mean RT
    np.nan_to_num(modelRTs, copy=False, nan=np.nanmean(modelRTs))
    np.nan_to_num(subjRTs, copy=False, nan=np.nanmean(subjRTs))
    
    #calculate model/participant target, lure, and nonlure accuracy vectors
    [model_totAccVec,model_tarAccVec,model_lurAccVec,model_nlrAccVec] = compute_model_acc(correctCueChunks,modelResponses)
    [subj_totAccVec,subj_tarAccVec,subj_lurAccVec,subj_nlrAccVec] = compute_acc(correctResponses,subjResponses)
    
    #calculate model/participant target, lure, and nonlure accuracy percentages
    model_tarAcc = np.mean(model_tarAccVec)
    model_lurAcc = np.mean(model_lurAccVec)
    model_nlrAcc = np.mean(model_nlrAccVec)
    
    subj_tarAcc = np.mean(subj_tarAccVec)
    subj_lurAcc = np.mean(subj_lurAccVec)
    subj_nlrAcc = np.mean(subj_nlrAccVec)
    
    #calculate block-by-block accuracies
    modelAcc_byBlock = np.array([np.mean(x) for x in chunks(model_totAccVec,10)], dtype=np.float)
    subjAcc_byBlock = np.array([np.mean(x) for x in chunks(subj_totAccVec,10)], dtype=np.float)
    
    #rescale RTs by dividing by max allowable RT (2 seconds)
    #RTs will now be on same scale as accuracy (bounded by (0,1))
    scaled_modelRTs = modelRTs/2
    scaled_subjRTs = subjRTs/2
    
    #create singleton vectors of combined scaled RTs and target/lure/nonlure accuracies for model and participant
    modelVec = np.concatenate((scaled_modelRTs,model_tarAcc,model_lurAcc,model_nlrAcc,modelAcc_byBlock), axis=None)
    subjVec = np.concatenate((scaled_subjRTs,subj_tarAcc,subj_lurAcc,subj_nlrAcc,subjAcc_byBlock), axis=None)
    
    #compute rmse
    rmse = np.sqrt(np.mean((subjVec - modelVec)**2))
    
    return(rmse)

# def objective_func (x, stimTiming, correctCueChunks, correctResponses, subjResponses, targetTypes):
#     return(compute_rmse(x[0], # css 
#                         x[1], # ga
#                         x[2], # ia
#                         x[3], # lf
#                         x[4], # bll
#                         stimTiming, correctCueChunks, correctResponses, subjResponses, targetTypes))

def objective_func (x, stimTiming, correctCueChunks, correctResponses, subjResponses, targetTypes):
    if x[4] > 1:
        return(10)
    else:
        return(compute_rmse(x[0], # css 
                        x[1], # ga
                        x[2], # ia
                        x[3], # lf
                        x[4], # bll
                        stimTiming, correctCueChunks, correctResponses, subjResponses, targetTypes))
    


#actr.load_act_r_code("Z:\gp\ACTR-WM\code\models\zeroBack\zeroBack-device.lisp")
#actr.load_act_r_code("/home/pjrice/gp/ACTR-WM/code/models/zeroBack/zeroBack-device.lisp")

#minimize(objective_func, x0=init, args=(stimTiming, correctResponses, subjResponses, targetTypes), method = "Nelder-Mead", options = {"maxiter" : 20})

def estPars_byPart (rootDataDir):
    
    actr.load_act_r_code("/home/pjrice/gp/ACTR-WM/code/models/zeroBack/zeroBack-device.lisp")
    
    correctCueChunks = np.array(['CUE0-0','CUE1-0','CUE2-0','CUE3-0','CUE4-0','CUE5-0','CUE6-0','CUE7-0'])
    correctCueChunks = np.repeat(correctCueChunks,10,axis=0).tolist()
    
    correctResponses = read_correct_responses("/home/pjrice/gp/ACTR-WM/data/zeroBack_correctResponses.csv")    
    targetTypes = [x[1] for x in correctResponses]    
    stimTiming = create_stim_timing()
    
    partList = os.listdir(rootDataDir)
    
    #badSubjs = ['sub-142828', 'sub-175035', 'sub-106319', 'sub-162329']
    
    #for subj in badSubjs:
    #    partList.remove(subj)
    
    init = [0, 1, 1, 2.25, 0.5]
    bnds = ((-1,1), (0,2), (0,2), (1,3.5), (0.2,0.8))
    
    results = results = dict(partID=list(), css=list(), ga=list(), ia=list(), lf = list(), bll = list(), converged=list())
    badSubjs = []
    
    for part in partList:
        
        print(part)
        
        subjResponses = read_participant_data('/home/pjrice/gp/ACTR-WM/data/beh/zb/'+part+'/zbResp.csv')
        
        #check if the participant was good at the task. If they weren't, don't estimate parameters
        #threshold values derived through one-sided binomial test of the number of responses that are significantly greater than chance for each condition
        [subj_totAccVec,subj_tarAccVec,subj_lurAccVec,subj_nlrAccVec] = compute_acc(correctResponses,subjResponses)
        subj_tarAcc_sum = np.sum(np.array(subj_tarAccVec))
        subj_lurAcc_sum = np.sum(np.array(subj_lurAccVec))
        subj_nlrAcc_sum = np.sum(np.array(subj_nlrAccVec))
        if (subj_tarAcc_sum < 12) or (subj_lurAcc_sum < 17) or (subj_nlrAcc_sum < 26):
            badSubjs.append(part)
            print('Bad subject: '+part)
            continue
            
        parEst = scipy.optimize.minimize(objective_func, x0=init, args=(stimTiming, correctCueChunks, correctResponses, subjResponses, targetTypes), method = "Powell", bounds = bnds, options = {"maxiter" : 200})
        
        results['partID'].append(part)
        results['css'].append(parEst.x[0])
        results['ga'].append(parEst.x[1])
        results['ia'].append(parEst.x[2])
        results['lf'].append(parEst.x[3])
        results['bll'].append(parEst.x[4])
        results['converged'].append(parEst.message)
        
    return(results,badSubjs)
    



#results,badSubjs = estPars_byPart('/home/pjrice/gp/ACTR-WM/data/beh/zb/')
#test = expandEstResults(results)
#with open('/home/pjrice/gp/ACTR-WM/data/parEstResults/Powell/bounded/chunkAcc2_noBadSubjs_ansEnabled_longRetrievalInterrupt2_parEstExp.json', 'w') as fp: json.dump(test,fp)
#modelMSEs,subjMeasures,modelPredictions = parameterVarExp(test)
#modelMSEs_perPart = parameterVarExp_perPart(test)
#with open('/home/pjrice/gp/ACTR-WM/data/varExp/aggregate/modelMSEs.json', 'w') as fp: json.dump(modelMSEs,fp)    
#with open('/home/pjrice/gp/ACTR-WM/data/varExp/aggregate/subjMeasures.json', 'w') as fp: json.dump(subjMeasures,fp)    
#with open('/home/pjrice/gp/ACTR-WM/data/varExp/aggregate/modelPredictions.json', 'w') as fp: json.dump(modelPredictions,fp)    
#with open('/home/pjrice/gp/ACTR-WM/data/varExp/perPart/modelMSEs_perPart.json', 'w') as fp: json.dump(modelMSEs_perPart,fp)
  
def expandEstResults (results):
    
    actr.load_act_r_code("/home/pjrice/gp/ACTR-WM/code/models/zeroBack/zeroBack-device.lisp")
    
    #correctResponses = read_correct_responses("Z:\gp\ACTR-WM\data\zeroBack_correctResponses.csv")
    correctResponses = read_correct_responses("/home/pjrice/gp/ACTR-WM/data/zeroBack_correctResponses.csv")
    
    correctCueChunks = np.array(['CUE0-0','CUE1-0','CUE2-0','CUE3-0','CUE4-0','CUE5-0','CUE6-0','CUE7-0'])
    correctCueChunks = np.repeat(correctCueChunks,10,axis=0).tolist()
    
    targetTypes = [x[1] for x in correctResponses]
    
    stimTiming = create_stim_timing()
    
    results['allRT_rmse'] = list()
    results['allAcc_rmse'] = list()
    results['bbAcc_rmse'] = list()
    results['bbRT_rmse'] = list()
    results['tarRT_rmse'] = list()
    results['lurRT_rmse'] = list()
    results['nlrRT_rmse'] = list()
    results['tarAcc_rmse'] = list()
    results['lurAcc_rmse'] = list()
    results['nlrAcc_rmse'] = list()
    results['model_tarRT_mean'] = list()
    results['model_lurRT_mean'] = list()
    results['model_nlrRT_mean'] = list()
    results['subj_tarRT_mean'] = list()
    results['subj_lurRT_mean'] = list()
    results['subj_nlrRT_mean'] = list()
    results['model_tarAcc_mean'] = list()
    results['model_lurAcc_mean'] = list()
    results['model_nlrAcc_mean'] = list()
    results['subj_tarAcc_mean'] = list()
    results['subj_lurAcc_mean'] = list()
    results['subj_nlrAcc_mean'] = list()
    results['rtDiff_mean'] = list()
    
    
    for i in range(0,len(results['partID'])):
        
        part = results['partID'][i]
        print(part)
        
        subjResponses = read_participant_data('/home/pjrice/gp/ACTR-WM/data/beh/zb/'+part+'/zbResp.csv')
        
        css = results['css'][i]
        ga = results['ga'][i]
        ia = results['ia'][i]
        lf = results['lf'][i]
        bll = results['bll'][i]
        
        tempModelResponses = runTask(css,ga,ia,lf,bll,stimTiming)
        #modelResponses = [[i[0],i[1],j] for i,j in zip(tempModelResponses,targetTypes)]
        modelResponses = [[i[0],i[1],i[2],j] for i,j in zip(tempModelResponses,targetTypes)]
        
        [model_totAccVec,model_tarAccVec,model_lurAccVec,model_nlrAccVec] = compute_model_acc(correctCueChunks,modelResponses)
        [subj_totAccVec,subj_tarAccVec,subj_lurAccVec,subj_nlrAccVec] = compute_acc(correctResponses,subjResponses)
        
        modelRTs = np.array([x[1] for x in modelResponses], dtype=np.float)
        subjRTs = np.array([x[1] for x in subjResponses], dtype=np.float)
        
        #replace nans (missing RTs) with mean RT
        np.nan_to_num(modelRTs, copy=False, nan=np.nanmean(modelRTs))
        np.nan_to_num(subjRTs, copy=False, nan=np.nanmean(subjRTs))
        
        ##########################################################################################
        #calculate 'all RTs' rmse
        allRT_rmse = np.sqrt(np.mean((modelRTs - subjRTs)**2))
        results['allRT_rmse'].append(allRT_rmse)
        
        #calculate 'all accuracy' rmse
        #this punishes the model for not fully predicting the trial-by-trial pattern of correct/incorrect
        allAcc_rmse = np.sqrt(np.mean((np.array(model_totAccVec) - np.array(subj_totAccVec))**2))
        results['allAcc_rmse'].append(allAcc_rmse)
        
        ##########################################################################################
        #calculate block-by-block RT/acc rmse
    
        modelAcc_byBlock = np.array([np.mean(x) for x in chunks(model_totAccVec,10)], dtype=np.float)
        subjAcc_byBlock = np.array([np.mean(x) for x in chunks(subj_totAccVec,10)], dtype=np.float)
        
        bbAcc_rmse = np.sqrt(np.mean((modelAcc_byBlock - subjAcc_byBlock)**2))
        results['bbAcc_rmse'].append(bbAcc_rmse)
        
        modelRT_byBlock = np.array([np.mean(x) for x in chunks(modelRTs,10)], dtype=np.float)
        subjRT_byBlock = np.array([np.mean(x) for x in chunks(subjRTs,10)], dtype=np.float)
        
        bbRT_rmse = np.sqrt(np.mean((modelRT_byBlock - subjRT_byBlock)**2))
        results['bbRT_rmse'].append(bbRT_rmse)
        
        ##########################################################################################
        #calculate target/lure/nonlure RT/acc rmse
        
        # target RTs
        model_tarRT = np.array([x[1] for x in modelResponses if x[3]=='target'], dtype=np.float)
        subj_tarRT = np.array([x[1] for x in subjResponses if x[2]=='target'], dtype=np.float)
        
        #replace nans (missing RTs) with mean RT
        np.nan_to_num(model_tarRT, copy=False, nan=np.nanmean(model_tarRT))
        np.nan_to_num(subj_tarRT, copy=False, nan=np.nanmean(subj_tarRT))
        
        tarRT_rmse = np.sqrt(np.mean((model_tarRT - subj_tarRT)**2))
        results['tarRT_rmse'].append(tarRT_rmse)
        
        # lure RTs
        model_lurRT = np.array([x[1] for x in modelResponses if x[3]=='lure'], dtype=np.float)
        subj_lurRT = np.array([x[1] for x in subjResponses if x[2]=='lure'], dtype=np.float)
        
        #replace nans (missing RTs) with mean RT
        np.nan_to_num(model_lurRT, copy=False, nan=np.nanmean(model_lurRT))
        np.nan_to_num(subj_lurRT, copy=False, nan=np.nanmean(subj_lurRT))
        
        lurRT_rmse = np.sqrt(np.mean((model_lurRT - subj_lurRT)**2))
        results['lurRT_rmse'].append(lurRT_rmse)
        
        
        # nonlure RTs
        model_nlrRT = np.array([x[1] for x in modelResponses if x[3]=='nonlure'], dtype=np.float)
        subj_nlrRT = np.array([x[1] for x in subjResponses if x[2]=='nonlure'], dtype=np.float)
        
        #replace nans (missing RTs) with mean RT
        np.nan_to_num(model_nlrRT, copy=False, nan=np.nanmean(model_nlrRT))
        np.nan_to_num(subj_nlrRT, copy=False, nan=np.nanmean(subj_nlrRT))
        
        nlrRT_rmse = np.sqrt(np.mean((model_nlrRT - subj_nlrRT)**2))
        results['nlrRT_rmse'].append(nlrRT_rmse)
    
        #target/lure/nonlure accuracy rmse
        #punishes model for not fully predicting the trial-by-trial pattern of correct/incorrect
        #do it across participants, difference between avg tar accs
        tarAcc_rmse = np.sqrt(np.mean((np.array(model_tarAccVec) - np.array(subj_tarAccVec))**2))
        lurAcc_rmse = np.sqrt(np.mean((np.array(model_lurAccVec) - np.array(subj_lurAccVec))**2))
        nlrAcc_rmse = np.sqrt(np.mean((np.array(model_nlrAccVec) - np.array(subj_nlrAccVec))**2))
        results['tarAcc_rmse'].append(tarAcc_rmse)
        results['lurAcc_rmse'].append(lurAcc_rmse)
        results['nlrAcc_rmse'].append(nlrAcc_rmse)
        
        ##########################################################################################
        #target/lure/nonlure RT and accuracy means to calculate across-parts rmse
        
        model_tarRT_mean = np.mean(model_tarRT)
        model_lurRT_mean = np.mean(model_lurRT)
        model_nlrRT_mean = np.mean(model_nlrRT)
        results['model_tarRT_mean'].append(model_tarRT_mean)
        results['model_lurRT_mean'].append(model_lurRT_mean)
        results['model_nlrRT_mean'].append(model_nlrRT_mean)
        
        subj_tarRT_mean = np.mean(subj_tarRT)
        subj_lurRT_mean = np.mean(subj_lurRT)
        subj_nlrRT_mean = np.mean(subj_nlrRT)
        results['subj_tarRT_mean'].append(subj_tarRT_mean)
        results['subj_lurRT_mean'].append(subj_lurRT_mean)
        results['subj_nlrRT_mean'].append(subj_nlrRT_mean)
        
        model_tarAcc_mean = np.mean(np.array(model_tarAccVec))
        model_lurAcc_mean = np.mean(np.array(model_lurAccVec))
        model_nlrAcc_mean = np.mean(np.array(model_nlrAccVec))
        results['model_tarAcc_mean'].append(model_tarAcc_mean)
        results['model_lurAcc_mean'].append(model_lurAcc_mean)
        results['model_nlrAcc_mean'].append(model_nlrAcc_mean)
        
        subj_tarAcc_mean = np.mean(np.array(subj_tarAccVec))
        subj_lurAcc_mean = np.mean(np.array(subj_lurAccVec))
        subj_nlrAcc_mean = np.mean(np.array(subj_nlrAccVec))
        results['subj_tarAcc_mean'].append(subj_tarAcc_mean)
        results['subj_lurAcc_mean'].append(subj_lurAcc_mean)
        results['subj_nlrAcc_mean'].append(subj_nlrAcc_mean)
        
        ##########################################################################################
        #is estimating :lf worthwhile?
        #histogram of the mean of the differences - if it isn't around 0, :lf could shift
        
        rtDiff_mean = np.mean(modelRTs - subjRTs)
        results['rtDiff_mean'].append(rtDiff_mean)
        
    return(results)

def expandEstResults_bootstrap (results):
    
    actr.load_act_r_code("/home/pjrice/gp/ACTR-WM/code/models/zeroBack/zeroBack-device.lisp")
    
    #correctResponses = read_correct_responses("Z:\gp\ACTR-WM\data\zeroBack_correctResponses.csv")
    correctResponses = read_correct_responses("/home/pjrice/gp/ACTR-WM/data/zeroBack_correctResponses.csv")
    
    correctCueChunks = np.array(['CUE0-0','CUE1-0','CUE2-0','CUE3-0','CUE4-0','CUE5-0','CUE6-0','CUE7-0'])
    correctCueChunks = np.repeat(correctCueChunks,10,axis=0).tolist()
    
    targetTypes = [x[1] for x in correctResponses]
    
    stimTiming = create_stim_timing()
    
    results['allRT_rmse'] = list()
    results['allAcc_rmse'] = list()
    results['bbAcc_rmse'] = list()
    results['bbRT_rmse'] = list()
    results['tarRT_rmse'] = list()
    results['lurRT_rmse'] = list()
    results['nlrRT_rmse'] = list()
    results['tarAcc_rmse'] = list()
    results['lurAcc_rmse'] = list()
    results['nlrAcc_rmse'] = list()
    results['model_tarRT_mean'] = list()
    results['model_lurRT_mean'] = list()
    results['model_nlrRT_mean'] = list()
    results['subj_tarRT_mean'] = list()
    results['subj_lurRT_mean'] = list()
    results['subj_nlrRT_mean'] = list()
    results['model_tarAcc_mean'] = list()
    results['model_lurAcc_mean'] = list()
    results['model_nlrAcc_mean'] = list()
    results['subj_tarAcc_mean'] = list()
    results['subj_lurAcc_mean'] = list()
    results['subj_nlrAcc_mean'] = list()
    results['rtDiff_mean'] = list()
    
    all_model_tarRT_means = list()
    all_model_lurRT_means = list()
    all_model_nlrRT_means = list()
    
    for i in range(0,len(results['partID'])):
        
        part = results['partID'][i]
        print(part)
        
        subjResponses = read_participant_data('/home/pjrice/gp/ACTR-WM/data/beh/zb/'+part+'/zbResp.csv')
        
        css = results['css'][i]
        ga = results['ga'][i]
        ia = results['ia'][i]
        lf = results['lf'][i]
        bll = results['bll'][i]
        
        allRT_rmses = list()
        allAcc_rmses = list()
        bbAcc_rmses = list()
        bbRT_rmses = list()
        tarRT_rmses = list()
        lurRT_rmses = list()
        nlrRT_rmses = list()
        tarAcc_rmses = list()
        lurAcc_rmses = list()
        nlrAcc_rmses = list()
        model_tarRT_means = list()
        model_lurRT_means = list()
        model_nlrRT_means = list()
        subj_tarRT_means = list()
        subj_lurRT_means = list()
        subj_nlrRT_means = list()
        model_tarAcc_means = list()
        model_lurAcc_means = list()
        model_nlrAcc_means = list()
        subj_tarAcc_means = list()
        subj_lurAcc_means = list()
        subj_nlrAcc_means = list()
        rtDiff_means = list()
        
        
        for ii in range(0,100):
            
            print('run ' + str(ii))
        
            tempModelResponses = runTask(css,ga,ia,lf,bll,stimTiming)
            #modelResponses = [[i[0],i[1],j] for i,j in zip(tempModelResponses,targetTypes)]
            modelResponses = [[i[0],i[1],i[2],j] for i,j in zip(tempModelResponses,targetTypes)]
        
            [model_totAccVec,model_tarAccVec,model_lurAccVec,model_nlrAccVec] = compute_model_acc(correctCueChunks,modelResponses)
            [subj_totAccVec,subj_tarAccVec,subj_lurAccVec,subj_nlrAccVec] = compute_acc(correctResponses,subjResponses)
        
            modelRTs = np.array([x[1] for x in modelResponses], dtype=np.float)
            subjRTs = np.array([x[1] for x in subjResponses], dtype=np.float)
        
            #replace nans (missing RTs) with mean RT
            np.nan_to_num(modelRTs, copy=False, nan=np.nanmean(modelRTs))
            np.nan_to_num(subjRTs, copy=False, nan=np.nanmean(subjRTs))
        
            ##########################################################################################
            #calculate 'all RTs' rmse
            allRT_rmse = np.sqrt(np.mean((modelRTs - subjRTs)**2))
            allRT_rmses.append(allRT_rmse)
            #results['allRT_rmse'].append(allRT_rmse)
        
            #calculate 'all accuracy' rmse
            #this punishes the model for not fully predicting the trial-by-trial pattern of correct/incorrect
            allAcc_rmse = np.sqrt(np.mean((np.array(model_totAccVec) - np.array(subj_totAccVec))**2))
            allAcc_rmses.append(allAcc_rmse)
            #results['allAcc_rmse'].append(allAcc_rmse)
        
            ##########################################################################################
            #calculate block-by-block RT/acc rmse
    
            modelAcc_byBlock = np.array([np.mean(x) for x in chunks(model_totAccVec,10)], dtype=np.float)
            subjAcc_byBlock = np.array([np.mean(x) for x in chunks(subj_totAccVec,10)], dtype=np.float)
        
            bbAcc_rmse = np.sqrt(np.mean((modelAcc_byBlock - subjAcc_byBlock)**2))
            bbAcc_rmses.append(bbAcc_rmse)
            #results['bbAcc_rmse'].append(bbAcc_rmse)
        
            modelRT_byBlock = np.array([np.mean(x) for x in chunks(modelRTs,10)], dtype=np.float)
            subjRT_byBlock = np.array([np.mean(x) for x in chunks(subjRTs,10)], dtype=np.float)
        
            bbRT_rmse = np.sqrt(np.mean((modelRT_byBlock - subjRT_byBlock)**2))
            bbRT_rmses.append(bbRT_rmse)
            #results['bbRT_rmse'].append(bbRT_rmse)
        
            ##########################################################################################
            #calculate target/lure/nonlure RT/acc rmse
        
            # target RTs
            model_tarRT = np.array([x[1] for x in modelResponses if x[3]=='target'], dtype=np.float)
            subj_tarRT = np.array([x[1] for x in subjResponses if x[2]=='target'], dtype=np.float)
        
            #replace nans (missing RTs) with mean RT
            np.nan_to_num(model_tarRT, copy=False, nan=np.nanmean(model_tarRT))
            np.nan_to_num(subj_tarRT, copy=False, nan=np.nanmean(subj_tarRT))
        
            tarRT_rmse = np.sqrt(np.mean((model_tarRT - subj_tarRT)**2))
            tarRT_rmses.append(tarRT_rmse)
            #results['tarRT_rmse'].append(tarRT_rmse)
        
            # lure RTs
            model_lurRT = np.array([x[1] for x in modelResponses if x[3]=='lure'], dtype=np.float)
            subj_lurRT = np.array([x[1] for x in subjResponses if x[2]=='lure'], dtype=np.float)
        
            #replace nans (missing RTs) with mean RT
            np.nan_to_num(model_lurRT, copy=False, nan=np.nanmean(model_lurRT))
            np.nan_to_num(subj_lurRT, copy=False, nan=np.nanmean(subj_lurRT))
        
            lurRT_rmse = np.sqrt(np.mean((model_lurRT - subj_lurRT)**2))
            lurRT_rmses.append(lurRT_rmse)
            #results['lurRT_rmse'].append(lurRT_rmse)
        
        
            # nonlure RTs
            model_nlrRT = np.array([x[1] for x in modelResponses if x[3]=='nonlure'], dtype=np.float)
            subj_nlrRT = np.array([x[1] for x in subjResponses if x[2]=='nonlure'], dtype=np.float)
        
            #replace nans (missing RTs) with mean RT
            np.nan_to_num(model_nlrRT, copy=False, nan=np.nanmean(model_nlrRT))
            np.nan_to_num(subj_nlrRT, copy=False, nan=np.nanmean(subj_nlrRT))
        
            nlrRT_rmse = np.sqrt(np.mean((model_nlrRT - subj_nlrRT)**2))
            nlrRT_rmses.append(nlrRT_rmse)
            #results['nlrRT_rmse'].append(nlrRT_rmse)
    
            #target/lure/nonlure accuracy rmse
            #punishes model for not fully predicting the trial-by-trial pattern of correct/incorrect
            #do it across participants, difference between avg tar accs
            tarAcc_rmse = np.sqrt(np.mean((np.array(model_tarAccVec) - np.array(subj_tarAccVec))**2))
            lurAcc_rmse = np.sqrt(np.mean((np.array(model_lurAccVec) - np.array(subj_lurAccVec))**2))
            nlrAcc_rmse = np.sqrt(np.mean((np.array(model_nlrAccVec) - np.array(subj_nlrAccVec))**2))
            tarAcc_rmses.append(tarAcc_rmse)
            lurAcc_rmses.append(lurAcc_rmse)
            nlrAcc_rmses.append(nlrAcc_rmse)
            #results['tarAcc_rmse'].append(tarAcc_rmse)
            #results['lurAcc_rmse'].append(lurAcc_rmse)
            #results['nlrAcc_rmse'].append(nlrAcc_rmse)
        
            ##########################################################################################
            #target/lure/nonlure RT and accuracy means to calculate across-parts rmse
        
            model_tarRT_mean = np.mean(model_tarRT)
            model_lurRT_mean = np.mean(model_lurRT)
            model_nlrRT_mean = np.mean(model_nlrRT)
            model_tarRT_means.append(model_tarRT_mean)
            model_lurRT_means.append(model_lurRT_mean)
            model_nlrRT_means.append(model_nlrRT_mean)
            #results['model_tarRT_mean'].append(model_tarRT_mean)
            #results['model_lurRT_mean'].append(model_lurRT_mean)
            #results['model_nlrRT_mean'].append(model_nlrRT_mean)
        
            subj_tarRT_mean = np.mean(subj_tarRT)
            subj_lurRT_mean = np.mean(subj_lurRT)
            subj_nlrRT_mean = np.mean(subj_nlrRT)
            subj_tarRT_means.append(subj_tarRT_mean)
            subj_lurRT_means.append(subj_lurRT_mean)
            subj_nlrRT_means.append(subj_nlrRT_mean)
            #results['subj_tarRT_mean'].append(subj_tarRT_mean)
            #results['subj_lurRT_mean'].append(subj_lurRT_mean)
            #results['subj_nlrRT_mean'].append(subj_nlrRT_mean)
        
            model_tarAcc_mean = np.mean(np.array(model_tarAccVec))
            model_lurAcc_mean = np.mean(np.array(model_lurAccVec))
            model_nlrAcc_mean = np.mean(np.array(model_nlrAccVec))
            model_tarAcc_means.append(model_tarAcc_mean)
            model_lurAcc_means.append(model_lurAcc_mean)
            model_nlrAcc_means.append(model_nlrAcc_mean)
            #results['model_tarAcc_mean'].append(model_tarAcc_mean)
            #results['model_lurAcc_mean'].append(model_lurAcc_mean)
            #results['model_nlrAcc_mean'].append(model_nlrAcc_mean)
        
            subj_tarAcc_mean = np.mean(np.array(subj_tarAccVec))
            subj_lurAcc_mean = np.mean(np.array(subj_lurAccVec))
            subj_nlrAcc_mean = np.mean(np.array(subj_nlrAccVec))
            subj_tarAcc_means.append(subj_tarAcc_mean)
            subj_lurAcc_means.append(subj_lurAcc_mean)
            subj_nlrAcc_means.append(subj_nlrAcc_mean)
            #results['subj_tarAcc_mean'].append(subj_tarAcc_mean)
            #results['subj_lurAcc_mean'].append(subj_lurAcc_mean)
            #results['subj_nlrAcc_mean'].append(subj_nlrAcc_mean)
        
            ##########################################################################################
            #is estimating :lf worthwhile?
            #histogram of the mean of the differences - if it isn't around 0, :lf could shift
        
            rtDiff_mean = np.mean(modelRTs - subjRTs)
            rtDiff_means.append(rtDiff_mean)
            #results['rtDiff_mean'].append(rtDiff_mean)
        
        #all model run model RT means
        all_model_tarRT_means.append(model_tarRT_means)
        all_model_lurRT_means.append(model_lurRT_means)
        all_model_nlrRT_means.append(model_nlrRT_means)
        
        #means of model runs
        results['allRT_rmse'].append(np.mean(allRT_rmses))
        results['allAcc_rmse'].append(np.mean(allAcc_rmses))
        results['bbAcc_rmse'].append(np.mean(bbAcc_rmses))
        results['bbRT_rmse'].append(np.mean(bbRT_rmses))
        results['tarRT_rmse'].append(np.mean(tarRT_rmses))
        results['lurRT_rmse'].append(np.mean(lurRT_rmses))
        results['nlrRT_rmse'].append(np.mean(nlrRT_rmses))
        results['tarAcc_rmse'].append(np.mean(tarAcc_rmses))
        results['lurAcc_rmse'].append(np.mean(lurAcc_rmses))
        results['nlrAcc_rmse'].append(np.mean(nlrAcc_rmses))
        results['model_tarRT_mean'].append(np.mean(model_tarRT_means))
        results['model_lurRT_mean'].append(np.mean(model_lurRT_means))
        results['model_nlrRT_mean'].append(np.mean(model_nlrRT_means))
        results['subj_tarRT_mean'].append(np.mean(subj_tarRT_means))
        results['subj_lurRT_mean'].append(np.mean(subj_lurRT_means))
        results['subj_nlrRT_mean'].append(np.mean(subj_nlrRT_means))
        results['model_tarAcc_mean'].append(np.mean(model_tarAcc_means))
        results['model_lurAcc_mean'].append(np.mean(model_lurAcc_means))
        results['model_nlrAcc_mean'].append(np.mean(model_nlrAcc_means))
        results['subj_tarAcc_mean'].append(np.mean(subj_tarAcc_means))
        results['subj_lurAcc_mean'].append(np.mean(subj_lurAcc_means))
        results['subj_nlrAcc_mean'].append(np.mean(subj_nlrAcc_means))
        results['rtDiff_mean'].append(np.mean(rtDiff_means))
        
    return(results, all_model_tarRT_means, all_model_lurRT_means, all_model_nlrRT_means)
        
        
