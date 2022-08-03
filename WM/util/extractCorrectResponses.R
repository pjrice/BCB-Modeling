
library(dplyr)

###################################################################################################################
#extracts correct response data = all participants saw the same sequence of stimuli, so this only needs to be done once

######################################
#zero-back

ses1 = read.delim('Z:\\gp\\ACTR-WM\\data\\sub-100307\\ses-01\\WM_run1_TAB.txt')
ses2 = read.delim('Z:\\gp\\ACTR-WM\\data\\sub-100307\\ses-02\\WM_run2_TAB.txt')


ses1_zb = ses1 %>% filter(BlockType=='0-Back') %>% select(Stim.CRESP,TargetType)
ses2_zb = ses2 %>% filter(BlockType=='0-Back') %>% select(Stim.CRESP,TargetType)

zb_correctResponses = c(ses1_zb$Stim.CRESP,ses2_zb$Stim.CRESP)
zb_correctResponses = rbind(ses1_zb,ses2_zb)

#for targets, the correct response is "2"=="f"
#for lures/nontargets, the correct response is "3"=="j"
zb_correctResponses$Stim.CRESP[zb_correctResponses$Stim.CRESP==2] = 'f'
zb_correctResponses$Stim.CRESP[zb_correctResponses$Stim.CRESP=='3'] = 'j'


write.table(zb_correctResponses,'Z:\\gp\\ACTR-WM\\data\\zeroBack_correctResponses.csv', row.names=FALSE, col.names=FALSE, sep=',')

######################################
#two-back

ses1_2b = ses1 %>% filter(BlockType=='2-Back') %>% select(Stim.CRESP,TargetType)
ses2_2b = ses2 %>% filter(BlockType=='2-Back') %>% select(Stim.CRESP,TargetType)

twob_correctResponses = rbind(ses1_2b,ses2_2b)
twob_correctResponses$Stim.CRESP[twob_correctResponses$Stim.CRESP==2] = 'f'
twob_correctResponses$Stim.CRESP[twob_correctResponses$Stim.CRESP=='3'] = 'j'

write.table(twob_correctResponses,'Z:\\gp\\ACTR-WM\\data\\twoBack_correctResponses.csv', row.names=FALSE, col.names=FALSE, sep=',')

######################################
#zero- and two-back

ses1_all = ses1 %>% filter(Procedure.Block.=='TrialsPROC') %>% select(Stim.CRESP,TargetType)
ses2_all = ses2 %>% filter(Procedure.Block.=='TrialsPROC') %>% select(Stim.CRESP,TargetType)

all_correctResponses = rbind(ses1_all,ses2_all)

all_correctResponses$Stim.CRESP[all_correctResponses$Stim.CRESP==2] = 'f'
all_correctResponses$Stim.CRESP[all_correctResponses$Stim.CRESP=='3'] = 'j'
write.table(all_correctResponses,'Z:\\gp\\ACTR-WM\\data\\all_correctResponses.csv', row.names=FALSE, col.names=FALSE, sep=',')



