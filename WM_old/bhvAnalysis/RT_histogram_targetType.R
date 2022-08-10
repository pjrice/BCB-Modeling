#script to extract HCP participant's WM task zero-back condition data for ACT-R model fitting

library(tidyr)
library(ggplot2)

rootDataDir = '/projects/commonModel/data/WM/'
saveDataDir = '/home/pjrice/gp/ACTR-WM/data/beh/zb/'

partList = list.dirs(rootDataDir, full.names=FALSE, recursive=FALSE)

sessions = c('ses-01','ses-02')

for (part in partList) {
  
  ses01folder = paste0(rootDataDir,part,'/ses-01/func/')
  ses02folder = paste0(rootDataDir,part,'/ses-02/func/')
  
  ses01file = list.files(ses01folder, pattern='WM_run')
  ses02file = list.files(ses02folder, pattern='WM_run')
  
  if (length(ses01file)!=1 | length(ses02file)!=1) {
    print("Warning, more than one behavioral file found!")
  }
  
  ses01 = read.delim(paste0(ses01folder,ses01file))
  ses02 = read.delim(paste0(ses02folder,ses02file))
  
  ses01RTs = ses01 %>% select(BlockType,TargetType,Stim.RT) %>% drop_na()
  ses02RTs = ses02 %>% select(BlockType,TargetType,Stim.RT) %>% drop_na()
  
  byTrialDF = rbind(ses01RTs,ses02RTs)
  
  byTrialDF$Stim.RT = byTrialDF$Stim.RT/1000
  
  if (!exists("allParts_allTrials")) {
    allParts_allTrials = byTrialDF
  } else {
    allParts_allTrials = rbind(allParts_allTrials,byTrialDF)
  }
  
  tarType_meanRT = byTrialDF %>% group_by(BlockType,TargetType) %>% summarise(meanRT=mean(Stim.RT))
  tarType_meanRT$partID = part
  
  if (!exists("allParts_meanRTs")) {
    allParts_meanRTs = tarType_meanRT
  } else
    allParts_meanRTs = rbind(allParts_meanRTs,tarType_meanRT)
  
  
}

#################################################################################################################
# All trials RTs
allParts_allTrials$conds = interaction(allParts_allTrials$BlockType, allParts_allTrials$TargetType)

test1 = allParts_allTrials %>% filter(conds=='2-Back.target' | conds=='0-Back.target')
ggplot(test1, aes(x=Stim.RT, fill=conds)) + 
  geom_histogram(alpha = 0.2, position='identity') +
  xlim(0,2) +
  ggtitle('All RTs: Targets, 0-Back versus 2-Back')

test2 = allParts_allTrials %>% filter(conds=='2-Back.lure' | conds=='0-Back.lure')
ggplot(test2, aes(x=Stim.RT, fill=conds)) + 
  geom_histogram(alpha = 0.2, position='identity') +
  xlim(0,2) +
  ggtitle('All RTs: Lures, 0-Back versus 2-Back')

test3 = allParts_allTrials %>% filter(conds=='2-Back.nonlure' | conds=='0-Back.nonlure')
ggplot(test3, aes(x=Stim.RT, fill=conds)) + 
  geom_histogram(alpha = 0.2, position='identity') +
  xlim(0,2) +
  ggtitle('All RTs: Nonlures, 0-Back versus 2-Back')

test4 = allParts_allTrials %>% filter(conds=='0-Back.target' | conds=='0-Back.lure' | conds=='0-Back.nonlure')
ggplot(test4, aes(x=Stim.RT, fill=conds)) + 
  geom_histogram(alpha = 0.2, position='identity') +
  xlim(0,2) +
  ggtitle('All RTs: 0-Back Targets, Lures, and Nonlures')

test5 = allParts_allTrials %>% filter(conds=='2-Back.target' | conds=='2-Back.lure' | conds=='2-Back.nonlure')
ggplot(test5, aes(x=Stim.RT, fill=conds)) + 
  geom_histogram(alpha = 0.2, position='identity') +
  xlim(0,2) +
  ggtitle('All RTs: 2-Back Targets, Lures, and Nonlures')



#################################################################################################################
# mean RTs over trials for Block Types/Target Types
allParts_meanRTs$conds = interaction(allParts_meanRTs$BlockType, allParts_meanRTs$TargetType)

test6 = allParts_meanRTs %>% filter(conds=='2-Back.target' | conds=='0-Back.target')
ggplot(test6, aes(x=meanRT, fill=conds)) + 
  geom_histogram(alpha = 0.2, position='identity') +
  xlim(0,2) +
  ggtitle('Mean RTs: Targets, 0-Back versus 2-Back')

test7 = allParts_meanRTs %>% filter(conds=='2-Back.lure' | conds=='0-Back.lure')
ggplot(test7, aes(x=meanRT, fill=conds)) + 
  geom_histogram(alpha = 0.2, position='identity') +
  xlim(0,2) +
  ggtitle('Mean RTs: Lures, 0-Back versus 2-Back')

test8 = allParts_meanRTs %>% filter(conds=='2-Back.nonlure' | conds=='0-Back.nonlure')
ggplot(test8, aes(x=meanRT, fill=conds)) + 
  geom_histogram(alpha = 0.2, position='identity') +
  xlim(0,2) +
  ggtitle('Mean RTs: Nonlures, 0-Back versus 2-Back')

test9 = allParts_meanRTs %>% filter(conds=='0-Back.target' | conds=='0-Back.lure' | conds=='0-Back.nonlure')
ggplot(test9, aes(x=meanRT, fill=conds)) + 
  geom_histogram(alpha = 0.2, position='identity') +
  xlim(0,2) +
  ggtitle('Mean RTs: 0-Back Targets, Lures, and Nonlures')

test10 = allParts_meanRTs %>% filter(conds=='2-Back.target' | conds=='2-Back.lure' | conds=='2-Back.nonlure')
ggplot(test10, aes(x=meanRT, fill=conds)) + 
  geom_histogram(alpha = 0.2, position='identity') +
  xlim(0,2) +
  ggtitle('Mean RTs: 2-Back Targets, Lures, and Nonlures')

#################################################################################################################
#paired t-tests

  