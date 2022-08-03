

library(tidyr)
library(dplyr)
library(ggplot2)
library(ggpubr)
library(grid)
library(gridExtra)


correctResp = read.csv('Z:\\gp\\ACTR-WM\\data\\zeroBack_correctResponses.csv', header=FALSE)


partList = read.csv('C:/Users/Patrick/Desktop/labMeeting_5.4_plots/partList.csv',header=FALSE)

rootDir = 'C:/Users/Patrick/Desktop/labMeeting_5.4_plots/zb/zb/'


for (partID in partList$V1) {
  
  partDir = paste0(rootDir,partID)
  
  partResp = read.csv(paste0(partDir,'/zbResp.csv'),header=FALSE)
  
  partAccVec = as.integer(correctResp$V1 == partResp$V1)
  
  partAcc = mean(partAccVec, na.rm=TRUE)
  
  partRT = mean(partResp$V2, na.rm=TRUE)
  
  partID = tail(strsplit(partDir,'/')[[1]], n=1)
  
  temp_pMeas = data.frame('partID'=partID,'RT'=partRT,'Accuracy'=partAcc)
  
  if (!exists('partMeasures')) {
    partMeasures = temp_pMeas
  } else {
    partMeasures = rbind(partMeasures,temp_pMeas)
  }
  
}


partMeasures = partMeasures %>% pivot_longer(-partID, values_to='value',names_to='measure')

ggplot(partMeasures, aes(x=value)) +
  geom_histogram(binwidth=0.025,boundary=0) +
  facet_wrap(~measure, scales="free", ncol=1) +
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




partMeasures %>% group_by(measure) %>% summarise(meanVal = mean(value),
                                                 sdVal = sd(value))