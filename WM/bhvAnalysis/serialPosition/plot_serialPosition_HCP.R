

library(tidyverse)

#the following code to make the session 2 only plot will no longer work because the accuracy columns
#in tl2tlSP_tempList have been split into num correct and num total columns
#can just filter out session 1 and do the accuracy calculation to make it if need be
tl2tlSPdata = as.data.frame(tl2tlSP_tempList)
colnames(tl2tlSPdata) = c('partID', 'session', 'SP1', 'SP2', 'SP3', 'SP4')


test = tl2tlSPdata %>% filter(session=='ses-02')

tl2tl_gplot = test %>% subset(select=-session) %>% gather('SerialPos', 'Accuracy', -partID)
tl2tl_gplot$partID = as.factor(as.character(tl2tl_gplot$partID))
tl2tl_gplot$SerialPos = as.factor(tl2tl_gplot$SerialPos)
tl2tl_gplot$Accuracy = as.numeric(tl2tl_gplot$Accuracy)

ggplot(tl2tl_gplot, aes(x=SerialPos, y=Accuracy, group=partID, color=partID)) + 
  geom_line() + 
  ggtitle('Accuracy by serial position per participant, session 2 only') +
  theme(legend.position = 'none')



#want to combine first+second session, so we'll probably be storing NumCorrect/NumTotal, summing across the two sessions and calculating accuracy



#average session 2 serial position plot
tester = tl2tlSPdata %>% filter(session=='ses-02')

tester$SP1 = as.numeric(tester$SP1)
tester$SP2 = as.numeric(tester$SP2)
tester$SP3 = as.numeric(tester$SP3)
tester$SP4 = as.numeric(tester$SP4)

SP1mean = mean(tester$SP1)
SP2mean = mean(tester$SP2)
SP3mean = mean(tester$SP3)
SP4mean = mean(tester$SP4)

SP1se = sd(tester$SP1)/sqrt(length(tester$SP1))
SP2se = sd(tester$SP2)/sqrt(length(tester$SP2))
SP3se = sd(tester$SP3)/sqrt(length(tester$SP3))
SP4se = sd(tester$SP4)/sqrt(length(tester$SP4))

meanSP_DF = data.frame(SerialPos=c('SP1', 'SP2', 'SP3', 'SP4'), Mean=c(SP1mean,SP2mean,SP3mean,SP4mean), SE=c(SP1se,SP2se,SP3se,SP4se))

fullAxis = ggplot(meanSP_DF, aes(x=SerialPos, y=Mean)) + 
  geom_point() +
  geom_errorbar(aes(ymin=Mean-SE, ymax=Mean+SE), width=0.1) +
  ylim(0,1) +
  xlab('Serial Position') +
  ylab('Target/Lure Accuracy') +
  ggtitle('Mean target or lure accuracy by serial position, session 2 only') +
  theme(axis.text = element_text(size=12),
        axis.title = element_text(size=15),
        title = element_text(size=15))

limAxis = ggplot(meanSP_DF, aes(x=SerialPos, y=Mean)) + 
  geom_point() +
  geom_errorbar(aes(ymin=Mean-SE, ymax=Mean+SE), width=0.1) +
  xlab('Serial Position') +
  ylab('Target/Lure Accuracy') +
  ggtitle('Mean target or lure accuracy by serial position, session 2 only, Y axis zoomed in') +
  theme(axis.text = element_text(size=12),
        axis.title = element_text(size=15),
        title = element_text(size=15))


library(gridExtra)
grid.arrange(fullAxis,limAxis, ncol=2)





##############################################################################################################################
tl2tlSPdata = as.data.frame(tl2tlSP_tempList)
colnames(tl2tlSPdata) = c('partID', 'session', 'SP1.NUMCORRECT', 'SP1.NUMTOTAL', 'SP2.NUMCORRECT', 'SP2.NUMTOTAL', 'SP3.NUMCORRECT', 'SP3.NUMTOTAL', 'SP4.NUMCORRECT', 'SP4.NUMTOTAL')
tl2tlSPdata$SP1.NUMCORRECT = as.numeric(tl2tlSPdata$SP1.NUMCORRECT)
tl2tlSPdata$SP1.NUMTOTAL = as.numeric(tl2tlSPdata$SP1.NUMTOTAL)
tl2tlSPdata$SP2.NUMCORRECT = as.numeric(tl2tlSPdata$SP2.NUMCORRECT)
tl2tlSPdata$SP2.NUMTOTAL = as.numeric(tl2tlSPdata$SP2.NUMTOTAL)
tl2tlSPdata$SP3.NUMCORRECT = as.numeric(tl2tlSPdata$SP3.NUMCORRECT)
tl2tlSPdata$SP3.NUMTOTAL = as.numeric(tl2tlSPdata$SP3.NUMTOTAL)
tl2tlSPdata$SP4.NUMCORRECT = as.numeric(tl2tlSPdata$SP4.NUMCORRECT)
tl2tlSPdata$SP4.NUMTOTAL = as.numeric(tl2tlSPdata$SP4.NUMTOTAL)

##############################################################################################################################
#both sessions

tl2tlSP.ACC = tl2tlSPdata %>% group_by(partID) %>% summarise(SP1.NUMCORRECT = sum(SP1.NUMCORRECT),
                                                      SP1.NUMTOTAL = sum(SP1.NUMTOTAL),
                                                      SP2.NUMCORRECT = sum(SP2.NUMCORRECT),
                                                      SP2.NUMTOTAL = sum(SP2.NUMTOTAL),
                                                      SP3.NUMCORRECT = sum(SP3.NUMCORRECT),
                                                      SP3.NUMTOTAL = sum(SP3.NUMTOTAL),
                                                      SP4.NUMCORRECT = sum(SP4.NUMCORRECT, na.rm=TRUE),
                                                      SP4.NUMTOTAL = sum(SP4.NUMTOTAL, na.rm=TRUE)) %>% mutate(SP1pcnt = SP1.NUMCORRECT/SP1.NUMTOTAL,
                                                                                                               SP2pcnt = SP2.NUMCORRECT/SP2.NUMTOTAL,
                                                                                                               SP3pcnt = SP3.NUMCORRECT/SP3.NUMTOTAL,
                                                                                                               SP4pcnt = SP4.NUMCORRECT/SP4.NUMTOTAL)

tl2tlSP.ACC$SP4pcnt[which(is.nan(tl2tlSP.ACC$SP4pcnt))] = NA


SP1mean = mean(tl2tlSP.ACC$SP1pcnt)
SP2mean = mean(tl2tlSP.ACC$SP2pcnt)
SP3mean = mean(tl2tlSP.ACC$SP3pcnt)
SP4mean = mean(tl2tlSP.ACC$SP4pcnt, na.rm=TRUE)

SP1sem = sd(tl2tlSP.ACC$SP1pcnt)/sqrt(length(tl2tlSP.ACC$SP1pcnt))
SP2sem = sd(tl2tlSP.ACC$SP2pcnt)/sqrt(length(tl2tlSP.ACC$SP2pcnt))
SP3sem = sd(tl2tlSP.ACC$SP3pcnt)/sqrt(length(tl2tlSP.ACC$SP3pcnt))
SP4sem = sd(tl2tlSP.ACC$SP4pcnt,na.rm=TRUE)/sqrt(length(tl2tlSP.ACC$SP4pcnt))

plotDF = data.frame(SerialPos=c('SP1', 'SP2', 'SP3', 'SP4'), Mean=c(SP1mean,SP2mean,SP3mean,SP4mean), SE=c(SP1sem,SP2sem,SP3sem,SP4sem))


fullAxis = ggplot(plotDF, aes(x=SerialPos, y=Mean)) + 
  geom_point() +
  geom_errorbar(aes(ymin=Mean-SE, ymax=Mean+SE), width=0.1) +
  ylim(0,1) +
  xlab('Serial Position') +
  ylab('Target/Lure Accuracy') +
  ggtitle('Mean target or lure accuracy by serial position, both sessions') +
  theme(axis.text = element_text(size=12),
        axis.title = element_text(size=15),
        title = element_text(size=15))

limAxis = ggplot(plotDF, aes(x=SerialPos, y=Mean)) + 
  geom_point() +
  geom_errorbar(aes(ymin=Mean-SE, ymax=Mean+SE), width=0.1) +
  xlab('Serial Position') +
  ylab('Target/Lure Accuracy') +
  ggtitle('Mean target or lure accuracy by serial position, both sessions, Y axis zoomed in') +
  theme(axis.text = element_text(size=12),
        axis.title = element_text(size=15),
        title = element_text(size=15))

##############################################################################################################################
#session1

tl2tlSP.ACC = tl2tlSPdata %>% filter(session=='ses-01') %>% group_by(partID) %>% summarise(SP1.NUMCORRECT = sum(SP1.NUMCORRECT),
                                                             SP1.NUMTOTAL = sum(SP1.NUMTOTAL),
                                                             SP2.NUMCORRECT = sum(SP2.NUMCORRECT),
                                                             SP2.NUMTOTAL = sum(SP2.NUMTOTAL),
                                                             SP3.NUMCORRECT = sum(SP3.NUMCORRECT),
                                                             SP3.NUMTOTAL = sum(SP3.NUMTOTAL),
                                                             SP4.NUMCORRECT = sum(SP4.NUMCORRECT, na.rm=TRUE),
                                                             SP4.NUMTOTAL = sum(SP4.NUMTOTAL, na.rm=TRUE)) %>% mutate(SP1pcnt = SP1.NUMCORRECT/SP1.NUMTOTAL,
                                                                                                                      SP2pcnt = SP2.NUMCORRECT/SP2.NUMTOTAL,
                                                                                                                      SP3pcnt = SP3.NUMCORRECT/SP3.NUMTOTAL,
                                                                                                                      SP4pcnt = SP4.NUMCORRECT/SP4.NUMTOTAL)

tl2tlSP.ACC$SP4pcnt[which(is.nan(tl2tlSP.ACC$SP4pcnt))] = NA


SP1meanS1 = mean(tl2tlSP.ACC$SP1pcnt)
SP2meanS1 = mean(tl2tlSP.ACC$SP2pcnt)
SP3meanS1 = mean(tl2tlSP.ACC$SP3pcnt)
SP4meanS1 = mean(tl2tlSP.ACC$SP4pcnt, na.rm=TRUE)

SP1semS1 = sd(tl2tlSP.ACC$SP1pcnt)/sqrt(length(tl2tlSP.ACC$SP1pcnt))
SP2semS1 = sd(tl2tlSP.ACC$SP2pcnt)/sqrt(length(tl2tlSP.ACC$SP2pcnt))
SP3semS1 = sd(tl2tlSP.ACC$SP3pcnt)/sqrt(length(tl2tlSP.ACC$SP3pcnt))
SP4semS1 = sd(tl2tlSP.ACC$SP4pcnt,na.rm=TRUE)/sqrt(length(tl2tlSP.ACC$SP4pcnt))

plotDF = data.frame(SerialPos=c('SP1', 'SP2', 'SP3', 'SP4'), Mean=c(SP1meanS1,SP2meanS1,SP3meanS1,SP4meanS1), SE=c(SP1semS1,SP2semS1,SP3semS1,SP4semS1))


fullAxisS1 = ggplot(plotDF, aes(x=SerialPos, y=Mean)) + 
  geom_point() +
  geom_errorbar(aes(ymin=Mean-SE, ymax=Mean+SE), width=0.1) +
  ylim(0,1) +
  xlab('Serial Position') +
  ylab('Target/Lure Accuracy') +
  ggtitle('Mean target or lure accuracy by serial position, session 1 only') +
  theme(axis.text = element_text(size=12),
        axis.title = element_text(size=15),
        title = element_text(size=15))

limAxisS1 = ggplot(plotDF, aes(x=SerialPos, y=Mean)) + 
  geom_point() +
  geom_errorbar(aes(ymin=Mean-SE, ymax=Mean+SE), width=0.1) +
  xlab('Serial Position') +
  ylab('Target/Lure Accuracy') +
  ggtitle('Mean target or lure accuracy by serial position, session 1 only, Y axis zoomed in') +
  theme(axis.text = element_text(size=12),
        axis.title = element_text(size=15),
        title = element_text(size=15))

##############################################################################################################################
#session2

tl2tlSP.ACC = tl2tlSPdata %>% filter(session=='ses-02') %>% group_by(partID) %>% summarise(SP1.NUMCORRECT = sum(SP1.NUMCORRECT),
                                                                                           SP1.NUMTOTAL = sum(SP1.NUMTOTAL),
                                                                                           SP2.NUMCORRECT = sum(SP2.NUMCORRECT),
                                                                                           SP2.NUMTOTAL = sum(SP2.NUMTOTAL),
                                                                                           SP3.NUMCORRECT = sum(SP3.NUMCORRECT),
                                                                                           SP3.NUMTOTAL = sum(SP3.NUMTOTAL),
                                                                                           SP4.NUMCORRECT = sum(SP4.NUMCORRECT, na.rm=TRUE),
                                                                                           SP4.NUMTOTAL = sum(SP4.NUMTOTAL, na.rm=TRUE)) %>% mutate(SP1pcnt = SP1.NUMCORRECT/SP1.NUMTOTAL,
                                                                                                                                                    SP2pcnt = SP2.NUMCORRECT/SP2.NUMTOTAL,
                                                                                                                                                    SP3pcnt = SP3.NUMCORRECT/SP3.NUMTOTAL,
                                                                                                                                                    SP4pcnt = SP4.NUMCORRECT/SP4.NUMTOTAL)

tl2tlSP.ACC$SP4pcnt[which(is.nan(tl2tlSP.ACC$SP4pcnt))] = NA


SP1meanS2 = mean(tl2tlSP.ACC$SP1pcnt)
SP2meanS2 = mean(tl2tlSP.ACC$SP2pcnt)
SP3meanS2 = mean(tl2tlSP.ACC$SP3pcnt)
SP4meanS2 = mean(tl2tlSP.ACC$SP4pcnt, na.rm=TRUE)

SP1semS2 = sd(tl2tlSP.ACC$SP1pcnt)/sqrt(length(tl2tlSP.ACC$SP1pcnt))
SP2semS2 = sd(tl2tlSP.ACC$SP2pcnt)/sqrt(length(tl2tlSP.ACC$SP2pcnt))
SP3semS2 = sd(tl2tlSP.ACC$SP3pcnt)/sqrt(length(tl2tlSP.ACC$SP3pcnt))
SP4semS2 = sd(tl2tlSP.ACC$SP4pcnt,na.rm=TRUE)/sqrt(length(tl2tlSP.ACC$SP4pcnt))

plotDF = data.frame(SerialPos=c('SP1', 'SP2', 'SP3', 'SP4'), Mean=c(SP1meanS2,SP2meanS2,SP3meanS2,SP4meanS2), SE=c(SP1semS2,SP2semS2,SP3semS2,SP4semS2))


fullAxisS2 = ggplot(plotDF, aes(x=SerialPos, y=Mean)) + 
  geom_point() +
  geom_errorbar(aes(ymin=Mean-SE, ymax=Mean+SE), width=0.1) +
  ylim(0,1) +
  xlab('Serial Position') +
  ylab('Target/Lure Accuracy') +
  ggtitle('Mean target or lure accuracy by serial position, session 2 only') +
  theme(axis.text = element_text(size=12),
        axis.title = element_text(size=15),
        title = element_text(size=15))

limAxisS2 = ggplot(plotDF, aes(x=SerialPos, y=Mean)) + 
  geom_point() +
  geom_errorbar(aes(ymin=Mean-SE, ymax=Mean+SE), width=0.1) +
  xlab('Serial Position') +
  ylab('Target/Lure Accuracy') +
  ggtitle('Mean target or lure accuracy by serial position, session 2 only, Y axis zoomed in') +
  theme(axis.text = element_text(size=12),
        axis.title = element_text(size=15),
        title = element_text(size=15))

##############################################################################################################################

library(gridExtra)
grid.arrange(fullAxis,limAxis,
             fullAxisS1,limAxisS1,
             fullAxisS2,limAxisS2,
             ncol=2)

##############################################################################################################################


plotDF = data.frame(SerialPos=c('SP1', 'SP2', 'SP3', 'SP4', 'SP1', 'SP2', 'SP3', 'SP4', 'SP1', 'SP2', 'SP3', 'SP4'), 
                    session=c('both','both','both','both','ses-01','ses-01','ses-01','ses-01','ses-02','ses-02','ses-02','ses-02'),
                    Mean=c(SP1mean,SP2mean,SP3mean,SP4mean,SP1meanS1,SP2meanS1,SP3meanS1,SP4meanS1,SP1meanS2,SP2meanS2,SP3meanS2,SP4meanS2), 
                    SE=c(SP1sem,SP2sem,SP3sem,SP4sem,SP1semS1,SP2semS1,SP3semS1,SP4semS1,SP1semS2,SP2semS2,SP3semS2,SP4semS2))


fullAxis = ggplot(plotDF, aes(x=SerialPos, y=Mean, color=session)) + 
  geom_point() +
  geom_errorbar(aes(ymin=Mean-SE, ymax=Mean+SE), width=0.1) +
  ylim(0,1) +
  xlab('Serial Position') +
  ylab('Target/Lure Accuracy') +
  ggtitle('Mean target or lure accuracy by serial position') +
  theme(axis.text = element_text(size=12),
        axis.title = element_text(size=15),
        title = element_text(size=15))

limAxis = ggplot(plotDF, aes(x=SerialPos, y=Mean, color=session)) + 
  geom_point() +
  geom_errorbar(aes(ymin=Mean-SE, ymax=Mean+SE), width=0.1) +
  xlab('Serial Position') +
  ylab('Target/Lure Accuracy') +
  ggtitle('Mean target or lure accuracy by serial position, session 2 only, Y axis zoomed in') +
  theme(axis.text = element_text(size=12),
        axis.title = element_text(size=15),
        title = element_text(size=15))

grid.arrange(fullAxis,limAxis,ncol=2)













