import os
import actr
import csv
import pickle
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
    
    # 86400 instead of 15 to account for day-long break between session 1 and 2
    #ses2Timing = ses1Timing[-1]+15+2.5+ses1Timing
    ses2Timing = ses1Timing[-1]+86400+2.5+ses1Timing
    
    stimTiming = np.concatenate((ses1Timing,ses2Timing), axis=None)
    
    return(stimTiming)

def runTask (css, ga, ia, stimTiming):
        
    #actr.load_act_r_model("Z:\gp\ACTR-WM\code\models\zeroBack\zeroBack-model-main.lisp")
    actr.load_act_r_model("/home/pjrice/gp/ACTR-WM/code/models/zeroBack/zeroBack-model-main.lisp")
    
    #set parameters in process of being estimated
    actr.call_command('set-similarities', ['cue', 'stimulus', css])
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

def compute_rmse(css, ga, ia, stimTiming, correctResponses, subjResponses, targetTypes):
    
    #run model, add targetTypes to model responses
    tempModelResponses = runTask(css, ga, ia, stimTiming)
    modelResponses = [[i[0],i[1],j] for i,j in zip(tempModelResponses,targetTypes)]
    
    #get model/participant RTs and target types
    modelRTs = [[x[1],x[2]] if x[1] is not None else [None,x[2]] for x in modelResponses]
    subjRTs = [[float(x[1]),x[2]] if x[1] is not None else [None,x[2]] for x in subjResponses]
    
    #calculate model/participant target, lure, and nonlure accuracy vectors
    [model_totAccVec,model_tarAccVec,model_lurAccVec,model_nlrAccVec] = compute_acc(correctResponses,modelResponses)
    [subj_totAccVec,subj_tarAccVec,subj_lurAccVec,subj_nlrAccVec] = compute_acc(correctResponses,subjResponses)
    
    #calculate model/participant target, lure, and nonlure accuracy percentages
    model_tarAcc = np.mean(model_tarAccVec)
    model_lurAcc = np.mean(model_lurAccVec)
    model_nlrAcc = np.mean(model_nlrAccVec)
    
    subj_tarAcc = np.mean(subj_tarAccVec)
    subj_lurAcc = np.mean(subj_lurAccVec)
    subj_nlrAcc = np.mean(subj_nlrAccVec)
    
    #calculate model/participant target, lure, and nonlure mean RTs
    #for missing model/participant responses (which are counted as incorrect in the accuracy measures), 
    #replace missing RT with the model/participant mean RT
    #so, just take the nanmean, because it results in the same mean RT    
    model_tarRT = np.nanmean(np.array([x[0] for x in modelRTs if x[1]=='target'], dtype=np.float))
    model_lurRT = np.nanmean(np.array([x[0] for x in modelRTs if x[1]=='lure'], dtype=np.float))
    model_nlrRT = np.nanmean(np.array([x[0] for x in modelRTs if x[1]=='nonlure'], dtype=np.float))
    
    subj_tarRT = np.nanmean(np.array([x[0] for x in subjRTs if x[1]=='target'], dtype=np.float))
    subj_lurRT = np.nanmean(np.array([x[0] for x in subjRTs if x[1]=='lure'], dtype=np.float))
    subj_nlrRT = np.nanmean(np.array([x[0] for x in subjRTs if x[1]=='nonlure'], dtype=np.float))

    #put both accuracies and RTs on the same scale by applying the transform:
    #   (predicted-observed)/observed
    #on both accuracies and RTs, where predicted=model results and observed=participant results
    # this is the "first half" of the RMSE calculation - the values will be squared, meaned, and sqr rooted later
    
    tarAcc = (model_tarAcc - subj_tarAcc)/subj_tarAcc
    lurAcc = (model_lurAcc - subj_lurAcc)/subj_lurAcc
    nlrAcc = (model_nlrAcc - subj_nlrAcc)/subj_nlrAcc
    
    tarRT = (model_tarRT - subj_tarRT)/subj_tarRT
    lurRT = (model_lurRT - subj_lurRT)/subj_lurRT
    nlrRT = (model_nlrRT - subj_nlrRT)/subj_nlrRT
    
    
    #create vector
    rmse_vec = np.array([tarAcc, lurAcc, nlrAcc, tarRT, lurRT, nlrRT])
    
    #rmse
    rmse = np.sqrt(np.mean(rmse_vec**2))
    
    return(rmse)

def objective_func (x, stimTiming, correctResponses, subjResponses, targetTypes):
    return(compute_rmse(x[0], # css 
                        x[1], # ga
                        x[2], # ia
                        stimTiming, correctResponses, subjResponses, targetTypes))
    


#actr.load_act_r_code("Z:\gp\ACTR-WM\code\models\zeroBack\zeroBack-device.lisp")
#actr.load_act_r_code("/home/pjrice/gp/ACTR-WM/code/models/zeroBack/zeroBack-device.lisp")

#minimize(objective_func, x0=init, args=(stimTiming, correctResponses, subjResponses, targetTypes), method = "Nelder-Mead", options = {"maxiter" : 20})


def estPars_byPart (rootDataDir):
    
    actr.load_act_r_code("/home/pjrice/gp/ACTR-WM/code/models/zeroBack/zeroBack-device.lisp")
    
    correctResponses = read_correct_responses("/home/pjrice/gp/ACTR-WM/data/zeroBack_correctResponses.csv")    
    targetTypes = [x[1] for x in correctResponses]    
    stimTiming = create_stim_timing()
    
    partList = os.listdir(rootDataDir)
    
    init = [-0.1, 1, 1]
    
    results = results = dict(partID=list(), css=list(), ga=list(), ia=list(), converged=list())
    
    for part in partList:
        
        print(part)
        
        subjResponses = read_participant_data('/home/pjrice/gp/ACTR-WM/data/beh/zb/'+part+'/zbResp.csv')
        
        parEst = minimize(objective_func, x0=init, args=(stimTiming, correctResponses, subjResponses, targetTypes), method = "Nelder-Mead", options = {"maxiter" : 200})
        
        results['partID'].append(part)
        results['css'].append(parEst.x[0])
        results['ga'].append(parEst.x[1])
        results['ia'].append(parEst.x[2])
        results['converged'].append(parEst.message)
        
    return(results)
    



#results = estPars_byPart('/home/pjrice/gp/ACTR-WM/data/beh/zb/')
#pickle.dump(results, open('/home/pjrice/gp/ACTR-WM/data/tt_parEst.p','wb'))
#results = pickle.load(open('/home/pjrice/gp/ACTR-WM/data/tt_parEst.p','rb'))
    

def check_parVal_4part (css, ga, ia):
    
    actr.load_act_r_code("/home/pjrice/gp/ACTR-WM/code/models/zeroBack/zeroBack-device.lisp")
    
    correctResponses = read_correct_responses("Z:\gp\ACTR-WM\data\zeroBack_correctResponses.csv")
    #correctResponses = read_correct_responses("/home/pjrice/gp/ACTR-WM/data/zeroBack_correctResponses.csv")

    subjResponses = read_participant_data('Z:\gp\ACTR-WM\data\sub-100307\zb_testResponses.csv')
    #subjResponses = read_participant_data('/home/pjrice/gp/ACTR-WM/data/sub-100307/zb_testResponses.csv')
    
    targetTypes = [x[1] for x in correctResponses]
    
    stimTiming = create_stim_timing()
    
    tempModelResponses = runTask(css,ga,ia,stimTiming)
    modelResponses = [[i[0],i[1],j] for i,j in zip(tempModelResponses,targetTypes)]
    
    [model_totAcc,model_tarAcc,model_lurAcc,model_nlrAcc] = compute_acc(correctResponses,modelResponses)
    [part_totAcc,part_tarAcc,part_lurAcc,part_nlrAcc] = compute_acc(correctResponses,subjResponses)
    
    results = dict(totAcc=dict(model=np.mean(model_totAcc),part=np.mean(part_totAcc)),
                   tarAcc=dict(model=np.mean(model_tarAcc),part=np.mean(part_tarAcc)),
                   lurAcc=dict(model=np.mean(model_lurAcc),part=np.mean(part_lurAcc)),
                   nlrAcc=dict(model=np.mean(model_nlrAcc),part=np.mean(part_nlrAcc)))
    
    
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
    
    
    

def expandEstResults (results):
    
    actr.load_act_r_code("/home/pjrice/gp/ACTR-WM/code/models/zeroBack/zeroBack-device.lisp")
    
    #correctResponses = read_correct_responses("Z:\gp\ACTR-WM\data\zeroBack_correctResponses.csv")
    correctResponses = read_correct_responses("/home/pjrice/gp/ACTR-WM/data/zeroBack_correctResponses.csv")
    
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
        
        tempModelResponses = runTask(css,ga,ia,stimTiming)
        modelResponses = [[i[0],i[1],j] for i,j in zip(tempModelResponses,targetTypes)]
        
        [model_totAccVec,model_tarAccVec,model_lurAccVec,model_nlrAccVec] = compute_acc(correctResponses,modelResponses)
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
        model_tarRT = np.array([x[1] for x in modelResponses if x[2]=='target'], dtype=np.float)
        subj_tarRT = np.array([x[1] for x in subjResponses if x[2]=='target'], dtype=np.float)
        
        #replace nans (missing RTs) with mean RT
        np.nan_to_num(model_tarRT, copy=False, nan=np.nanmean(model_tarRT))
        np.nan_to_num(subj_tarRT, copy=False, nan=np.nanmean(subj_tarRT))
        
        tarRT_rmse = np.sqrt(np.mean((model_tarRT - subj_tarRT)**2))
        results['tarRT_rmse'].append(tarRT_rmse)
        
        # lure RTs
        model_lurRT = np.array([x[1] for x in modelResponses if x[2]=='lure'], dtype=np.float)
        subj_lurRT = np.array([x[1] for x in subjResponses if x[2]=='lure'], dtype=np.float)
        
        #replace nans (missing RTs) with mean RT
        np.nan_to_num(model_lurRT, copy=False, nan=np.nanmean(model_lurRT))
        np.nan_to_num(subj_lurRT, copy=False, nan=np.nanmean(subj_lurRT))
        
        lurRT_rmse = np.sqrt(np.mean((model_lurRT - subj_lurRT)**2))
        results['lurRT_rmse'].append(lurRT_rmse)
        
        
        # nonlure RTs
        model_nlrRT = np.array([x[1] for x in modelResponses if x[2]=='nonlure'], dtype=np.float)
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
        
        
        
       
        
        
        
        
#results = pickle.load(open('/home/pjrice/Desktop/parEstResults/ttBB_parEst.p','rb'))
#test = expandEstResults(results)
#pickle.dump(test, open('/home/pjrice/Desktop/parEstResults/ttBB_parEstExp.p','wb'))
        
        
        
    
    
    
    
    
    
    
    
    
    
    