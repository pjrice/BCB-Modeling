

library(dplyr)


HCP_beh = read.csv('C:\\Users\\Patrick\\Desktop\\HCP_beh\\HCP_beh.csv')

partIDs = list.dirs('C:\\Users\\Patrick\\Desktop\\labMeeting_5.4_plots\\zb\\zb',full.names=FALSE,recursive=FALSE)

partIDs = sapply(strsplit(partIDs,'sub-'),tail,1)



partData = HCP_beh %>% filter(Subject %in% partIDs)


#get ages of participants
partMinAges = as.numeric(sapply(strsplit(partData$Age,'-'),'[',1))
partMaxAges = as.numeric(sapply(strsplit(partData$Age,'-'),tail,1))

levels(as.factor(HCP_beh$Age))

sum(as.numeric(partData$Age=='22-25'))
sum(as.numeric(partData$Age=='26-30'))
sum(as.numeric(partData$Age=='31-35'))
sum(as.numeric(partData$Age=='36+'))


minAge = min(partMinAges,na.rm=TRUE)
maxAge = max(partMaxAges,na.rm=TRUE)

#get number of males/females
numFemale = sum(as.numeric(partData$Gender == 'F'))