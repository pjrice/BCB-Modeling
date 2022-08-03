





import itertools

def setBLL (bll_val):
    actr.set_parameter_value(":bll", bll_val)
    
def setGA (ga_val):
    actr.set_parameter_value(":ga", ga_val)
    
def setIA (ia_val):
    actr.set_parameter_value(":imaginal-activation", ia_val) 

def setLF (lf_val):
    actr.set_parameter_value(":lf", lf_val)
    
def setCSS (css_val):
    actr.call_command('set-similarities', ['cue', 'stimulus', css_val])
    
def setACTR_parVal (parName,parVal):
    switcher = {
        'bll':setBLL,
        'ga':setGA,
        'ia':setIA,
        'lf':setLF,
        'css':setCSS
        }
    
    #get function from switcher dictionary
    func = switcher.get(parName, lambda: "Invalid parameter name")
    func(parVal)


def produceModelPredictions (parNames,parCombos,estPars,meanPars,subjRTs,subj_totAccVec,stimTiming,targetTypes,correctCueChunks,nRuns):
    """Runs five total models 100 times each. Each model iteration includes n-1 estimated parameters, (where
    n is the number of estimated parameters) with the "left out" parameter set to the mean of the estimated parameter
    (across the group). Computes the the mean trial-by-trial RTs and accuracies (across runs), and returns the mean
    RT and accuracy (across run-averaged trials). Also computes the Pearson's r and p-value between the model+subject 
    trial-by-trial RTs and accuracies, as well as the condition-wise (target/lure/nonlure and block-wise) accuracies."""
    
    #set up output dictionary
    results = {'models':{}}
    
    #get the participant's target, lure, and nonlure mean accuracies
    subj_tarAcc = np.mean([i for i,j in zip(subj_totAccVec,targetTypes) if j=='target'])
    subj_lurAcc = np.mean([i for i,j in zip(subj_totAccVec,targetTypes) if j=='lure'])
    subj_nlrAcc = np.mean([i for i,j in zip(subj_totAccVec,targetTypes) if j=='nonlure'])
        
    #get the block-by-block model accs
    subjAcc_byBlock = [np.mean(x) for x in chunks(subj_totAccVec,10)]
    
    subjAccVec = np.concatenate((subj_tarAcc,subj_lurAcc,subj_nlrAcc,subjAcc_byBlock), axis=None)
    
    #for print diagnostics/dictKeys
    separator1 = ', '
    separator2 = ','
    
    for parCombo in parCombos:
        
        leftOutPars = [parName for parName in parNames if parName not in parCombo]
            
        print('Getting model predictions including '+separator1.join(parCombo)+' parameters, "leaving out" '+separator1.join(leftOutPars)+'...')
        dictKey = separator2.join(parCombo)
            
        temp_tbtRTs = list()
        temp_tbtAccs = list()
        meanRTdiffs = list()
        meanAccdiffs = list()
        for ii in range(0,nRuns):
            print('Run ', ii+1)
            actr.load_act_r_model("/home/pjrice/gp/ACTR-WM/code/models/zeroBack/zeroBack-model-main.lisp")
            
            # set the "left out" parameters to mean values
            if len(leftOutPars)!=0:
                for par2set in leftOutPars:
                    setACTR_parVal(par2set,meanPars[par2set])
            #loop over parameters in parCombo to set (these are the ones estimated for the participant)
            for par2set in parCombo:
                setACTR_parVal(par2set,estPars[par2set])
            
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
            
            #calculate the difference between mean model RT/Acc and mean participant RT/Acc for this run
            tempRun_RTdiff = np.mean(modelRTs) - np.mean(subjRTs)
            meanRTdiffs.append(tempRun_RTdiff)
            tempRun_Accdiff = np.mean(model_totAccVec) - np.mean(subj_totAccVec)
            meanAccdiffs.append(tempRun_Accdiff)
            
        #get the trial-by-trial mean RTs/Accs across runs
        tbtModelRTs = np.mean(np.array(temp_tbtRTs),axis=0)
        tbtModelAccs = np.mean(np.array(temp_tbtAccs),axis=0)
        
        #get the model's target, lure, and nonlure mean RTs
        model_tarRT = np.mean([i for i,j in zip(tbtModelRTs,targetTypes) if j=='target'])
        model_lurRT = np.mean([i for i,j in zip(tbtModelRTs,targetTypes) if j=='lure'])
        model_nlrRT = np.mean([i for i,j in zip(tbtModelRTs,targetTypes) if j=='nonlure'])
        
        #get the block-by-block model RTs
        modelRT_byBlock = [np.mean(x) for x in chunks(tbtModelRTs,10)]
        
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
        
        #get the standard deviation (across runs) of the mean tbt RTs/Accs (so, the mean of each run is found, and then compute std across runs)
        sdModelRT = np.std(np.mean(np.array(temp_tbtRTs),axis=1))
        sdModelAcc = np.std(np.mean(np.array(temp_tbtAccs),axis=1))
        
        results['models'][dictKey] = {'meanRT':meanModelRT, 
                                      'meanAcc':meanModelAcc,
                                      'sdRTAcrossRuns':sdModelRT,
                                      'sdAccAcrossRuns':sdModelAcc,
                                      'mean_tarRT':model_tarRT,
                                      'mean_lurRT':model_lurRT,
                                      'mean_nlrRT':model_nlrRT,
                                      'mean_tarAcc':model_tarAcc,
                                      'mean_lurAcc':model_lurAcc,
                                      'mean_nlrAcc':model_nlrAcc,
                                      'mean_blockRT':modelRT_byBlock,
                                      'mean_blockAcc':modelAcc_byBlock,
                                      'RT_corr':RT_pearsonr[0],
                                      'RT_pval':RT_pearsonr[1],
                                      'Acc_corr':Acc_pearsonr[0],
                                      'Acc_pval':Acc_pearsonr[1],
                                      'cwAcc_corr':cwAcc_pearsonr[0],
                                      'cwAcc_pval':cwAcc_pearsonr[1],
                                      'meanRTdiffs':meanRTdiffs,
                                      'meanAccdiffs':meanAccdiffs}
            
    return(results)
            
 

def allModelPredictions (estResults,nRuns=100):
    """For each participant, runs the incremental model procedure. Returns each participant's
    mean RT and mean accuracy in subjMeasures, and the set of model's predicted mean RTs and mean 
    accuracies in modelPredictions."""
    
    actr.load_act_r_code("/home/pjrice/gp/ACTR-WM/code/models/zeroBack/zeroBack-device.lisp")
    
    correctResponses = read_correct_responses("/home/pjrice/gp/ACTR-WM/data/zeroBack_correctResponses.csv")
    
    correctCueChunks = np.array(['CUE0-0','CUE1-0','CUE2-0','CUE3-0','CUE4-0','CUE5-0','CUE6-0','CUE7-0'])
    correctCueChunks = np.repeat(correctCueChunks,10,axis=0).tolist()
    
    targetTypes = [x[1] for x in correctResponses]
    
    stimTiming = create_stim_timing()
        
    #parameter names
    parNames = ['bll','ga','ia','lf','css']
    
    #get mean parameter values
    meanPars = {}
    for parName in parNames:
        meanPars[parName] = np.mean(estResults[parName])
    
    # set up dict to return
    results = {'subj':{'subjID':list(),
                       'subjMeanRTs':list(),
                       'subjMeanAcc':list(),
                       'subj_mean_tarRT':list(),
                       'subj_mean_lurRT':list(),
                       'subj_mean_nlrRT':list(),
                       'subj_mean_tarAcc':list(),
                       'subj_mean_lurAcc':list(),
                       'subj_mean_nlrAcc':list(),
                       'subj_mean_blockRT':list(),
                       'subj_mean_blockAcc':list()},
               'models':{}}
    
    #create list of all parameter combinations
    tempParCombos = list()
    for numPars in range(1,len(parNames)+1):
        tempParCombos.append(list(itertools.combinations(parNames,numPars)))
    parCombos = list(itertools.chain(*tempParCombos))
        
        
    # produce model predictions for each model for each participant
    for i in range(0,len(estResults['partID'])):
            
        part = estResults['partID'][i]
        print(part)
        
        #get subject data
        subjResponses = read_participant_data('/home/pjrice/gp/ACTR-WM/data/beh/zb/'+part+'/zbResp.csv')
        
        [subj_totAccVec,subj_tarAccVec,subj_lurAccVec,subj_nlrAccVec] = compute_acc(correctResponses,subjResponses)
        
        subjAcc_byBlock = [np.mean(x) for x in chunks(subj_totAccVec,10)]
        
        subjRTs = np.array([x[1] for x in subjResponses], dtype=np.float)
        np.nan_to_num(subjRTs, copy=False, nan=np.nanmean(subjRTs))
        
        #get the participant's target, lure, and nonlure mean RTs
        subj_tarRT = np.mean([i for i,j in zip(subjRTs,targetTypes) if j=='target'])
        subj_lurRT = np.mean([i for i,j in zip(subjRTs,targetTypes) if j=='lure'])
        subj_nlrRT = np.mean([i for i,j in zip(subjRTs,targetTypes) if j=='nonlure'])
        
        subjRT_byBlock = [np.mean(x) for x in chunks(subjRTs,10)]
            
        # add subj data to results dict
        results['subj']['subjID'].append(part)
        results['subj']['subjMeanRTs'].append(np.mean(subjRTs))
        results['subj']['subjMeanAcc'].append(np.mean(subj_totAccVec))
        results['subj']['subj_mean_tarRT'].append(subj_tarRT)
        results['subj']['subj_mean_lurRT'].append(subj_lurRT)
        results['subj']['subj_mean_nlrRT'].append(subj_nlrRT)
        results['subj']['subj_mean_tarAcc'].append(np.mean(subj_tarAccVec))
        results['subj']['subj_mean_lurAcc'].append(np.mean(subj_lurAccVec))
        results['subj']['subj_mean_nlrAcc'].append(np.mean(subj_nlrAccVec))
        results['subj']['subj_mean_blockRT'].append(subjRT_byBlock)
        results['subj']['subj_mean_blockAcc'].append(subjAcc_byBlock)
            
        #get estimated parameter values
        estPars = {}
        for parName in parNames:
            estPars[parName] = estResults[parName][i]
            
        # get predicted mean RTs and mean accuracies for this set of parameter combinations for this participant
        subjResults = produceModelPredictions(parNames,
                                              parCombos,
                                              estPars,
                                              meanPars,
                                              subjRTs,
                                              subj_totAccVec,
                                              stimTiming,
                                              targetTypes,
                                              correctCueChunks,
                                              nRuns)
            
        # add model results to dict
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
       
            
        
    return(results)
            