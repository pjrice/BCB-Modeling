#script to extract behavioral data from HCP raw data files, save to .RData file
library(dplyr)

dataDir = '/projects/commonModel/data/WM/'
sessions = c('ses-01', 'ses-02')

partIDs = list.dirs(dataDir, full.names=FALSE, recursive=FALSE)

dPrime = function(hit, fa) {
  
  # hit and fa are numeric vectors containing 1s and 0s
  # 1 represents the presence of a hit (i.e., the stimulus was a target, and the participant responded that it was) or the presence of a false alarm (the stimulus was a nonlure, but the participant responded target)
  # 0 represents the presence of a miss (i.e., the stimulus was a target, but the participant responded that it wasn't) or the presence of a correct negative (the stimulus was a nonlure, and the participant responded that it was)
  
  # qnorm() undefined at 0/1, so adjust perfect scores and scores of 0
  # perfect scores are adjusted as 1-(1/(2*n))
  # scores of zero are adjusted as 1/(2*n)
  # where n was the total number of hits/false alarms
  # according to Haatveit et al. 2010 The validity of d prime as a working memory index: Results from the “Bergen n-back task”
  
  #check for perfect score/score of 0 on hits
  if (sum(hit)==length(hit)) {
    hitProb = 1-(1/(2*length(hit)))
  } else if (sum(hit)==0) {
    hitProb = 1/(2*length(hit))
  } else {
    hitProb = sum(hit)/length(hit)
  }
  
  #check for perfect score/score of 0 on FAs
  if (sum(fa)==length(fa)) {
    faProb = 1-(1/(2*length(fa)))
  } else if (sum(fa)==0) {
    faProb = 1/(2*length(fa))
  } else {
    faProb = sum(fa)/length(fa)
  }
  
  # dPrime = Z_hit - Z_fa
  # Z_hit: hits when a signal is present (huts/(hits+misses))
  # Z_fa: proportion of false alarms when signal is absent (false alarms/(false alarms+correct negative))
  # both are z-transformed
  dPrime = qnorm(hitProb) - qnorm(faProb) 
  
  return(dPrime)
  
}


for (partID in partIDs) {
  
  cat(partID,'\n')
  
  for (sesh in sessions) {
    
    # if (sesh=='ses-01') {
    #   run = 'run1'
    # } else {
    #   run = 'run2'
    # }
    # 
    # file2load = paste0(dataDir,partID,'/',sesh,'/func/WM_',run,'_TAB.txt')
    
    file2load = list.files(paste0(dataDir,partID,'/',sesh,'/func/'), pattern='^WM_run')
    file2load = paste0(dataDir,partID,'/',sesh,'/func/',file2load)
    
    if (!file.exists(file2load)) {next}
    
    rawData = read.delim(file2load, header=TRUE, sep='\t', na.strings=c(''))
    
    taskData = rawData %>% select(Procedure.Block., Stimulus.Block., TargetType, CorrectResponse, StimType, BlockType, RunTrialNumber.Block., Stim.ACC, Stim.RESP, Stim.CRESP, ConsecSameResp)
    
    # full task, target HITS
    targetHit = taskData %>% filter(TargetType=='target') %>% .$Stim.ACC
    # full task, lure HITS
    lureHit = taskData %>% filter(TargetType=='lure') %>% .$Stim.ACC
    # full task, nonlure FALSE ALARMS
    nonlureFA = taskData %>% filter(TargetType=='nonlure') %>% .$Stim.ACC
    nonlureFA = abs(nonlureFA-1)
    
    dPrime_target = dPrime(targetHit, nonlureFA) # d prime - hits on targets versus false alarms on nonlures
    dPrime_lure = dPrime(lureHit, nonlureFA) # d prime - hits on lures (correctly identify a lure as a nontarget) versus false alarms on nonlures
    dPrime_tVl = dPrime(targetHit, abs(lureHit-1)) # d prime - hits on targets versus false alarms on lures (incorrectly identify a lure as a target)
    
    # 2-back, target HITS
    targetHit_2Back = taskData %>% filter(BlockType=='2-Back' & TargetType=='target') %>% .$Stim.ACC
    # 2-back, lure HITS
    lureHit_2Back = taskData %>% filter(BlockType=='2-Back' & TargetType=='lure') %>% .$Stim.ACC
    # 2-back, nonlure FALSE ALARMS
    nonlureFA_2Back = taskData %>% filter(BlockType=='2-Back' & TargetType=='nonlure') %>% .$Stim.ACC
    # invert FA (so that 0==correct negative and 1==false alarm)
    nonlureFA_2Back = abs(nonlureFA_2Back-1)
    
    dPrime_target2Back = dPrime(targetHit_2Back, nonlureFA_2Back) # d prime - hits on targets versus false alarms on nonlures
    dPrime_lure2Back = dPrime(lureHit_2Back, nonlureFA_2Back) # d prime - hits on lures (correctly identify a lure as a nontarget) versus false alarms on nonlures
    dPrime_tVl2Back = dPrime(targetHit_2Back, abs(lureHit_2Back-1)) # d prime - hits on targets versus false alarms on lures (incorrectly identify a lure as a target)

    
    # 0-back, target HITS
    targetHit_0Back = taskData %>% filter(BlockType=='0-Back' & TargetType=='target') %>% .$Stim.ACC
    # 0-back, lure HITS
    lureHit_0Back = taskData %>% filter(BlockType=='0-Back' & TargetType=='lure') %>% .$Stim.ACC
    # 0-back, nonlure FALSE ALARMS
    nonlureFA_0Back = taskData %>% filter(BlockType=='0-Back' & TargetType=='nonlure') %>% .$Stim.ACC
    # invert FA (so that 0==correct negative and 1==false alarm)
    nonlureFA_0Back = abs(nonlureFA_0Back-1)
    
    dPrime_target0Back = dPrime(targetHit_0Back, nonlureFA_0Back) # d prime - hits on targets versus false alarms on nonlures
    dPrime_lure0Back = dPrime(lureHit_0Back, nonlureFA_0Back) # d prime - hits on lures (correctly identify a lure as a nontarget) versus false alarms on nonlures
    dPrime_tVl0Back = dPrime(targetHit_0Back, abs(lureHit_0Back-1)) # d prime - hits on targets versus false alarms on lures (incorrectly identify a lure as a target)
    
    dPrime_temp = c(dPrime_target,dPrime_lure,dPrime_tVl,
                    dPrime_target2Back,dPrime_lure2Back,dPrime_tVl2Back,
                    dPrime_target0Back,dPrime_lure0Back,dPrime_tVl0Back)
    dPrime_strings = c('target', 'lure', 'tVl',
                       'target', 'lure', 'tVl',
                       'target', 'lure', 'tVl')
    nback_strings = c('both', 'both', 'both',
                      '2Back', '2Back', '2Back',
                      '0Back', '0Back', '0Back')
    
    #dataframe of d primes
    tempDF = data.frame(partID = partID,
                        session = sesh,
                        nback = nback_strings,
                        dPrime_cond = dPrime_strings,
                        dPrime_val = dPrime_temp)
    
    #calculate dPrimes for session 1, store info, calculate for session 2, combine info and calculate across session
    #determine maximum numbers of targets, lures, and nonlures - probably different numbers of lures/nonlures for participants, screws up dPrime adjustment
    #determine dPrime bounds
    
    if (sesh=='ses-01') {
      
      #store info to calculate d prime across sessions
      targetHit_temp = targetHit
      lureHit_temp = lureHit
      nonlureFA_temp = nonlureFA
      
      targetHit_2Back_temp = targetHit_2Back
      lureHit_2Back_temp = lureHit_2Back
      nonlureFA_2Back_temp = nonlureFA_2Back
      
      targetHit_0Back_temp = targetHit_0Back
      lureHit_0Back_temp = lureHit_0Back
      nonlureFA_0Back_temp = nonlureFA_0Back
      
      #add session 1 dPrime info to dataframe
      if (!exists('dPrimeDF')) {
        dPrimeDF = tempDF
      } else {
        dPrimeDF = rbind(dPrimeDF,tempDF)
      }
    } else {
      
      #add session 2 dPrime info to dataframe
      dPrimeDF = rbind(dPrimeDF,tempDF)
      
      #combine info to calculate d prime across sessions
      targetHitBoth = c(targetHit_temp,targetHit)
      lureHitBoth = c(lureHit_temp,lureHit)
      nonlureFABoth = c(nonlureFA_temp,nonlureFA)
      
      dPrime_targetBoth = dPrime(targetHitBoth,nonlureFABoth)
      dPrime_lureBoth = dPrime(lureHitBoth,nonlureFABoth)
      dPrime_tVlBoth = dPrime(targetHitBoth,abs(lureHitBoth-1))
      
      targetHitBoth_2Back = c(targetHit_2Back_temp,targetHit_2Back)
      lureHitBoth_2Back = c(lureHit_2Back_temp,lureHit_2Back)
      nonlureFABoth_2Back = c(nonlureFA_2Back_temp,nonlureFA_2Back)
      
      dPrime_target2BackBoth = dPrime(targetHitBoth_2Back,nonlureFABoth_2Back)
      dPrime_lure2BackBoth = dPrime(lureHitBoth_2Back,nonlureFABoth_2Back)
      dPrime_tVl2BackBoth = dPrime(targetHitBoth_2Back,abs(lureHitBoth_2Back-1))
      
      targetHitBoth_0Back = c(targetHit_0Back_temp,targetHit_0Back)
      lureHitBoth_0Back = c(lureHit_0Back_temp,lureHit_0Back)
      nonlureFABoth_0Back = c(nonlureFA_0Back_temp,nonlureFA_0Back)
      
      dPrime_target0BackBoth = dPrime(targetHitBoth_0Back,nonlureFABoth_0Back)
      dPrime_lure0BackBoth = dPrime(lureHitBoth_0Back,nonlureFABoth_0Back)
      dPrime_tVl0BackBoth = dPrime(targetHitBoth_0Back,abs(lureHitBoth_0Back-1))
      
      #make combined session d prime dataframe
      dPrimeBoth_temp = c(dPrime_targetBoth, dPrime_lureBoth, dPrime_tVlBoth,
                          dPrime_target2BackBoth, dPrime_lure2BackBoth, dPrime_tVl2BackBoth,
                          dPrime_target0BackBoth, dPrime_lure0BackBoth, dPrime_tVl0BackBoth)
      
      both_tempDF = data.frame(partID = partID,
                               session = 'both',
                               nback = nback_strings,
                               dPrime_cond = dPrime_strings,
                               dPrime_val = dPrimeBoth_temp)
      
      #add combined session dPrime info to dataframe
      dPrimeDF = rbind(dPrimeDF,both_tempDF)
    }
    
  }
}

#save the d prime dataframe
save(dPrimeDF, file = '/home/pjrice/Desktop/dissertation/dPrime.RData')
