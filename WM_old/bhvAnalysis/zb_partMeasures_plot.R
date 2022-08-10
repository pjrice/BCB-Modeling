
library(tidyr)
library(dplyr)
library(lemon)
library(ggplot2)
library(ggpubr)
library(grid)
library(gridExtra)


correctResp = read.csv('Z:\\gp\\ACTR-WM\\data\\zeroBack_correctResponses.csv', header=FALSE)
colnames(correctResp) = c('cResp','targetType')

partList = read.csv('C:/Users/Patrick/Desktop/labMeeting_5.4_plots/partList.csv',header=FALSE)

rootDir = 'C:/Users/Patrick/Desktop/labMeeting_5.4_plots/zb/zb/'


for (partID in partList$V1) {
  
  partDir = paste0(rootDir,partID)
  
  partResp = read.csv(paste0(partDir,'/zbResp.csv'),header=FALSE)
  
  colnames(partResp) = c('resp','RT','targetType')
  
  #get mean accuracy
  partAccVec = as.integer(correctResp$cResp == partResp$resp)
  partAcc = mean(partAccVec, na.rm=TRUE)
  
  #get mean RT
  partRT = mean(partResp$RT, na.rm=TRUE)
  
  #get target, lure, and nonlure accuracy
  tarTrials = partResp %>% filter(targetType=='target')
  tarCresp = correctResp %>% filter(targetType=='target')
  tarAcc = mean(as.integer(tarCresp$cResp == tarTrials$resp), na.rm=TRUE)
  tarRT = mean(tarTrials$RT, na.rm=TRUE)
  
  lurTrials = partResp %>% filter(targetType=='lure')
  lurCresp = correctResp %>% filter(targetType=='lure')
  lurAcc = mean(as.integer(lurCresp$cResp == lurTrials$resp), na.rm=TRUE)
  lurRT = mean(lurTrials$RT, na.rm=TRUE)
  
  nlrTrials = partResp %>% filter(targetType=='nonlure')
  nlrCresp = correctResp %>% filter(targetType=='nonlure')
  nlrAcc = mean(as.integer(nlrCresp$cResp == nlrTrials$resp), na.rm=TRUE)
  nlrRT = mean(nlrTrials$RT, na.rm=TRUE)
  
  partID = tail(strsplit(partDir,'/')[[1]], n=1)
  
  temp_pMeas = data.frame('partID'=partID,
                          'mRT'=partRT,
                          'mAccuracy'=partAcc,
                          'tarRT'=tarRT,
                          'tarAcc'=tarAcc,
                          'lurRT'=lurRT,
                          'lurAcc'=lurAcc,
                          'nlrRT'=nlrRT,
                          'nlrAcc'=nlrAcc)
  
  if (!exists('partMeasures')) {
    partMeasures = temp_pMeas
  } else {
    partMeasures = rbind(partMeasures,temp_pMeas)
  }
  
}

partMeasures = partMeasures %>% pivot_longer(-partID, values_to='value',names_to='measure')
partMeasures$measure = factor(partMeasures$measure, levels=c('mAccuracy','mRT','tarAcc','tarRT','lurAcc','lurRT','nlrAcc','nlrRT'))


#could play around with scales='fixed' to see if we can get different x-axis scales for accuracy and RT
ggplot(partMeasures, aes(x=value)) +
  geom_histogram(binwidth=0.025,boundary=0) +
  #facet_wrap(~measure, scales="fixed", ncol=2) +
  facet_rep_wrap(~measure, scales="free", ncol=2, repeat.tick.labels=TRUE) +
  scale_y_continuous(expand=expansion(mult = c(0, .1))) +
  ggtitle('Participant measures') +
  theme(line = element_line(size=1),
        text = element_text(size=15),
        plot.title = element_text(size=17),
        strip.background = element_blank(),
        #strip.text.x = element_blank(),
        panel.background = element_blank(),
        panel.grid = element_blank(),
        axis.line = element_line(color='black'),
        aspect.ratio=1/2.75)
