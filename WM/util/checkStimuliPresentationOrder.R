#script to determine if the order of presentation of stimuli was the same across
#all participants
library(dplyr)

dataDir = '/projects/commonModel/data/WM/'
#change the following to 'ses-02' to check the second session
sessions = 'ses-01'

partIDs = list.dirs(dataDir, full.names=FALSE, recursive=FALSE)

#FOR TESTING
partID = partIDs[2]
sesh = 'ses-01'

stimuli = c()
for (partID in partIDs) {
  
  cat(partID,'\n')
  
  for (sesh in sessions) {
    
    if (sesh=='ses-01') {
      run = 'run1'
    } else {
      run = 'run2'
    }
    
    file2load = paste0(dataDir,partID,'/',sesh,'/func/WM_',run,'_TAB.txt')
    
    if (!file.exists(file2load)) {next}
    
    rawData = read.delim(file2load, header=TRUE, sep='\t', na.strings=c(''))
    stimuli = cbind(stimuli,rawData$Stimulus.Block.)
    
  }
}

stimuli = as.data.frame(stimuli)

#checking if the columns of the dataframe are the same by asking 
#for unique columns and checking if the number of those is 1
length(unique(as.list(stimuli))) == 1