# ***FOUR*** parameter zero-back model estimation

import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '/home/pjrice/gp/ACTR-WM/code/estimation')
from modelEstimationUtilFunctions import *

import os
import scipy.optimize

os.chdir('/home/pjrice/Downloads/ACT-R/tutorial/python')
import actr

def runTask (ga, ia, lf, bll, stimTiming):
    """Loads the ACT-R model, sets the parameters [that have been input as
    arguments], runs the model by calling the 'runTaskFromPython' lisp function,
    retrieves the model's responses, and returns a cleaned-up list of those
    responses."""
        
    # load the zero-back ACT-R model
    actr.load_act_r_model("/home/pjrice/gp/ACTR-WM/code/models/zeroBack/zeroBack-model-main.lisp")
    
    # set parameters in process of being estimated
    actr.call_command('set-similarities', ['cue', 'stimulus', -0.49]) #mean (across parts) of css estimated in 5-parameter ests
    actr.set_parameter_value(":ga", ga)
    actr.set_parameter_value(":imaginal-activation", ia)
    actr.set_parameter_value(":lf", lf)
    actr.set_parameter_value(":bll", bll)    
    
    # run the task
    actr.call_command('runTaskFromPython')
    
    # retrieve the responses
    tempModelResponses = actr.call_command('print-resp')
    tempModelResponses.reverse()
    
    # get model's keypress responses, RTs, and retrieved chunks
    tempResponses = [x[0] for x in tempModelResponses]
    tempRTs = [x[1] for x in tempModelResponses]
    tempChunkRetrievals = [x[2] for x in tempModelResponses]
    
    # compute RTs by subtracting the timing of the stimuli
    modelRespTimes = [round((i-j),3) if i is not None else i for i,j in zip(tempRTs,stimTiming.tolist())]
    
    # clean up responses/RTs/chunk retrievals into list of lists
    modelResponses = [[i,j,k] for i,j,k in zip(tempResponses,modelRespTimes,tempChunkRetrievals)]
    
    return(modelResponses)

def compute_rmse(ga, ia, lf, bll, stimTiming, correctCueChunks, correctResponses, subjResponses, targetTypes):
    """Compute the RMSE between the participant's and model's trial-by-trial RTs
    and block-by-block/condition-wise accuracies. Calls runTask(), replaces 
    missing RTs with the mean RT, calculates model/participant accuracies,
    rescales RTs to between 0-1 to be on the same scale as accuracies, and then
    computes the RMSE."""
    
    # run model, add targetTypes to model responses
    tempModelResponses = runTask(ga, ia, lf, bll, stimTiming)
    modelResponses = [[i[0],i[1],i[2],j] for i,j in zip(tempModelResponses,targetTypes)]
    
    # get model/participant RTs
    modelRTs = np.array([x[1] for x in modelResponses], dtype=np.float)
    subjRTs = np.array([x[1] for x in subjResponses], dtype=np.float)
    
    # replace nans (missing RTs) with mean RT
    np.nan_to_num(modelRTs, copy=False, nan=np.nanmean(modelRTs))
    np.nan_to_num(subjRTs, copy=False, nan=np.nanmean(subjRTs))
    
    # calculate model/participant target, lure, and nonlure accuracy vectors
    [model_totAccVec,model_tarAccVec,model_lurAccVec,model_nlrAccVec] = compute_model_acc(correctCueChunks,modelResponses)
    [subj_totAccVec,subj_tarAccVec,subj_lurAccVec,subj_nlrAccVec] = compute_acc(correctResponses,subjResponses)
    
    # calculate model/participant target, lure, and nonlure accuracy percentages
    model_tarAcc = np.mean(model_tarAccVec)
    model_lurAcc = np.mean(model_lurAccVec)
    model_nlrAcc = np.mean(model_nlrAccVec)
    
    subj_tarAcc = np.mean(subj_tarAccVec)
    subj_lurAcc = np.mean(subj_lurAccVec)
    subj_nlrAcc = np.mean(subj_nlrAccVec)
    
    # calculate block-by-block accuracies
    modelAcc_byBlock = np.array([np.mean(x) for x in chunks(model_totAccVec,10)], dtype=np.float)
    subjAcc_byBlock = np.array([np.mean(x) for x in chunks(subj_totAccVec,10)], dtype=np.float)
    
    # rescale RTs by dividing by max allowable RT (2 seconds)
    # RTs will now be on same scale as accuracy (bounded by (0,1))
    scaled_modelRTs = modelRTs/2
    scaled_subjRTs = subjRTs/2
    
    # create singleton vectors of combined scaled RTs and target/lure/nonlure accuracies for model and participant
    modelVec = np.concatenate((scaled_modelRTs,model_tarAcc,model_lurAcc,model_nlrAcc,modelAcc_byBlock), axis=None)
    subjVec = np.concatenate((scaled_subjRTs,subj_tarAcc,subj_lurAcc,subj_nlrAcc,subjAcc_byBlock), axis=None)
    
    # compute rmse
    rmse = np.sqrt(np.mean((modelVec - subjVec)**2))
    
    return(rmse)

# def objective_func (x, stimTiming, correctCueChunks, correctResponses, subjResponses, targetTypes):
#     return(compute_rmse(x[0], # css 
#                         x[1], # ga
#                         x[2], # ia
#                         x[3], # lf
#                         x[4], # bll
#                         stimTiming, correctCueChunks, correctResponses, subjResponses, targetTypes))

def objective_func (x, stimTiming, correctCueChunks, correctResponses, subjResponses, targetTypes):
    """Objective function for the minimization algorithm. Usually returns the output of compute_rmse();
    however, due to scipy.optimize.minimize sometimes not respecting the bounds on the parameters, returns
    a large value (10) if the :bll parameter is set out of range."""
    if x[3] > 1:
        return(10)
    else:
        return(compute_rmse(x[0], # ga 
                        x[1], # ia
                        x[2], # lf
                        x[3], # bll
                        stimTiming, correctCueChunks, correctResponses, subjResponses, targetTypes))
    
def estPars_byPart (rootDir):
    """Estimates parameters for the zero-back HCP n-back task ACT-R model on a per-participant basis.
    Establishes the correct chunk to be retrieved for each trial/loads the correct responses. Filters for 
    bad participants who did not achieve responses significantly greater than chance for the target, lure,
    or nonlure conditions. Estimates parameters using scipy.optimize.minimize's 'Powell' method."""
    
    # load the device
    actr.load_act_r_code(rootDir+"code/models/zeroBack/zeroBack-device.lisp")
    
    #establish the "correct" chunk to retrieve on each trial
    correctCueChunks = np.array(['CUE0-0','CUE1-0','CUE2-0','CUE3-0','CUE4-0','CUE5-0','CUE6-0','CUE7-0'])
    correctCueChunks = np.repeat(correctCueChunks,10,axis=0).tolist()
    
    # read the correct responses for the zero-back condition of the n-back task from the file
    # get the target type of each trial from this data
    correctResponses = read_correct_responses(rootDir+"data/zeroBack_correctResponses.csv")    
    targetTypes = [x[1] for x in correctResponses]    
    
    # create the stimulus timing for the zero-back condition
    stimTiming = create_stim_timing()
    
    # get the list of participants from the behavioral zero-back data directory 
    partList = os.listdir(rootDir+"data/beh/zb/")

    # establish initial values and bounds for the five parameters    
    init = [1, 1, 2.25, 0.5]
    bnds = ((0,2), (0,2), (1,3.5), (0.2,0.8))
    
    #set up dict to put estimation results in
    results = results = dict(partID=list(), ga=list(), ia=list(), lf = list(), bll = list(), converged=list())
    
    # set up list for "bad" participants
    badSubjs = []
    
    # for each particiapnt
    for part in partList:
        
        print(part)
        
        # read this participant's responses for the zero-back condition of the n-back task from the file
        subjResponses = read_participant_data(rootDir+'data/beh/zb/'+part+'/zbResp.csv')
        
        # check if the participant was good at the task. If they weren't, don't estimate parameters
        # threshold values derived through one-sided binomial test of the number of responses that are 
        # significantly greater than chance for each condition
        [subj_totAccVec,subj_tarAccVec,subj_lurAccVec,subj_nlrAccVec] = compute_acc(correctResponses,subjResponses)
        subj_tarAcc_sum = np.sum(np.array(subj_tarAccVec))
        subj_lurAcc_sum = np.sum(np.array(subj_lurAccVec))
        subj_nlrAcc_sum = np.sum(np.array(subj_nlrAccVec))
        if (subj_tarAcc_sum < 12) or (subj_lurAcc_sum < 17) or (subj_nlrAcc_sum < 26):
            badSubjs.append(part)
            print('Bad subject: '+part)
            continue
        
        # estimate parameter set using scipy.optimize.minimize
        parEst = scipy.optimize.minimize(objective_func, 
                                         x0=init, 
                                         args=(stimTiming, 
                                               correctCueChunks, 
                                               correctResponses, 
                                               subjResponses, 
                                               targetTypes), 
                                         method = "Powell", 
                                         bounds = bnds, 
                                         options = {"maxiter" : 200})
        
        # add the estimation results to the dict
        results['partID'].append(part)
        results['ga'].append(parEst.x[0])
        results['ia'].append(parEst.x[1])
        results['lf'].append(parEst.x[2])
        results['bll'].append(parEst.x[3])
        results['converged'].append(parEst.message)
        
    return(results,badSubjs)

def expandEstResults_bootstrap (results):
    """Calculates a set of RMSE values for trial-by-trial RTs/accuracies (allRT/allAcc_rmse),
    block-by-block RTs/accuracies (bbRT/bbAcc_rmse), condition-wise RTs/accuracies (tar/lur/nlrRT/Acc_rmse)
    between a given participant's responses and the model's prediction of those responses. Produces model predictions
    over 100 model runs. Also computes model condition-wise RT and accuracy means, as well as the mean of differences
    between the model RTs and participant RTs."""
    
    actr.load_act_r_code("/home/pjrice/gp/ACTR-WM/code/models/zeroBack/zeroBack-device.lisp")
    
    #correctResponses = read_correct_responses("Z:\gp\ACTR-WM\data\zeroBack_correctResponses.csv")
    correctResponses = read_correct_responses("/home/pjrice/gp/ACTR-WM/data/zeroBack_correctResponses.csv")
    
    correctCueChunks = np.array(['CUE0-0','CUE1-0','CUE2-0','CUE3-0','CUE4-0','CUE5-0','CUE6-0','CUE7-0'])
    correctCueChunks = np.repeat(correctCueChunks,10,axis=0).tolist()
    
    targetTypes = [x[1] for x in correctResponses]
    
    stimTiming = create_stim_timing()
    
    results['allRT_rmse'] = list()
    results['allAcc_rmse'] = list()
    results['bbRT_rmse'] = list()
    results['bbAcc_rmse'] = list()
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
        [subj_totAccVec,subj_tarAccVec,subj_lurAccVec,subj_nlrAccVec] = compute_acc(correctResponses,subjResponses)
        subjRTs = np.array([x[1] for x in subjResponses], dtype=np.float)
        np.nan_to_num(subjRTs, copy=False, nan=np.nanmean(subjRTs))
        
        ga = results['ga'][i]
        ia = results['ia'][i]
        lf = results['lf'][i]
        bll = results['bll'][i]
        
        modelRTs_temp = list()
        modelAccs_temp = list()
        modeltarAccs_temp = list()
        modellurAccs_temp = list()
        modelnlrAccs_temp = list()
        
        for ii in range(0,100):
            
            print('run ' + str(ii+1))
        
            tempModelResponses = runTask(ga,ia,lf,bll,stimTiming)
            #modelResponses = [[i[0],i[1],j] for i,j in zip(tempModelResponses,targetTypes)]
            modelResponses = [[i[0],i[1],i[2],j] for i,j in zip(tempModelResponses,targetTypes)]
        
            [model_totAccVec,model_tarAccVec,model_lurAccVec,model_nlrAccVec] = compute_model_acc(correctCueChunks,modelResponses)
            modelRTs = np.array([x[1] for x in modelResponses], dtype=np.float)
            np.nan_to_num(modelRTs, copy=False, nan=np.nanmean(modelRTs))
            
            ##########################################################################################
            # add model RTs and accuracies to temporary lists
            modelRTs_temp.append(modelRTs)
            modelAccs_temp.append(model_totAccVec)
            modeltarAccs_temp.append(model_tarAccVec)
            modellurAccs_temp.append(model_lurAccVec)
            modelnlrAccs_temp.append(model_nlrAccVec)
            
        # take trial-by-trial means of model RTs and accs
        tbtModelRTs = np.mean(np.array(modelRTs_temp),axis=0)
        tbtModelAccs = np.mean(np.array(modelAccs_temp),axis=0)
        tbtModeltarAccs = np.mean(np.array(modeltarAccs_temp),axis=0)
        tbtModellurAccs = np.mean(np.array(modellurAccs_temp),axis=0)
        tbtModelnlrAccs = np.mean(np.array(modelnlrAccs_temp),axis=0)
        
        ##########################################################################################
        #calculate 'all RTs' rmse
        allRT_rmse = np.sqrt(np.mean((tbtModelRTs - subjRTs)**2))
        results['allRT_rmse'].append(allRT_rmse)
        
        #calculate 'all accuracy' rmse
        #this punishes the model for not fully predicting the trial-by-trial pattern of correct/incorrect
        allAcc_rmse = np.sqrt(np.mean((tbtModelAccs - np.array(subj_totAccVec))**2))
        results['allAcc_rmse'].append(allAcc_rmse)
        
        ##########################################################################################
        #calculate block-by-block RT/acc rmse
        
        modelRT_byBlock = np.array([np.mean(x) for x in chunks(tbtModelRTs,10)], dtype=np.float)
        subjRT_byBlock = np.array([np.mean(x) for x in chunks(subjRTs,10)], dtype=np.float)
        bbRT_rmse = np.sqrt(np.mean((modelRT_byBlock - subjRT_byBlock)**2))
        results['bbRT_rmse'].append(bbRT_rmse)
    
        modelAcc_byBlock = np.array([np.mean(x) for x in chunks(tbtModelAccs,10)], dtype=np.float)
        subjAcc_byBlock = np.array([np.mean(x) for x in chunks(subj_totAccVec,10)], dtype=np.float)
        bbAcc_rmse = np.sqrt(np.mean((modelAcc_byBlock - subjAcc_byBlock)**2))
        results['bbAcc_rmse'].append(bbAcc_rmse)
        
        ##########################################################################################
        #calculate target/lure/nonlure RT/acc rmse
        
        # target RTs
        model_tarRTs = np.array([i for i,j in zip(tbtModelRTs,targetTypes) if j=='target'])
        subj_tarRTs = np.array([i for i,j in zip(subjRTs,targetTypes) if j=='target'])
        tarRT_rmse = np.sqrt(np.mean((model_tarRTs - subj_tarRTs)**2))
        results['tarRT_rmse'].append(tarRT_rmse)
        
        # lure RTs
        model_lurRTs = np.array([i for i,j in zip(tbtModelRTs,targetTypes) if j=='lure'])
        subj_lurRTs = np.array([i for i,j in zip(subjRTs,targetTypes) if j=='lure'])
        lurRT_rmse = np.sqrt(np.mean((model_lurRTs - subj_lurRTs)**2))
        results['lurRT_rmse'].append(lurRT_rmse)
        
        # nonlure RTs
        model_nlrRTs = np.array([i for i,j in zip(tbtModelRTs,targetTypes) if j=='nonlure'])
        subj_nlrRTs = np.array([i for i,j in zip(subjRTs,targetTypes) if j=='nonlure'])
        nlrRT_rmse = np.sqrt(np.mean((model_nlrRTs - subj_nlrRTs)**2))
        results['nlrRT_rmse'].append(nlrRT_rmse)
    
        # target/lure/nonlure accuracy rmse
        tarAcc_rmse = np.sqrt(np.mean((tbtModeltarAccs - np.array(subj_tarAccVec))**2))
        lurAcc_rmse = np.sqrt(np.mean((tbtModellurAccs - np.array(subj_lurAccVec))**2))
        nlrAcc_rmse = np.sqrt(np.mean((tbtModelnlrAccs - np.array(subj_nlrAccVec))**2))
        results['tarAcc_rmse'].append(tarAcc_rmse)
        results['lurAcc_rmse'].append(lurAcc_rmse)
        results['nlrAcc_rmse'].append(nlrAcc_rmse)
        
        ##########################################################################################
        #target/lure/nonlure RT and accuracy means to calculate across-parts rmse
        
        model_tarRT_mean = np.mean(model_tarRTs)
        model_lurRT_mean = np.mean(model_lurRTs)
        model_nlrRT_mean = np.mean(model_nlrRTs)
        results['model_tarRT_mean'].append(model_tarRT_mean)
        results['model_lurRT_mean'].append(model_lurRT_mean)
        results['model_nlrRT_mean'].append(model_nlrRT_mean)
        
        subj_tarRT_mean = np.mean(subj_tarRTs)
        subj_lurRT_mean = np.mean(subj_lurRTs)
        subj_nlrRT_mean = np.mean(subj_nlrRTs)
        results['subj_tarRT_mean'].append(subj_tarRT_mean)
        results['subj_lurRT_mean'].append(subj_lurRT_mean)
        results['subj_nlrRT_mean'].append(subj_nlrRT_mean)
        
        model_tarAcc_mean = np.mean(np.array(tbtModeltarAccs))
        model_lurAcc_mean = np.mean(np.array(tbtModellurAccs))
        model_nlrAcc_mean = np.mean(np.array(tbtModelnlrAccs))
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
        
        rtDiff_mean = np.mean(tbtModelRTs - subjRTs)
        results['rtDiff_mean'].append(rtDiff_mean)
    
        
        
    return(results)



def modelMeanRTAcc (tempModelResponses,targetTypes,correctCueChunks):
    """Returns the mean model RT and accuracy from a single model run."""
    
    modelResponses = [[i[0],i[1],i[2],j] for i,j in zip(tempModelResponses,targetTypes)]
    
    #get model RTs
    modelRTs = np.array([x[1] for x in modelResponses], dtype=np.float)
    #replace nans (missing RTs) with mean RT
    np.nan_to_num(modelRTs, copy=False, nan=np.nanmean(modelRTs))
    modelMeanRT = np.mean(modelRTs)
    
    #calculate model/participant target, lure, and nonlure accuracy vectors
    [model_totAccVec,model_tarAccVec,model_lurAccVec,model_nlrAccVec] = compute_model_acc(correctCueChunks,modelResponses)
    modelMeanAcc = np.mean(model_totAccVec)
    
    return(modelMeanRT,modelMeanAcc)

def incrementalParsModelPredictions (parList,meanPars,subjRTs,subj_totAccVec,stimTiming,targetTypes,correctCueChunks,nRuns):
    """Runs five total models 100 times each. Each model iteration includes another estimated parameter,
    in the order of bll -> ga -> ia -> lf -> css, so that the first model iteration only includes bll and
    the last model iteration includes all five parameters. Computes the mean model RT and accuracy for each
    run, and then averages across the runs to return the mean predicted RT and accuracy."""
    
    #set up output dictionary
    results = {'models':{}}
    
    #get the participant's target, lure, and nonlure mean accuracies
    subj_tarAcc = np.mean([i for i,j in zip(subj_totAccVec,targetTypes) if j=='target'])
    subj_lurAcc = np.mean([i for i,j in zip(subj_totAccVec,targetTypes) if j=='lure'])
    subj_nlrAcc = np.mean([i for i,j in zip(subj_totAccVec,targetTypes) if j=='nonlure'])
        
    #get the block-by-block model accs
    subjAcc_byBlock = [np.mean(x) for x in chunks(subj_totAccVec,10)]
    
    subjAccVec = np.concatenate((subj_tarAcc,subj_lurAcc,subj_nlrAcc,subjAcc_byBlock), axis=None)
    
    #get participant's parameter values
    ga = parList[0]
    ia = parList[1]
    lf = parList[2]
    bll = parList[3]
    
    #get mean (across participants) parameter values
    #meanCSS = meanPars[0]
    meanGA = meanPars[0]
    meanIA = meanPars[1]
    meanLF = meanPars[2]
    meanBLL = meanPars[3] #unused
    
    for i in range(0,len(parList)):
        
        if i==0:
            print('Getting model predictions including only bll parameter...')
            dictKey='bll'
        elif i==1:
            print('Getting model predictions including bll and ga parameters...')
            dictKey='bll,ga'
        elif i==2:
            print('Getting model predictions including bll, ga, and ia parameters...')
            dictKey='bll,ga,ia'
        elif i==3:
            print('Getting model predictions including all four parameters (bll, ga, ia, and lf)...')
            dictKey='bll,ga,ia,lf'
        
        temp_tbtRTs = list()
        temp_tbtAccs = list()
        for ii in range(0,nRuns):
            print('Run ', ii+1)
            actr.load_act_r_model("/home/pjrice/gp/ACTR-WM/code/models/zeroBack/zeroBack-model-main.lisp")
                
            #always setting css to the value it was set to during estimation
            actr.call_command('set-similarities', ['cue', 'stimulus', -0.49]) #mean (across parts) of css estimated in 5-parameter ests
            #always setting bll to the estimated value
            actr.set_parameter_value(":bll", bll)
            #incrementally set parameters to either the mean value or the estimated value
            if i==0:
                actr.set_parameter_value(":ga", meanGA) #mean parameter value
                actr.set_parameter_value(":imaginal-activation", meanIA) #mean parameter value
                actr.set_parameter_value(":lf", meanLF) #mean parameter value
            elif i==1:
                actr.set_parameter_value(":ga", ga) #estimated value
                actr.set_parameter_value(":imaginal-activation", meanIA) #mean parameter value
                actr.set_parameter_value(":lf", meanLF) #mean parameter value
            elif i==2:
                actr.set_parameter_value(":ga", ga) #estimated value
                actr.set_parameter_value(":imaginal-activation", ia) #estimated value
                actr.set_parameter_value(":lf", meanLF) #mean parameter value
            elif i==3:
                actr.set_parameter_value(":ga", ga) #estimated value
                actr.set_parameter_value(":imaginal-activation", ia) #estimated value
                actr.set_parameter_value(":lf", lf) #estimated value

                
            #run the task
            actr.call_command('runTaskFromPython')
            
            #get the model responses
            tempModelResponses = actr.call_command('print-resp')
            tempModelResponses.reverse()
                
            #clean up model responses
            tempResponses = [x[0] for x in tempModelResponses]
            tempRunRTs = [x[1] for x in tempModelResponses]
            tempChunkRetrievals = [x[2] for x in tempModelResponses]
            #clean up responses/RTs into list of lists
            modelRespTimes = [round((i-j),3) if i is not None else i for i,j in zip(tempRunRTs,stimTiming.tolist())]
            modelResponses = [[i,j,k] for i,j,k in zip(tempResponses,modelRespTimes,tempChunkRetrievals)]
            
            #get model RTs
            modelRTs = np.array([x[1] for x in modelResponses], dtype=np.float)
            #replace nans (missing RTs) with mean RT
            np.nan_to_num(modelRTs, copy=False, nan=np.nanmean(modelRTs))
            temp_tbtRTs.append(modelRTs)
            
            #calculate model/participant target, lure, and nonlure accuracy vectors
            modelResponses4Acc = [[i[0],i[1],i[2],j] for i,j in zip(modelResponses,targetTypes)]
            [model_totAccVec,model_tarAccVec,model_lurAccVec,model_nlrAccVec] = compute_model_acc(correctCueChunks,modelResponses4Acc)
            temp_tbtAccs.append(model_totAccVec)
  
            
        #get the trial-by-trial mean RTs/Accs across runs
        tbtModelRTs = np.mean(np.array(temp_tbtRTs),axis=0)
        tbtModelAccs = np.mean(np.array(temp_tbtAccs),axis=0)
        
        #get the model's target, lure, and nonlure mean accuracies
        model_tarAcc = np.mean([i for i,j in zip(tbtModelAccs,targetTypes) if j=='target'])
        model_lurAcc = np.mean([i for i,j in zip(tbtModelAccs,targetTypes) if j=='lure'])
        model_nlrAcc = np.mean([i for i,j in zip(tbtModelAccs,targetTypes) if j=='nonlure'])
        
        #get the block-by-block model accs
        modelAcc_byBlock = [np.mean(x) for x in chunks(tbtModelAccs,10)]
        
        modelAccVec = np.concatenate((model_tarAcc,model_lurAcc,model_nlrAcc,modelAcc_byBlock), axis=None)
        
        #calculate pearson r for tbt RTs and condition-wise/block-wise accuracies
        RT_pearsonr = scipy.stats.pearsonr(subjRTs,tbtModelRTs)
        Acc_pearsonr = scipy.stats.pearsonr(subj_totAccVec,tbtModelAccs)
        cwAcc_pearsonr = scipy.stats.pearsonr(subjAccVec,modelAccVec)
        
        #get the mean of the tbt mean RTs/Accs
        meanModelRT = np.mean(tbtModelRTs)
        meanModelAcc = np.mean(tbtModelAccs)
        
        results['models'][dictKey] = {'meanRT':meanModelRT, 
                                      'meanAcc':meanModelAcc,
                                      'RT_corr':RT_pearsonr[0],
                                      'RT_pval':RT_pearsonr[1],
                                      'Acc_corr':Acc_pearsonr[0],
                                      'Acc_pval':Acc_pearsonr[1],
                                      'cwAcc_corr':cwAcc_pearsonr[0],
                                      'cwAcc_pval':cwAcc_pearsonr[1]}
            
    return(results)
        

def parameterVarExp (estResults,nRuns=100):
    """For each participant, runs the incremental model procedure. Returns each participant's
    mean RT and mean accuracy in subjMeasures, and the set of model's predicted mean RTs and mean 
    accuracies in modelPredictions."""
    
    actr.load_act_r_code("/home/pjrice/gp/ACTR-WM/code/models/zeroBack/zeroBack-device.lisp")
    
    correctResponses = read_correct_responses("/home/pjrice/gp/ACTR-WM/data/zeroBack_correctResponses.csv")
    
    correctCueChunks = np.array(['CUE0-0','CUE1-0','CUE2-0','CUE3-0','CUE4-0','CUE5-0','CUE6-0','CUE7-0'])
    correctCueChunks = np.repeat(correctCueChunks,10,axis=0).tolist()
    
    targetTypes = [x[1] for x in correctResponses]
    
    stimTiming = create_stim_timing()
    
    #get mean parameter values
    meanGA = np.mean(estResults['ga'])
    meanIA = np.mean(estResults['ia'])
    meanLF = np.mean(estResults['lf'])
    meanBLL = np.mean(estResults['bll'])
    meanPars = [meanGA,meanIA,meanLF,meanBLL]
    
    # set up dict to return
    results = {'subj':{'subjID':list(),
                       'subjMeanRTs':list(),
                       'subjMeanAcc':list()},
               'models':{}}
    
    for i in range(0,len(estResults['partID'])):
        
        part = estResults['partID'][i]
        print(part)
        
        #get subject data
        subjResponses = read_participant_data('/home/pjrice/gp/ACTR-WM/data/beh/zb/'+part+'/zbResp.csv')
        
        [subj_totAccVec,subj_tarAccVec,subj_lurAccVec,subj_nlrAccVec] = compute_acc(correctResponses,subjResponses)
        
        subjRTs = np.array([x[1] for x in subjResponses], dtype=np.float)
        np.nan_to_num(subjRTs, copy=False, nan=np.nanmean(subjRTs))
        
        #get estimated parameter values
        ga = estResults['ga'][i]
        ia = estResults['ia'][i]
        lf = estResults['lf'][i]
        bll = estResults['bll'][i]
        
        parList = [ga,ia,lf,bll]
        
        # get predicted mean RT and mean accuracy, sequentially adding parameters
        subjResults = incrementalParsModelPredictions(parList,meanPars,subjRTs,subj_totAccVec,stimTiming,targetTypes,correctCueChunks,nRuns)
        
        # add this subject's mean responses and model results to dict
        modelKeys = list(subjResults['models'].keys())
        outputKeys = list(subjResults['models'][modelKeys[0]].keys())
        
        if i==0:
            for modelKey in modelKeys:
                results['models'][modelKey] = {}
                for outputKey in outputKeys:
                    results['models'][modelKey][outputKey] = list()
        
        for modelKey in modelKeys:
            for outputKey in outputKeys:
                results['models'][modelKey][outputKey].append(subjResults['models'][modelKey][outputKey])
                
        results['subj']['subjID'].append(part)
        results['subj']['subjMeanRTs'].append(np.mean(subjRTs))
        results['subj']['subjMeanAcc'].append(np.mean(subj_totAccVec))

    return(results)
    
    

               
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        



        