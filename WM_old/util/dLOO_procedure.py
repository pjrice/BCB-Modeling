


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


def dLOO_ModelPredictions (parNames,poppedParNames,parCombos,estPars,meanPars,subjRTs,subj_totAccVec,stimTiming,targetTypes,correctCueChunks,nRuns):
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
        
        leftOutPar = [parName for parName in poppedParNames if parName not in parCombo]
        droppedPars = [parName for parName in parNames if parName not in parCombo and parName not in leftOutPar]
        
            
        print('Getting model predictions including '+separator1.join(parCombo)+' parameters, "leaving out" '+leftOutPar[0]+', with formerly "dropped" parameters '+separator1.join(droppedPars)+'...')
        dictKey = separator2.join(parCombo)
            
        temp_tbtRTs = list()
        temp_tbtAccs = list()
        for ii in range(0,nRuns):
            print('Run ', ii+1)
            actr.load_act_r_model("/home/pjrice/gp/ACTR-WM/code/models/zeroBack/zeroBack-model-main.lisp")
            
            # set parameters to either the mean value or the estimated value, "leaving one out" (set to mean) on each iteration of runs
            setACTR_parVal(leftOutPar[0],meanPars[leftOutPar[0]]) # first set the "left out" parameter to the mean value
            # set the formerly "dropped" parameters to mean values
            if len(droppedPars)!=0:
                for par2set in droppedPars:
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
            
 

def parameterVarExp_dLOO (estResults,nRuns=100):
    """For each participant, runs the incremental model procedure. Returns each participant's
    mean RT and mean accuracy in subjMeasures, and the set of model's predicted mean RTs and mean 
    accuracies in modelPredictions."""
    
    actr.load_act_r_code("/home/pjrice/gp/ACTR-WM/code/models/zeroBack/zeroBack-device.lisp")
    
    correctResponses = read_correct_responses("/home/pjrice/gp/ACTR-WM/data/zeroBack_correctResponses.csv")
    
    correctCueChunks = np.array(['CUE0-0','CUE1-0','CUE2-0','CUE3-0','CUE4-0','CUE5-0','CUE6-0','CUE7-0'])
    correctCueChunks = np.repeat(correctCueChunks,10,axis=0).tolist()
    
    targetTypes = [x[1] for x in correctResponses]
    
    stimTiming = create_stim_timing()
    
    separator = ','
    
    #parameter names
    parNames = ['bll','ga','ia','lf','css']
    parNames2pop = ['bll','ga','ia','lf','css']
    
    #get mean parameter values
    meanPars = {}
    for parName in parNames:
        meanPars[parName] = np.mean(estResults[parName])
    
    # set up dict to return
    results = {'subj':{'subjID':list(),
                       'subjMeanRTs':list(),
                       'subjMeanAcc':list()},
               'models':{}}
    
    # loop over the "whittling down" set of parameters, testing all permutations of n-1 out of n parameters (aka leave-one-out)
    for numPars in range(len(parNames)-1,0,-1):
        
        # make parameter permutations
        parCombos = list(itertools.combinations(parNames2pop,numPars))
        
        dictFlag=0
        
        # perform the leave-one-out procedure using this set of parameter combinations for each participant
        for i in range(0,len(estResults['partID'])):
            
            part = estResults['partID'][i]
            print(part)
            
            #skip the "bad trial order" participants
            if part in ["sub-103515", "sub-121618", "sub-126325", "sub-137936", "sub-150726", "sub-154936", "sub-157437", "sub-159239", "sub-172029", "sub-172332", "sub-992774"]:
                continue
        
            #get subject data
            subjResponses = read_participant_data('/home/pjrice/gp/ACTR-WM/data/beh/zb/'+part+'/zbResp.csv')
        
            [subj_totAccVec,subj_tarAccVec,subj_lurAccVec,subj_nlrAccVec] = compute_acc(correctResponses,subjResponses)
        
            subjRTs = np.array([x[1] for x in subjResponses], dtype=np.float)
            np.nan_to_num(subjRTs, copy=False, nan=np.nanmean(subjRTs))
            
            # add subj data to results dict just once (on first loop through parameter sets)
            if numPars==len(parNames)-1:
                results['subj']['subjID'].append(part)
                results['subj']['subjMeanRTs'].append(np.mean(subjRTs))
                results['subj']['subjMeanAcc'].append(np.mean(subj_totAccVec))
            
            #get estimated parameter values
            estPars = {}
            for parName in parNames2pop:
                estPars[parName] = estResults[parName][i]
            
            # get predicted mean RTs and mean accuracies for this set of parameter combinations for this participant
            subjResults = dLOO_ModelPredictions(parNames,
                                                parNames2pop,
                                                parCombos,
                                                estPars,
                                                meanPars,
                                                subjRTs,
                                                subj_totAccVec,
                                                stimTiming,
                                                targetTypes,
                                                correctCueChunks,
                                                nRuns)
            
            # add this subject's mean responses and model results to dict
            modelKeys = list(subjResults['models'].keys())
            outputKeys = list(subjResults['models'][modelKeys[0]].keys())
        
            if dictFlag==0:
                for modelKey in modelKeys:
                    results['models'][modelKey] = {}
                    for outputKey in outputKeys:
                        results['models'][modelKey][outputKey] = list()
                dictFlag = 1
        
            for modelKey in modelKeys:
                for outputKey in outputKeys:
                    results['models'][modelKey][outputKey].append(subjResults['models'][modelKey][outputKey])
       
            
        # determine which of the parameter combos has the largest Rsquared
        rSquareds = {}
        for parCombo in parCombos:
            modelKey = separator.join(parCombo)
            rValRT = scipy.stats.pearsonr(results['subj']['subjMeanRTs'],results['models'][modelKey]['meanRT'])[0]
            rValAcc = scipy.stats.pearsonr(results['subj']['subjMeanAcc'],results['models'][modelKey]['meanAcc'])[0]
            
            rS_RT = rValRT**2
            rS_Acc = rValAcc**2
            mean_rS = np.mean([rS_RT,rS_Acc])
            rSquareds[modelKey] = mean_rS
         
        # gets the dictKey of the model with the largest mean rSquared
        bestModel = max(rSquareds, key=lambda key: rSquareds[key])
            
        # drop the parameter that wasn't inclued in the parameter combo with the largest Rsquared
        par2pop = [parName for parName in parNames2pop if parName not in bestModel.split(',')]
        popIdx = parNames2pop.index(par2pop[0])
        parNames2pop.pop(popIdx)
        
    return(results)
            