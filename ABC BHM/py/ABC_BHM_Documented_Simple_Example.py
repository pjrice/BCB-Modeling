import math
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

def hammy_sammy(indiv1Hist, indiv2Hist, sample, samplePrev, i):
    return hamiltonian_sampling(indiv1Hist, indiv2Hist, sample, samplePrev, i)

def hamiltonian_sampling(indiv1Hist, indiv2Hist, sample, samplePrev, i):
    """
    Computes the likelihood ratio for the population parameter.

    Parameters
    ----------
    indiv1Hist : A list of posterior samples representing an individual.
    indiv2Hist : A list of posterior samples representing a second individual.
    sample     : The current population mean parameter.
    samplePrev : The previously accepted population mean parameter.
    i          : Index of the iteration of the Markov Chain.

    Returns
    -------
    llhRatio   : The likelihood ratio for the population parameter.

    """
    
    # compute the likelihood ratio between the previous sample of the parameter and the current sample 
    # kappa = 2 (fixed; only estimating mu)
    currSample = sum(beta.logpdf([indiv1Hist[i-1],indiv2Hist[i-1]], sample*2, (1-sample)*2)) # current likelihood value
    prevSample = sum(beta.logpdf([indiv1Hist[i-1],indiv2Hist[i-1]], samplePrev*2, (1-samplePrev)*2)) # previous likelihood value
    llhRatio   = currSample - prevSample # likelihood ratio
    return llhRatio

def markov_chain(tuning, DV):
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
    
    sampleHist = []
    indiv1Hist = []
    indiv2Hist = []
    for i in range (0,10000):
        print("Run number "+str(i))
        
        # estimate the sample parameter
        if i==0: # initialize sample parameter from the prior
            sample = sample_prior()
        else: # determine sample parameter via Hamiltonian sampling
            sample = sample_prior()
            samplePrev = sampleHist[i-1]
            
            # get the likelihood ratio between the current and previous samples
            r = hammy_sammy(indiv1Hist,indiv2Hist,sample,samplePrev,i)
            
            # if the likelihood ratio is less than or equal to some randomly sampled value,
            # keep the newly sampled parameter value; otherwise, keep the previously sampled parameter value
            if math.log(uniform.rvs(0,1,1)) <= r: # check
                pass
            else:
                sample = [samplePrev]
                
        # sample parameters for individual participants
        # in this example the rate parameter is held constant
        indiv1 = beta.rvs(sample[0]*10, (1-sample[0])*10, size=1)
        indiv2 = beta.rvs(sample[0]*10, (1-sample[0])*10, size=1)
            
        ###
        # integrate ACT-R here
        # (probably) don't have to integrate behavioral measures! 
        # just calculate the residual for each measure, then when alpha is checked against p, it has to pass checks
        # for each of the behavioral measures to be kept
        ###
            
        #compute residual between model predictions and observed data
        dist1 = np.sqrt(np.mean((DV[0:50] - indiv1[0])**2))
        dist2 = np.sqrt(np.mean((DV[51:100] - indiv2[0])**2))
            
        #add residuals from all participants
        dist = dist1 + dist2
            
        # initialize distPost to 0
        if i==0:
            distPost = 0.01
            
        # compute likelihood ratio for ABC sampling
        #alpha = norm.logpdf(dist/tuning) - norm.logpdf(distPost/tuning)
        alpha = math.log(norm.pdf(dist/tuning)) - math.log(norm.pdf(distPost/tuning))
        # sample a random value to test against
        p = math.log(uniform.rvs(0,1,1))
            
        if i==0:
            sampleHist.append(sample[0])
            indiv1Hist.append(indiv1[0])
            indiv2Hist.append(indiv2[0])
            distPost = dist
        else:
            if p <= alpha: # if p is less than or equal to alpha, store newly sampled values
                sampleHist.append(sample[0])
                indiv1Hist.append(indiv1[0])
                indiv2Hist.append(indiv2[0])
                distPost = dist
            else: # otherwise store the previously sampled values again
                sampleHist.append(sampleHist[i-1])
                indiv1Hist.append(indiv1Hist[i-1])
                indiv2Hist.append(indiv2Hist[i-1])
                    
    # store chain as dict
    chain = {"Sample":list(range(0,len(sampleHist))),
             "SampleMean":sampleHist,
             "Individual_1":indiv1Hist,
             "Individual_2":indiv2Hist}
    return chain


def abc_hierarchical_model(tuning, dv):
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
    chain1 = pd.DataFrame(markov_chain(tuning,dv))
    chain2 = pd.DataFrame(markov_chain(tuning,dv))
    chain3 = pd.DataFrame(markov_chain(tuning,dv))
    
    chain1['Chain'] = 1
    chain2['Chain'] = 2
    chain3['Chain'] = 3
    
    data = pd.concat([chain1,chain2,chain3],ignore_index=True)
    return data



# generate data
part = [1]*50 + [2]*50
dv = [.3]*50 + [.7]*50
dv = list(truncnorm.rvs(a=0, b=1, loc=0.3, scale=0.05, size=50)) + list(truncnorm.rvs(a=0, b=1, loc=0.7, scale=0.05, size=50))

partData = {"partID":part,
            "dvSteady":[.3]*50 + [.7]*50,
            "dv":dv
    }

tuning05 = abc_hierarchical_model(.05,dv)
tuning10 = abc_hierarchical_model(.1,dv)
tuning15 = abc_hierarchical_model(.15,dv)   
tuning20 = abc_hierarchical_model(.2,dv)

tuning05.to_csv('/Users/pjr5/Desktop/BCB-Modeling-main/ABC BHM R Code/pyData/tuning05.csv')    
tuning10.to_csv('/Users/pjr5/Desktop/BCB-Modeling-main/ABC BHM R Code/pyData/tuning10.csv')    
tuning15.to_csv('/Users/pjr5/Desktop/BCB-Modeling-main/ABC BHM R Code/pyData/tuning15.csv')    
tuning20.to_csv('/Users/pjr5/Desktop/BCB-Modeling-main/ABC BHM R Code/pyData/tuning20.csv')    

partData = pd.DataFrame(partData)
partData.to_csv('/Users/pjr5/Desktop/BCB-Modeling-main/ABC BHM R Code/pyData/partData.csv')
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    