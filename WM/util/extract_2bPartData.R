#script to extract HCP participant's WM task two-back condition data for ACT-R model fitting
library(dplyr)

rootDataDir = '/projects/commonModel/data/WM/'
saveDataDir = '/home/pjrice/gp/ACTR-WM/data/beh/2b/'

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
  
  ses01_2b = ses01 %>% filter(BlockType=='2-Back') %>% select(Stim.RESP, Stim.RT, TargetType)
  ses02_2b = ses02 %>% filter(BlockType=='2-Back') %>% select(Stim.RESP, Stim.RT, TargetType)
  
  twobResp = rbind(ses01_2b,ses02_2b)
  
  twobResp$Stim.RESP[twobResp$Stim.RESP==2] = 'f'
  twobResp$Stim.RESP[twobResp$Stim.RESP=='3'] = 'j'
  
  twobResp$Stim.RT = twobResp$Stim.RT/1000
  twobResp$Stim.RT[twobResp$Stim.RT==0] = NA
  
  if (nrow(twobResp)!=80) {
    print("Warning, number of trials is wrong!")
  }
  
  partDir = paste0(saveDataDir,part,'/')
  dir.create(partDir, showWarnings=FALSE)
  write.table(twobResp, paste0(partDir,'2bResp.csv'), na='', row.names=FALSE, col.names=FALSE, sep=',')
  
  rm(ses01folder,ses02folder,ses01file,ses02file,ses01,ses02,ses01_2b,ses02_2b,twobResp,partDir)
  
}