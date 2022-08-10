
library(dplyr)



correctResp = read.csv('/home/pjrice/gp/ACTR-WM/data/twoBack_correctResponses.csv',header=FALSE,stringsAsFactors = FALSE)

partList = list.dirs('/home/pjrice/gp/ACTR-WM/data/beh/2b',full.names = FALSE)
partList = partList[-1]

rootDataDir = '/home/pjrice/gp/ACTR-WM/data/beh/2b/'
fName = '/2bResp.csv'

for (partID in partList) {
  
  file2load = paste0(rootDataDir,partID,fName)
  
  partData = read.csv(file2load,header=FALSE,stringsAsFactors = FALSE)
  
  partAccVec = as.integer(correctResp$V1 == partData$V1)
  
  partDF = data.frame(Acc = partAccVec,targetType=correctResp$V2)
  
  part_totAcc = sum(partDF$Acc)/nrow(partDF)
  
  part_tarAcc = partDF %>% filter(targetType=='target') %>% summarise(meanAcc = mean(Acc))
  part_lurAcc = partDF %>% filter(targetType=='lure') %>% summarise(meanAcc = mean(Acc))
  part_nlrAcc = partDF %>% filter(targetType=='nonlure') %>% summarise(meanAcc = mean(Acc))
  
  tempDF = data.frame(partID=partID,totAcc=part_totAcc,tarAcc = part_tarAcc$meanAcc,lurAcc=part_lurAcc$meanAcc,nlrAcc=part_nlrAcc$meanAcc)
  
  if (!exists('accDF')) {
    accDF = tempDF
  } else {
    accDF = rbind(accDF,tempDF)
  }
  
  
}

accDF %>% summarise_if(is.numeric, mean, na.rm=TRUE)
