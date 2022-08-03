
import csv
import numpy as np
from scipy.stats import zscore


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]  

def read_correct_responses (fName):
    """Read the file containing the correct responses from the HCP N-Back task."""
    outList = list()
    with open(fName) as csvfile:
        fReader = csv.reader(csvfile)
        for row in fReader:
            outList.append(row)
    return(outList)

def read_participant_data (fName):
    """Read the file containing the participant's responses from the HCP N-Back task."""
    outList = list()
    with open(fName) as csvfile:
        fReader = csv.reader(csvfile)
        for row in fReader:
            outList.append(row)
    outList = [x if x[0] != '' else [None,None,x[2]] for x in outList]
    return(outList)

def compute_acc (correctResponses,responses):
    """Computes accuracy of the participant by comparing the participant's list
    of responses ('j'==nontarget; 'f'==target) to the list of correct responses."""
    
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
        nontarget stimulus). Should be used for the zero-back model only."""
    
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

def compute_model_acc_combined (correctResponses,modelResponses,correctRespChunks,retrievalRespChunks,targetTypes):
    """Computes the accuracy of the model by first comparing the model's keypress responses
        to the correct keypress responses, and then by comparing the chunks that were in the
        retrieval buffer at time of response to the 'correct' chunk that 'should' have been
        in the retrieval buffer at time of response. Combines these measures by using whatever
        the keypress response accuracy for a trial was, unless the chunk comparison accuracy
        for that trial was incorrect, in which case the model is marked as incorrect on that
        trial. Should be used for the two-back model only."""
    
    keypressRespAccVec = [1 if i[0]==j[0] else 0 for i,j in zip(correctResponses,modelResponses)]
    
    chunkAccVec = [1 if i==j else 0 for i,j in zip(correctRespChunks,retrievalRespChunks)]
    
    combinedAccVec = [i if j==1 else 0 for i,j in zip(keypressRespAccVec,chunkAccVec)]
    
    combinedAccVecTT = [[i,j] for i,j in zip(combinedAccVec,targetTypes)]
    
    tarAccVec = [x[0] for x in combinedAccVecTT if x[1]=='target']
    lurAccVec = [x[0] for x in combinedAccVecTT if x[1]=='lure']
    nlrAccVec = [x[0] for x in combinedAccVecTT if x[1]=='nonlure']
    
    return([combinedAccVec,tarAccVec,lurAccVec,nlrAccVec])

def zscore_wrt (signal1, signal2):
    """zscores signal 1, and zscores signal 2 with respect to signal 1 (that is,
    uses signal1's mean/std to zscore signal2)."""
    
    normSig1 = zscore(signal1, nan_policy='omit')
    
    meanSig1 = np.nanmean(signal1)
    stdSig1 = np.nanstd(signal1)
    
    normSig2 = (signal2 - meanSig1)/stdSig1
    
    return(normSig1,normSig2)

def create_stim_timing():
    """Create a list containing the times of stimulus presentation (in seconds)
    for the HCP N-Back task. Includes the 24-hour gap between the first and 
    second sessions. Currently, only the timing for the zero-back condition is
    implemented."""
    
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