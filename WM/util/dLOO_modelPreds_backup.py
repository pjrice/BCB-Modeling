




def dLOO_ModelPredictions (parNames,parCombos,estPars,meanPars,subjRTs,subj_totAccVec,stimTiming,targetTypes,correctCueChunks,nRuns):
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
        
        missingPar = [parName for parName in parNames if parName not in parCombo]
            
        print('Getting model predictions including '+separator1.join(parCombo)+' parameters, "leaving out" '+missingPar[0]+'...')
        dictKey = separator2.join(parCombo)
            
        temp_tbtRTs = list()
        temp_tbtAccs = list()
        for ii in range(0,nRuns):
            print('Run ', ii+1)
            actr.load_act_r_model("/home/pjrice/gp/ACTR-WM/code/models/zeroBack/zeroBack-model-main.lisp")
            
            # set parameters to either the mean value or the estimated value, "leaving one out" (set to mean) on each iteration of runs
            setACTR_parVal(missingPar[0],meanPars[missingPar[0]]) # first set the "left out" parameter to the mean value
            #loop over parameters in parCombo to set
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
            