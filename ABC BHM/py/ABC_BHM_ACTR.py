import actr
import modelFuncs
import math
import subprocess
import multiprocessing
import numpy as np
import pandas as pd
from scipy.stats import beta
from scipy.stats import norm
from scipy.stats import uniform
from scipy.stats import truncnorm

def sample_prior():
    """Returns a list of parameter value samples from a beta distribution with flat priors"""
    parameters = beta.rvs(1,1,size=1)
    return parameters

def hamiltonian_sampling(indiv1Hist, indiv2Hist, sample, samplePrev, popKappa, i):
    """
    Computes the likelihood ratio for the population parameter.

    Parameters
    ----------
    indiv1Hist : A list of posterior samples representing an individual.
    indiv2Hist : A list of posterior samples representing a second individual.
    sample     : The current population mean parameter.
    samplePrev : The previously accepted population mean parameter.
    popKappa   : The current population kappa parameter.
    i          : Index of the iteration of the Markov Chain.

    Returns
    -------
    llhRatio   : The likelihood ratio for the population parameter.

    """
    
    # compute the likelihood ratio between the previous sample of the parameter and the current sample 
    currSample = sum(beta.logpdf([indiv1Hist[i-1],indiv2Hist[i-1]], sample*popKappa, (1-sample)*popKappa)) # current likelihood value
    prevSample = sum(beta.logpdf([indiv1Hist[i-1],indiv2Hist[i-1]], samplePrev*popKappa, (1-samplePrev)*popKappa)) # previous likelihood value
    llhRatio   = currSample - prevSample # likelihood ratio
    return llhRatio

def markov_chain(params, DV=None, numChainIter=1):
    """
    Runs a single instance of a Markov Chain for a given model.

    Parameters
    ----------
    tuning : Tuning parameter for the ABC sampling algorithm.
    DV     : Dependent variable; the data that the model is being fit to.

    Returns
    -------
    chain : The estimated model parameter values from a single Markov Chain.

    """
    
    # get model parameter values
    tuning = params['tuning']
    indivKappa = params['indiv_kappa']
    popKappa = params['pop_kappa']
    
    
    #indiv1Data = pd.read_csv('Z:\\gp\\BCB-Modeling\\WM_ABCest\\data\\modelPreds_part1.csv')
    indiv1Data = pd.read_csv('Z:\\gp\\BCB-Modeling\\ABC BHM\\py\\pyData\\parameterRecovery\\test3\\modelPreds_ga40.csv')
    # indiv1RT_real = np.mean(indiv1Data['rt'])
    # indiv1Acc_real = np.mean(indiv1Data['kpAcc'])
    
    #indiv2Data = pd.read_csv('Z:\\gp\\BCB-Modeling\\WM_ABCest\\data\\modelPreds_part2.csv')
    indiv2Data = pd.read_csv('Z:\\gp\\BCB-Modeling\\ABC BHM\\py\\pyData\\parameterRecovery\\test3\\modelPreds_ga93.csv')
    # indiv2RT_real = np.mean(indiv2Data['rt'])
    # indiv2Acc_real = np.mean(indiv2Data['kpAcc'])
    
    
    sampleHist = []
    indiv1Hist = []
    indiv2Hist = []
    model_meanRTs_indiv1 = []
    model_meanAccs_indiv1 = []
    model_meanRTs_indiv2 = []
    model_meanAccs_indiv2 = []
    
    # open ACT-R
    #subprocess.call([r'Z:\\gp\\BCB-Modeling\\ABC BHM\\py\\run-act-r.bat'])
    #import actr
    #import modelFuncs
    
    # load the device
    actr.load_act_r_code('Z:\\gp\\BCB-Modeling\\WM_ABCest\\model\\zeroBack-device.lisp')
    
    for i in range (0,numChainIter):
        print("Run number "+str(i))
        
        # estimate the sample parameter
        if i==0: # initialize sample parameter from the prior
            sample = sample_prior()
        else: # determine sample parameter via Hamiltonian sampling
            sample = sample_prior()
            samplePrev = sampleHist[i-1]
            
            # get the likelihood ratio between the current and previous samples
            r = hamiltonian_sampling(indiv1Hist,indiv2Hist,sample,samplePrev,popKappa,i)
            
            # if the likelihood ratio is less than or equal to some randomly sampled value,
            # keep the newly sampled parameter value; otherwise, keep the previously sampled parameter value
            if math.log(uniform.rvs(0,1,1)) <= r: # check
                pass
            else:
                sample = [samplePrev]
                
        # sample parameters for individual participants
        # in this example the rate parameter is held constant
        indiv1 = beta.rvs(sample[0]*indivKappa, (1-sample[0])*indivKappa, size=1)
        indiv2 = beta.rvs(sample[0]*indivKappa, (1-sample[0])*indivKappa, size=1)
            
        ###
        # integrate ACT-R here
        # here we have drawn sample parameters for each individual; 
        # need to run the model with each of these parameters, 
        # get the model's behavior, 
        # and subsequently compute the residual between each individual model parameterization and each individual
        
        # this will cause issues with large numbers of participants/chain iterations - each participant's act-r model has to be run on each chain iteration
        paramDict = {':ga':indiv1[0], ':imaginal-activation':0.69, ':lf':2.49, ':bll': 0.52, 'css':-0.43}
        indiv1Dict = modelFuncs.run_model_with_params('Z:\\gp\\BCB-Modeling\\WM_ABCest\\model\\zeroBack-model-main.lisp',paramDict)
        
        paramDict = {':ga':indiv2[0], ':imaginal-activation':0.69, ':lf':2.49, ':bll': 0.52, 'css':-0.43}
        indiv2Dict = modelFuncs.run_model_with_params('Z:\\gp\\BCB-Modeling\\WM_ABCest\\model\\zeroBack-model-main.lisp',paramDict)
        
        model_meanRT_indiv1 = np.mean(indiv1Dict['RTs'])
        model_meanAcc_indiv1 = np.mean(indiv1Dict['keypressAcc'])
        
        model_meanRT_indiv2 = np.mean(indiv2Dict['RTs'])
        model_meanAcc_indiv2 = np.mean(indiv2Dict['keypressAcc'])
        
        ###
        
        # right now, r squared computed on trial-by-trial basis; instead compute over the vectors of participant RT/Acc means?
        
        #compute residual between model predictions and observed data
        dist1_RT = np.sqrt(np.mean((indiv1Data['rt'] - indiv1Dict['RTs'])**2))
        dist1_Acc = np.sqrt(np.mean((indiv1Data['kpAcc'] - indiv1Dict['keypressAcc'])**2))
        
        dist2_RT = np.sqrt(np.mean((indiv2Data['rt'] - indiv2Dict['RTs'])**2))
        dist2_Acc = np.sqrt(np.mean((indiv2Data['kpAcc'] - indiv2Dict['keypressAcc'])**2))
        
        # add residuals from all participants
        dist_RT = dist1_RT + dist2_RT
        dist_Acc = dist1_Acc + dist2_Acc
            
        # #compute residual between model predictions and observed data
        # dist1 = np.sqrt(np.mean((DV[0:50] - indiv1[0])**2))
        # dist2 = np.sqrt(np.mean((DV[51:100] - indiv2[0])**2))
            
        # #add residuals from all participants
        # dist = dist1 + dist2
            
        # initialize distPost to 0
        if i==0:
            distPost_RT = 0.01
            distPost_Acc = 0.01
            
        # compute likelihood ratio for ABC sampling
        alpha_RT = math.log(norm.pdf(dist_RT/tuning)) - math.log(norm.pdf(distPost_RT/tuning))
        alpha_Acc = math.log(norm.pdf(dist_Acc/tuning)) - math.log(norm.pdf(distPost_Acc/tuning)) # different tuning vals for RT and Acc?
        # sample a random value to test against
        p = math.log(uniform.rvs(0,1,1))
            
        if i==0:
            sampleHist.append(sample[0])
            indiv1Hist.append(indiv1[0])
            indiv2Hist.append(indiv2[0])
            model_meanRTs_indiv1.append(model_meanRT_indiv1)
            model_meanAccs_indiv1.append(model_meanAcc_indiv1)
            model_meanRTs_indiv2.append(model_meanRT_indiv2)
            model_meanAccs_indiv2.append(model_meanAcc_indiv2)
            distPost_RT = dist_RT
            distPost_Acc = dist_Acc
        else:                                        #  This would necessitate a greater number of chain iterations, correct?
            if (p <= alpha_RT) and (p <= alpha_Acc): # if p is less than or equal to both RT and Acc alphas, store newly sampled values
                sampleHist.append(sample[0])
                indiv1Hist.append(indiv1[0])
                indiv2Hist.append(indiv2[0])
                model_meanRTs_indiv1.append(model_meanRT_indiv1)
                model_meanAccs_indiv1.append(model_meanAcc_indiv1)
                model_meanRTs_indiv2.append(model_meanRT_indiv2)
                model_meanAccs_indiv2.append(model_meanAcc_indiv2)
                distPost_RT = dist_RT
                distPost_Acc = dist_Acc
            else: # otherwise store the previously sampled values again
                sampleHist.append(sampleHist[i-1])
                indiv1Hist.append(indiv1Hist[i-1])
                indiv2Hist.append(indiv2Hist[i-1])
                model_meanRTs_indiv1.append(model_meanRTs_indiv1[i-1])
                model_meanAccs_indiv1.append(model_meanAccs_indiv1[i-1])
                model_meanRTs_indiv2.append(model_meanRTs_indiv2[i-1])
                model_meanAccs_indiv2.append(model_meanAccs_indiv2[i-1])
                    
    # store chain as dict
    chain = {"Sample":list(range(0,len(sampleHist))),
             "SampleMean":sampleHist,
             "ModelMeanRT_indiv1":model_meanRTs_indiv1,
             "ModelMeanAcc_indiv1":model_meanAccs_indiv1,
             "ModelMeanRT_indiv2":model_meanRTs_indiv2,
             "ModelMeanAcc_indiv2":model_meanAccs_indiv2,
             "Individual_1":indiv1Hist,
             "Individual_2":indiv2Hist}
    
    # close lisp terminal
    # works as a standalone call, but causes python to hang; when called in script, causes python->actr connection to fail
    #actr.call_command('quit-lisp-terminal')
    
    return chain


def abc_hierarchical_model(params, dv=None, numChainIter=1):
    """
    Runs a set of Markov Chains for a given model.

    Parameters
    ----------
    tuning : Tuning parameter for the ABC sampling algorithm.
    DV     : Dependent variable; the data that the model is being fit to.

    Returns
    -------
    data : The results of the ABC hierarchical sampling model.

    """    
    chain1 = pd.DataFrame(markov_chain(params,dv,numChainIter))
    chain2 = pd.DataFrame(markov_chain(params,dv,numChainIter))
    chain3 = pd.DataFrame(markov_chain(params,dv,numChainIter))
    
    chain1['Chain'] = 1
    chain2['Chain'] = 2
    chain3['Chain'] = 3
    
    data = pd.concat([chain1,chain2,chain3],ignore_index=True)
    return data

################################################################################################################################################
################################################################################################################################################
################################################################################################################################################
################################################################################################################################################


def markov_chain_RTonly(params, DV=None, numChainIter=1):
    """
    Runs a single instance of a Markov Chain for a given model.

    Parameters
    ----------
    tuning : Tuning parameter for the ABC sampling algorithm.
    DV     : Dependent variable; the data that the model is being fit to.

    Returns
    -------
    chain : The estimated model parameter values from a single Markov Chain.

    """
    
    # get model parameter values
    tuning = params['tuning']
    indivKappa = params['indiv_kappa']
    popKappa = params['pop_kappa']
    
    
    #indiv1Data = pd.read_csv('Z:\\gp\\BCB-Modeling\\WM_ABCest\\data\\modelPreds_part1.csv')
    indiv1Data = pd.read_csv('Z:\\gp\\BCB-Modeling\\ABC BHM\\py\\pyData\\parameterRecovery\\test3\\modelPreds_ga40.csv')
    # indiv1RT_real = np.mean(indiv1Data['rt'])
    # indiv1Acc_real = np.mean(indiv1Data['kpAcc'])
    
    #indiv2Data = pd.read_csv('Z:\\gp\\BCB-Modeling\\WM_ABCest\\data\\modelPreds_part2.csv')
    indiv2Data = pd.read_csv('Z:\\gp\\BCB-Modeling\\ABC BHM\\py\\pyData\\parameterRecovery\\test3\\modelPreds_ga93.csv')
    # indiv2RT_real = np.mean(indiv2Data['rt'])
    # indiv2Acc_real = np.mean(indiv2Data['kpAcc'])
    
    
    sampleHist = []
    indiv1Hist = []
    indiv2Hist = []
    model_meanRTs_indiv1 = []
    model_meanAccs_indiv1 = []
    model_meanRTs_indiv2 = []
    model_meanAccs_indiv2 = []
    
    # open ACT-R
    #subprocess.call([r'Z:\\gp\\BCB-Modeling\\ABC BHM\\py\\run-act-r.bat'])
    #import actr
    #import modelFuncs
    
    # load the device
    actr.load_act_r_code('Z:\\gp\\BCB-Modeling\\WM_ABCest\\model\\zeroBack-device.lisp')
    
    for i in range (0,numChainIter):
        print("Run number "+str(i))
        
        # estimate the sample parameter
        if i==0: # initialize sample parameter from the prior
            sample = sample_prior()
        else: # determine sample parameter via Hamiltonian sampling
            sample = sample_prior()
            samplePrev = sampleHist[i-1]
            
            # get the likelihood ratio between the current and previous samples
            r = hamiltonian_sampling(indiv1Hist,indiv2Hist,sample,samplePrev,popKappa,i)
            
            # if the likelihood ratio is less than or equal to some randomly sampled value,
            # keep the newly sampled parameter value; otherwise, keep the previously sampled parameter value
            if math.log(uniform.rvs(0,1,1)) <= r: # check
                pass
            else:
                sample = [samplePrev]
                
        # sample parameters for individual participants
        # in this example the rate parameter is held constant
        indiv1 = beta.rvs(sample[0]*indivKappa, (1-sample[0])*indivKappa, size=1)
        indiv2 = beta.rvs(sample[0]*indivKappa, (1-sample[0])*indivKappa, size=1)
            
        ###
        # integrate ACT-R here
        # here we have drawn sample parameters for each individual; 
        # need to run the model with each of these parameters, 
        # get the model's behavior, 
        # and subsequently compute the residual between each individual model parameterization and each individual
        
        # this will cause issues with large numbers of participants/chain iterations - each participant's act-r model has to be run on each chain iteration
        paramDict = {':ga':indiv1[0], ':imaginal-activation':0.69, ':lf':2.49, ':bll': 0.52, 'css':-0.43}
        indiv1Dict = modelFuncs.run_model_with_params('Z:\\gp\\BCB-Modeling\\WM_ABCest\\model\\zeroBack-model-main.lisp',paramDict)
        
        paramDict = {':ga':indiv2[0], ':imaginal-activation':0.69, ':lf':2.49, ':bll': 0.52, 'css':-0.43}
        indiv2Dict = modelFuncs.run_model_with_params('Z:\\gp\\BCB-Modeling\\WM_ABCest\\model\\zeroBack-model-main.lisp',paramDict)
        
        model_meanRT_indiv1 = np.mean(indiv1Dict['RTs'])
        model_meanAcc_indiv1 = np.mean(indiv1Dict['keypressAcc'])
        
        model_meanRT_indiv2 = np.mean(indiv2Dict['RTs'])
        model_meanAcc_indiv2 = np.mean(indiv2Dict['keypressAcc'])
        
        ###
        
        # right now, r squared computed on trial-by-trial basis; instead compute over the vectors of participant RT/Acc means?
        
        #compute residual between model predictions and observed data
        dist1_RT = np.sqrt(np.mean((indiv1Data['rt'] - indiv1Dict['RTs'])**2))
        
        dist2_RT = np.sqrt(np.mean((indiv2Data['rt'] - indiv2Dict['RTs'])**2))
        
        # add residuals from all participants
        dist_RT = dist1_RT + dist2_RT
            
        # #compute residual between model predictions and observed data
        # dist1 = np.sqrt(np.mean((DV[0:50] - indiv1[0])**2))
        # dist2 = np.sqrt(np.mean((DV[51:100] - indiv2[0])**2))
            
        # #add residuals from all participants
        # dist = dist1 + dist2
            
        # initialize distPost to 0
        if i==0:
            distPost_RT = 0.01
            
        # compute likelihood ratio for ABC sampling
        alpha_RT = math.log(norm.pdf(dist_RT/tuning)) - math.log(norm.pdf(distPost_RT/tuning))
        # sample a random value to test against
        p = math.log(uniform.rvs(0,1,1))
            
        if i==0:
            sampleHist.append(sample[0])
            indiv1Hist.append(indiv1[0])
            indiv2Hist.append(indiv2[0])
            model_meanRTs_indiv1.append(model_meanRT_indiv1)
            model_meanAccs_indiv1.append(model_meanAcc_indiv1)
            model_meanRTs_indiv2.append(model_meanRT_indiv2)
            model_meanAccs_indiv2.append(model_meanAcc_indiv2)
            distPost_RT = dist_RT
        else:                                        #  This would necessitate a greater number of chain iterations, correct?
            if (p <= alpha_RT): # if p is less than or equal to both RT and Acc alphas, store newly sampled values
                sampleHist.append(sample[0])
                indiv1Hist.append(indiv1[0])
                indiv2Hist.append(indiv2[0])
                model_meanRTs_indiv1.append(model_meanRT_indiv1)
                model_meanAccs_indiv1.append(model_meanAcc_indiv1)
                model_meanRTs_indiv2.append(model_meanRT_indiv2)
                model_meanAccs_indiv2.append(model_meanAcc_indiv2)
                distPost_RT = dist_RT
            else: # otherwise store the previously sampled values again
                sampleHist.append(sampleHist[i-1])
                indiv1Hist.append(indiv1Hist[i-1])
                indiv2Hist.append(indiv2Hist[i-1])
                model_meanRTs_indiv1.append(model_meanRTs_indiv1[i-1])
                model_meanAccs_indiv1.append(model_meanAccs_indiv1[i-1])
                model_meanRTs_indiv2.append(model_meanRTs_indiv2[i-1])
                model_meanAccs_indiv2.append(model_meanAccs_indiv2[i-1])
                    
    # store chain as dict
    chain = {"Sample":list(range(0,len(sampleHist))),
             "SampleMean":sampleHist,
             "ModelMeanRT_indiv1":model_meanRTs_indiv1,
             "ModelMeanAcc_indiv1":model_meanAccs_indiv1,
             "ModelMeanRT_indiv2":model_meanRTs_indiv2,
             "ModelMeanAcc_indiv2":model_meanAccs_indiv2,
             "Individual_1":indiv1Hist,
             "Individual_2":indiv2Hist}
    
    # close lisp terminal
    # works as a standalone call, but causes python to hang; when called in script, causes python->actr connection to fail
    #actr.call_command('quit-lisp-terminal')
    
    return chain


def abc_hierarchical_model_RTonly(params, dv=None, numChainIter=1):
    """
    Runs a set of Markov Chains for a given model.

    Parameters
    ----------
    tuning : Tuning parameter for the ABC sampling algorithm.
    DV     : Dependent variable; the data that the model is being fit to.

    Returns
    -------
    data : The results of the ABC hierarchical sampling model.

    """    
    chain1 = pd.DataFrame(markov_chain_RTonly(params,dv,numChainIter))
    chain2 = pd.DataFrame(markov_chain_RTonly(params,dv,numChainIter))
    chain3 = pd.DataFrame(markov_chain_RTonly(params,dv,numChainIter))
    
    chain1['Chain'] = 1
    chain2['Chain'] = 2
    chain3['Chain'] = 3
    
    data = pd.concat([chain1,chain2,chain3],ignore_index=True)
    return data



    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    