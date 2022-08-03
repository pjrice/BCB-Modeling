library(dplyr)
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
  
  ses01RT = ses01 %>% select(Stim.RT)
  ses02RT = ses02 %>% select(Stim.RT)
  
  partRTs = rbind(ses01RT,ses02RT)
  
  if (!exists('allRTs')) {
    allRTs = partRTs
  } else {
    allRTs = rbind(allRTs, partRTs)
  }
  
}

ggplot(allRTs, aes(Stim.RT)) + geom_histogram()