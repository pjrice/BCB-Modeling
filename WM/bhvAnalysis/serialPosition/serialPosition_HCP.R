library(dplyr)
library(ggplot2)

dataDir = '/projects/commonModel/data/WM/'
sessions = c('ses-01', 'ses-02')

partIDs = list.dirs(dataDir, full.names=FALSE, recursive=FALSE)

#FOR TESTING
partID = partIDs[2]
sesh = 'ses-01'

missingFilePartIDs = c()
for (partID in partIDs) {
  
  cat(partID,'\n')
  
  for (sesh in sessions) {
    
    # if (sesh=='ses-01') {
    #   run = 'run1'
    # } else {
    #   run = 'run2'
    # }
    # 
    # 
    # file2load = paste0(dataDir,partID,'/',sesh,'/func/WM_',run,'_TAB.txt')
    
    file2load = list.files(paste0(dataDir,partID,'/',sesh,'/func/'), pattern='^WM_run')
    file2load = paste0(dataDir,partID,'/',sesh,'/func/',file2load)
    
    #so it seems there are some files we want to load that are named slightly differently
    #instead of 'run1' or 'run2' it may be 'run3' or 'run4' (from what I've seen), either in session1 or session2
    if (!file.exists(file2load)) {
      
      
      temp = paste(partID, sesh)
      missingFilePartIDs = c(missingFilePartIDs,temp)
      next
      }
    
    rawData = read.delim(file2load, header=TRUE, sep='\t', na.strings=c(''))
    
    taskData = rawData %>% select(Procedure.Block., Stimulus.Block., TargetType, CorrectResponse, StimType, BlockType, RunTrialNumber.Block., Stim.ACC, Stim.RESP, Stim.CRESP, ConsecSameResp)
    
    
    ##########################################################################################################################################################################################
    #here we are calculating serial position in three ways, and then extracting the number correct and number total of each serial position
    #only doing this for 2-back
    
    ########################################
    #serial position - only target to only target
    #possible serial positions: 1-9
    # tempVec = rep(NA,nrow(taskData))
    # oldTarPosition = NA
    # for (i in 1:nrow(taskData)) {
    #   
    #   if (!is.na(taskData$TargetType[i]) & taskData$TargetType[i]=='target') {
    #     
    #     if (is.na(oldTarPosition)) {
    #       #the first target we see in a block
    #       oldTarPosition = i
    #     } else {
    #       #compute serial position of the current target
    #       currTarSerialPos = taskData$RunTrialNumber.Block.[i] - taskData$RunTrialNumber.Block.[oldTarPosition]
    #       tempVec[i] = currTarSerialPos
    #       oldTarPosition = i
    #     }
    #     
    #   }
    #   
    #   #need to reset oldTarPosition if we hit a new block
    #   if (taskData$Procedure.Block.[i] == 'Cue2BackPROC' | taskData$Procedure.Block.[i] == 'Cue0BackPROC') {
    #     oldTarPosition = NA
    #   }
    #   
    # }
    # taskData$t2tSP = tempVec
    # 
    # tempList = list()
    # tempList = cbind(tempList,partID)
    # for (i in 1:9) {
    #   
    #   tempDF = taskData %>% filter(BlockType=='2-Back' & t2tSP==i)
    #   
    #   #can handle instances where SP didn't occur with nrow()==0
    #   if (nrow(tempDF)!=0) {
    #     tempSP.ACC = sum(tempDF$Stim.ACC)/length(tempDF$Stim.ACC)
    #   } else {
    #     tempSP.ACC = NA
    #   }
    #   
    #   tempList = cbind(tempList,tempSP.ACC)
    #   
    # }
    # 
    # if (!exists('t2tSP_tempList')) {
    #   t2tSP_tempList = tempList
    # } else {
    #   t2tSP_tempList = rbind(t2tSP_tempList,tempList)
    # }
    
    ########################################
    
    ########################################
    
    #serial position - target/lure to target/lure
    #possible serial positions: 1-6
    tempVec = rep(NA,nrow(taskData))
    oldTarPosition = NA
    for (i in 1:nrow(taskData)) {
      
      if (!is.na(taskData$TargetType[i]) & (taskData$TargetType[i]=='target' | taskData$TargetType[i]=='lure')) {
        
        if (is.na(oldTarPosition)) {
          #the first target we see in a block
          oldTarPosition = i
        } else {
          #compute serial position of the current target
          currTarSerialPos = taskData$RunTrialNumber.Block.[i] - taskData$RunTrialNumber.Block.[oldTarPosition]
          tempVec[i] = currTarSerialPos
          oldTarPosition = i
        }
        
      }
      
      #need to reset oldTarPosition if we hit a new block
      if (taskData$Procedure.Block.[i] == 'Cue2BackPROC' | taskData$Procedure.Block.[i] == 'Cue0BackPROC') {
        oldTarPosition = NA
      }
      
    }
    taskData$tl2tlSP = tempVec
    
    tempList = list()
    tempList = cbind(tempList,partID)
    tempList = cbind(tempList,sesh)
    for (i in 1:4) {
      
      tempDF = taskData %>% filter(BlockType=='2-Back' & tl2tlSP==i)
      
      #can handle instances where SP didn't occur with nrow()==0
      if (nrow(tempDF)!=0) {
        #tempSP.ACC = sum(tempDF$Stim.ACC)/length(tempDF$Stim.ACC)
        tempSP.CORRECT = sum(tempDF$Stim.ACC)
        tempSP.NUMTOTAL = length(tempDF$Stim.ACC)
      } else {
        #tempSP.ACC = NA
        tempSP.CORRECT = NA
        tempSP.NUMTOTAL = NA
      }
      
      tempList = cbind(tempList,tempSP.CORRECT,tempSP.NUMTOTAL)
      
    }
    
    if (!exists('tl2tlSP_tempList')) {
      tl2tlSP_tempList = tempList
    } else {
      tl2tlSP_tempList = rbind(tl2tlSP_tempList,tempList)
    }
    

    
    
    
    ##########################################################################################################################################################################################
    #here we are calculating the number correct and the number total of target or lure presentations in 2-back or 0-back conditios
    targets2back = taskData %>% filter(TargetType=='target' & BlockType=='2-Back')
    t2bNumCorrect = sum(targets2back$Stim.ACC)
    t2bTotal = length(targets2back$Stim.ACC)
    
    lures2back = taskData %>% filter(TargetType=='lure' & BlockType=='2-Back')
    l2bNumCorrect = sum(lures2back$Stim.ACC)
    l2bTotal = length(lures2back$Stim.ACC)
    
    targets0back = taskData %>% filter(TargetType=='target' & BlockType=='0-Back')
    t0bNumCorrect = sum(targets0back$Stim.ACC)
    t0bTotal = length(targets0back$Stim.ACC)
    
    lures0back = taskData %>% filter(TargetType=='lure' & BlockType=='0-Back')
    l0bNumCorrect = sum(lures0back$Stim.ACC)
    l0bTotal = length(lures0back$Stim.ACC)
    
    tempDF = data.frame(partID, sesh, 
                        t2bNumCorrect, t2bTotal, 
                        l2bNumCorrect, l2bTotal, 
                        t0bNumCorrect, t0bTotal, 
                        l0bNumCorrect, l0bTotal)

    
    if (!exists('targetLure.ACC')) {
      targetLure.ACC = tempDF
    } else {
      targetLure.ACC = rbind(targetLure.ACC,tempDF)
    }
    

    
  } #end of session loop
  
} #end of part loop

targetLure.ACC.bySesh = targetLure.ACC %>% mutate(t2bPcnt=t2bNumCorrect/t2bTotal,
                                           l2bPcnt=l2bNumCorrect/l2bTotal,
                                           t0bPcnt=t0bNumCorrect/t0bTotal,
                                           l0bPcnt=l0bNumCorrect/l0bTotal)

targetLure.ACC.bothSesh = targetLure.ACC %>% group_by(partID) %>% summarise(t2bNumCorrect=sum(t2bNumCorrect),
                                                                            t2bTotal=sum(t2bTotal),
                                                                            l2bNumCorrect=sum(l2bNumCorrect),
                                                                            l2bTotal=sum(l2bTotal),
                                                                            t0bNumCorrect=sum(t0bNumCorrect),
                                                                            t0bTotal=sum(t0bTotal),
                                                                            l0bNumCorrect=sum(l0bNumCorrect),
                                                                            l0bTotal=sum(l0bTotal)) %>% mutate(t2bPcnt=t2bNumCorrect/t2bTotal,
                                                                                                               l2bPcnt=l2bNumCorrect/l2bTotal,
                                                                                                               t0bPcnt=t0bNumCorrect/t0bTotal,
                                                                                                               l0bPcnt=l0bNumCorrect/l0bTotal)


ggplot(targetLure.ACC.bothSesh, aes(x=t2bPcnt, y=l2bPcnt)) + geom_point() + geom_smooth(method='lm')
tl2bCorr = cor(targetLure.ACC.bothSesh$t2bPcnt,targetLure.ACC.bothSesh$l2bPcnt)

ggplot(targetLure.ACC.bothSesh, aes(x=t0bPcnt, y=l0bPcnt)) + geom_point() + geom_smooth(method='lm')
tl0bCorr = cor(targetLure.ACC.bothSesh$t0bPcnt,targetLure.ACC.bothSesh$l0bPcnt)


tlSesh1 = targetLure.ACC.bySesh %>% filter(sesh=='ses-01')
tlSesh2 = targetLure.ACC.bySesh %>% filter(sesh=='ses-02')

ggplot(tlSesh1, aes(x=t2bPcnt, y=l2bPcnt)) + geom_point() + geom_smooth(method='lm')
tl2b_sesh1Corr = cor(tlSesh1$t2bPcnt, tlSesh1$l2bPcnt)

ggplot(tlSesh2, aes(x=t2bPcnt, y=l2bPcnt)) + geom_point() + geom_smooth(method='lm')
tl2b_sesh2Corr = cor(tlSesh2$t2bPcnt, tlSesh2$l2bPcnt)

##########################################################################################################################################################
#relationships between sessions

#2-back target accuracy
t2bPcnt = targetLure.ACC.bySesh %>% select(partID,sesh,t2bPcnt) %>% spread(sesh, t2bPcnt)
colnames(t2bPcnt) = c('partID', 'ses1','ses2')

ggplot(t2bPcnt, aes(x=ses1, y=ses2)) + 
  geom_point() +
  xlab('Session 1 target accuracy') +
  ylab('Session 2 target accuracy') +
  ggtitle('2-back target accuracy between sessions')


#2-back lure accuracy
l2bPcnt = targetLure.ACC.bySesh %>% select(partID,sesh,l2bPcnt) %>% spread(sesh, l2bPcnt)
colnames(l2bPcnt) = c('partID', 'ses1','ses2')

ggplot(l2bPcnt, aes(x=ses1, y=ses2)) + 
  geom_point() +
  xlab('Session 1 lure accuracy') +
  ylab('Session 2 lure accuracy') +
  ggtitle('2-back lure accuracy between sessions')


#0-back target accuracy
t0bPcnt = targetLure.ACC.bySesh %>% select(partID,sesh,t0bPcnt) %>% spread(sesh, t0bPcnt)
colnames(t0bPcnt) = c('partID', 'ses1','ses2')

ggplot(t0bPcnt, aes(x=ses1, y=ses2)) + 
  geom_point() +
  xlab('Session 1 target accuracy') +
  ylab('Session 2 target accuracy') +
  ggtitle('0-back target accuracy between sessions')


#0-back lure accuracy
l0bPcnt = targetLure.ACC.bySesh %>% select(partID,sesh,l0bPcnt) %>% spread(sesh, l0bPcnt)
colnames(l0bPcnt) = c('partID', 'ses1','ses2')

ggplot(l0bPcnt, aes(x=ses1, y=ses2)) + 
  geom_point() +
  xlab('Session 1 lure accuracy') +
  ylab('Session 2 lure accuracy') +
  ggtitle('0-back lure accuracy between sessions')






















