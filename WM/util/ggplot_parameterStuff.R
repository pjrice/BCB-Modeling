
library(tidyr)
library(dplyr)
library(ggplot2)
library(grid)
library(gridExtra)


parEsts = read.csv('Z:\\gp\\ACTR-WM\\data\\parEstResults\\Powell\\bounded\\fivePar\\fiveParEstResults.csv',header=TRUE)

subjMeas = read.csv('Z:\\gp\\ACTR-WM\\data\\parEstResults\\Powell\\bounded\\fivePar\\subjMeasures.csv',header=TRUE)
subjMeas = subjMeas[-c(1)]
colnames(subjMeas) = c('subjMeanRT','subjMeanAcc')

modelPreds = read.csv('Z:\\gp\\ACTR-WM\\data\\parEstResults\\Powell\\bounded\\fivePar\\modelPreds.csv',header=TRUE)


allDF = cbind(parEsts,subjMeas,modelPreds)

##############################################################################################################################
#parameter results

allDF$gaIAdiff = allDF$ga - allDF$ia

allDF %>% 
  select(partID,css,ga,ia,lf,bll,gaIAdiff) %>% 
  pivot_longer(-partID, values_to='value', names_to='parameter') %>% 
  group_by(parameter) %>% 
  summarise(meanVal = mean(value),
            sdVal = sd(value),
            rangeVal = range(value))

##############################################################################################################################
#function to produce histograms of parameter estimates

parEstHist = function(parName,parEstVec,xlims) {
  
  parDF = data.frame(parEstVec)
  colnames(parDF) = parName
  

  ggplot(parDF, aes_string(x=parName)) + 
    geom_histogram(bins=20, fill='blue') +
    xlim(xlims[1],xlims[2])+
    scale_y_continuous(expand=c(0,0)) +
    ggtitle(paste0('Histogram of estimated ',parName,' values')) +
    theme(line = element_line(size=1),
          text = element_text(size=15),
          panel.background = element_blank(),
          panel.grid = element_blank(),
          axis.line = element_line(color='black'),
          legend.position = c(0.9,0.9),
          aspect.ratio=1/2)
  
  
  
}



parEstHist('css',allDF$css,xlims=c(-1,0))

parEstHist('lf',allDF$lf,xlims=c(1,3.5))

parEstHist('bll',allDF$bll,xlims=c(0.2,0.8))

parEstHist('ga',allDF$ga,xlims=c(0,2))

parEstHist('ia',allDF$ia,xlims=c(0,2))


parEstHist('c',allDF$css,xlims=c(-1,0))

parEstHist('F',allDF$lf,xlims=c(1,3.5))

parEstHist('d',allDF$bll,xlims=c(0.2,0.8))

parEstHist('Wg',allDF$ga,xlims=c(0,2))

parEstHist('Wi',allDF$ia,xlims=c(0,2))

gaIAdiff = allDF$ga - allDF$ia
parEstHist('ga_minus_ia',gaIAdiff,xlims=c(-2,2))

##############################################################################################################################

parScatterPlot = function(parDF) {
  
  parNames=colnames(parDF)
  
  corrData = cor.test(parDF[,1],parDF[,2],method='pearson', conf.level=0.95)
  
  corr = round(corrData$estimate,digits=2)
  pval = round(corrData$p.value,digits=2)
  
  ggplot(parDF,aes_string(x=parNames[1],y=parNames[2])) +
    geom_point() +
    geom_smooth(method=lm, se=FALSE) +
    annotate("text", x=min(parDF[,1]), y=max(parDF[,2]), label=paste0('r = ',corr,'\np = ',pval)) +
    ggtitle(paste0(parNames[1],' parameter estimate versus ',parNames[2],' parameter estimate'))
  
}

parDF = data.frame('ga'=allDF$ga,'ia'=allDF$ia)
parScatterPlot(parDF)

parDF = data.frame('css'=allDF$css,'ga_minus_ia'=gaIAdiff)
parScatterPlot(parDF)

parDF = data.frame('bll'=allDF$bll,'ga_minus_ia'=gaIAdiff)
parScatterPlot(parDF)

##############################################################################################################################

test = allDF %>% select(ends_with('meanRT')) %>% pivot_longer(!subjMeanRT,names_to='model',values_to='prediction')

test$model = unlist(strsplit(test$model,'_'))[seq(1,length(unlist(strsplit(test$model,'_'))),2)]

colnames(test) = c('measure','model','prediction')

p.list = lapply(sort(unique(test$model)), function (i) {
  
  corrDF = test %>% filter(model==i)
  
  corrData = cor.test(corrDF$measure,corrDF$prediction)
  corr = round(corrData$estimate,digits=2)
  pval = round(corrData$p.value,digits=2)

  
  ggplot(test[test$model==i,], aes(x=measure,y=prediction)) + 
    geom_point() +
    geom_smooth(method=lm, se=FALSE) +
    annotate("text", x=0.5, y=0.9, label=paste0('r = ',corr,'\np = ',pval)) +
    facet_wrap(~model,scales='fixed')
})


p.list[[3]] = p.list[[3]] + ylim(0.4,1) + theme(axis.title.x=element_blank(),
                                                axis.title.y=element_blank())
p.list[[2]] = p.list[[2]] + ylim(0.4,1) + theme(axis.title.x=element_blank(),
                                                axis.title.y=element_blank())
p.list[[5]] = p.list[[5]] + ylim(0.4,1) + theme(axis.title.x=element_blank(),
                                                axis.title.y=element_blank())
p.list[[7]] = p.list[[7]] + ylim(0.4,1) + theme(axis.title.x=element_blank(),
                                                axis.title.y=element_blank())
p.list[[11]] = p.list[[11]] + ylim(0.4,1) + theme(axis.title.x=element_blank(),
                                                axis.title.y=element_blank())

p.list[[1]] = p.list[[1]] + ylim(0.4,1) + theme(axis.title.x=element_blank(),
                                                axis.title.y=element_blank())
p.list[[4]] = p.list[[4]] + ylim(0.4,1) + theme(axis.title.x=element_blank(),
                                                axis.title.y=element_blank())
p.list[[6]] = p.list[[6]] + ylim(0.4,1) + theme(axis.title.x=element_blank(),
                                                axis.title.y=element_blank())
p.list[[10]] = p.list[[10]] + ylim(0.4,1) + theme(axis.title.x=element_blank(),
                                                  axis.title.y=element_blank())

p.list[[9]] = p.list[[9]] + ylim(0.4,1) + theme(axis.title.x=element_blank(),
                                                axis.title.y=element_blank())
p.list[[12]] = p.list[[12]] + ylim(0.4,1) + theme(axis.title.x=element_blank(),
                                                  axis.title.y=element_blank())
p.list[[14]] = p.list[[14]] + ylim(0.4,1) + theme(axis.title.x=element_blank(),
                                                  axis.title.y=element_blank())

p.list[[8]] = p.list[[8]] + ylim(0.4,1) + theme(axis.title.x=element_blank(),
                                                axis.title.y=element_blank())
p.list[[13]] = p.list[[13]] + ylim(0.4,1) + theme(axis.title.x=element_blank(),
                                                  axis.title.y=element_blank())


c1title = textGrob("Leave one out")
c2title = textGrob("Leave two out")
c3title = textGrob("Leave three out")
c4title = textGrob("Leave four out")

ylabel = textGrob('Model\nprediction',rot=90)
xlabel = textGrob('Subject RT')
xlabel2 = textGrob('Subject RT',vjust=-6)

lay2 = rbind(c(NA,15,16,17,18),
             c(23,1,6,10,13),
             c(24,2,7,11,14),
             c(25,3,8,12,22),
             c(26,4,9,21,NA),
             c(27,5,20,NA,NA),
             c(NA,19,NA,NA,NA))



grid.arrange(p.list[[3]],  #1
             p.list[[2]],  #2
             p.list[[5]],  #3
             p.list[[7]],  #4
             p.list[[11]], #5
             p.list[[1]],  #6
             p.list[[4]],  #7
             p.list[[6]],  #8
             p.list[[10]], #9
             p.list[[9]],  #10
             p.list[[12]], #11
             p.list[[14]], #12
             p.list[[8]],  #13
             p.list[[13]], #14
             c1title,      #15
             c2title,      #16
             c3title,      #17
             c4title,      #18
             xlabel,       #19
             xlabel2,       #20
             xlabel2,       #21
             xlabel2,       #22
             ylabel,       #23
             ylabel,       #24
             ylabel,       #25
             ylabel,       #26
             ylabel,       #27
             layout_matrix=lay2,
             heights = c(0.25,1,1,1,1,1,0.25),
             widths = c(0.1,1,1,1,1))

##############################################################################################################################

test = allDF %>% select(ends_with('meanAcc')) %>% pivot_longer(!subjMeanAcc,names_to='model',values_to='prediction')

test$model = unlist(strsplit(test$model,'_'))[seq(1,length(unlist(strsplit(test$model,'_'))),2)]

colnames(test) = c('measure','model','prediction')


p.list = lapply(sort(unique(test$model)), function (i) {
  
  corrDF = test %>% filter(model==i)
  
  corrData = cor.test(corrDF$measure,corrDF$prediction)
  corr = round(corrData$estimate,digits=2)
  pval = round(corrData$p.value,digits=2)
  
  
  ggplot(test[test$model==i,], aes(x=measure,y=prediction)) + 
    geom_point() +
    geom_smooth(method=lm, se=FALSE) +
    annotate("text", x=0.6, y=0.9, label=paste0('r = ',corr,'\np = ',pval)) +
    facet_wrap(~model,scales='fixed') +
    theme(legend.position='none')
})


p.list[[3]] = p.list[[3]] + ylim(0.4,1) + xlim(0.6,1) + theme(axis.title.x=element_blank(),
                                                axis.title.y=element_blank())
p.list[[2]] = p.list[[2]] + ylim(0.4,1) + xlim(0.6,1) + theme(axis.title.x=element_blank(),
                                                axis.title.y=element_blank())
p.list[[5]] = p.list[[5]] + ylim(0.4,1) + xlim(0.6,1) + theme(axis.title.x=element_blank(),
                                                axis.title.y=element_blank())
p.list[[7]] = p.list[[7]] + ylim(0.4,1) + xlim(0.6,1) + theme(axis.title.x=element_blank(),
                                                axis.title.y=element_blank())
p.list[[11]] = p.list[[11]] + ylim(0.4,1) + xlim(0.6,1) + theme(axis.title.x=element_blank(),
                                                  axis.title.y=element_blank())

p.list[[1]] = p.list[[1]] + ylim(0.4,1) + xlim(0.6,1) + theme(axis.title.x=element_blank(),
                                                axis.title.y=element_blank())
p.list[[4]] = p.list[[4]] + ylim(0.4,1) + xlim(0.6,1) + theme(axis.title.x=element_blank(),
                                                axis.title.y=element_blank())
p.list[[6]] = p.list[[6]] + ylim(0.4,1) + xlim(0.6,1) + theme(axis.title.x=element_blank(),
                                                axis.title.y=element_blank())
p.list[[10]] = p.list[[10]] + ylim(0.4,1) + xlim(0.6,1) + theme(axis.title.x=element_blank(),
                                                  axis.title.y=element_blank())

p.list[[9]] = p.list[[9]] + ylim(0.4,1) + xlim(0.6,1) + theme(axis.title.x=element_blank(),
                                                axis.title.y=element_blank())
p.list[[12]] = p.list[[12]] + ylim(0.4,1) + xlim(0.6,1) + theme(axis.title.x=element_blank(),
                                                  axis.title.y=element_blank())
p.list[[14]] = p.list[[14]] + ylim(0.4,1) + xlim(0.6,1) + theme(axis.title.x=element_blank(),
                                                  axis.title.y=element_blank())

p.list[[8]] = p.list[[8]] + ylim(0.4,1) + xlim(0.6,1) + theme(axis.title.x=element_blank(),
                                                axis.title.y=element_blank())
p.list[[13]] = p.list[[13]] + ylim(0.4,1) + xlim(0.6,1) + theme(axis.title.x=element_blank(),
                                                  axis.title.y=element_blank())


c1title = textGrob("Leave one out")
c2title = textGrob("Leave two out")
c3title = textGrob("Leave three out")
c4title = textGrob("Leave four out")

ylabel = textGrob('Model\nprediction',rot=90)
xlabel = textGrob('Subject Acc')
xlabel2 = textGrob('Subject Acc',vjust=-6)



grid.arrange(p.list[[3]],  #1
             p.list[[2]],  #2
             p.list[[5]],  #3
             p.list[[7]],  #4
             p.list[[11]], #5
             p.list[[1]],  #6
             p.list[[4]],  #7
             p.list[[6]],  #8
             p.list[[10]], #9
             p.list[[9]],  #10
             p.list[[12]], #11
             p.list[[14]], #12
             p.list[[8]],  #13
             p.list[[13]], #14
             c1title,      #15
             c2title,      #16
             c3title,      #17
             c4title,      #18
             xlabel,       #19
             xlabel2,       #20
             xlabel2,       #21
             xlabel2,       #22
             ylabel,       #23
             ylabel,       #24
             ylabel,       #25
             ylabel,       #26
             ylabel,       #27
             layout_matrix=lay2,
             heights = c(0.25,1,1,1,1,1,0.25),
             widths = c(0.1,1,1,1,1))




##############################################################################################################################
# arcsin transformation of accuracy


test = allDF %>% 
  select(c(partID,ends_with('meanAcc'))) %>% 
  pivot_longer(!c(partID,subjMeanAcc),names_to='model',values_to='prediction') %>% 
  group_by(partID) %>% 
  mutate(subjMeanAcc=asin(sqrt(subjMeanAcc)), prediction=asin(sqrt(prediction)))


test$model = unlist(strsplit(test$model,'_'))[seq(1,length(unlist(strsplit(test$model,'_'))),2)]

colnames(test) = c('partID','measure','model','prediction')


p.list = lapply(sort(unique(test$model)), function (i) {
  
  corrDF = test %>% filter(model==i)
  
  corrData = cor.test(corrDF$measure,corrDF$prediction)
  corr = round(corrData$estimate,digits=2)
  pval = round(corrData$p.value,digits=2)
  
  
  ggplot(test[test$model==i,], aes(x=measure,y=prediction)) + 
    geom_point() +
    geom_smooth(method=lm, se=FALSE) +
    annotate("text", x=0.95, y=1.4, label=paste0('r = ',corr,'\np = ',pval)) +
    facet_wrap(~model,scales='fixed') +
    theme(legend.position='none')
})


p.list[[3]] = p.list[[3]] + ylim(0.7,1.5) + xlim(0.9,1.6) + theme(axis.title.x=element_blank(),
                                                              axis.title.y=element_blank())
p.list[[2]] = p.list[[2]] + ylim(0.7,1.5) + xlim(0.9,1.6) + theme(axis.title.x=element_blank(),
                                                              axis.title.y=element_blank())
p.list[[5]] = p.list[[5]] + ylim(0.7,1.5) + xlim(0.9,1.6) + theme(axis.title.x=element_blank(),
                                                              axis.title.y=element_blank())
p.list[[7]] = p.list[[7]] + ylim(0.7,1.5) + xlim(0.9,1.6) + theme(axis.title.x=element_blank(),
                                                              axis.title.y=element_blank())
p.list[[11]] = p.list[[11]] + ylim(0.7,1.5) + xlim(0.9,1.6) + theme(axis.title.x=element_blank(),
                                                                axis.title.y=element_blank())

p.list[[1]] = p.list[[1]] + ylim(0.7,1.5) + xlim(0.9,1.6) + theme(axis.title.x=element_blank(),
                                                              axis.title.y=element_blank())
p.list[[4]] = p.list[[4]] + ylim(0.7,1.5) + xlim(0.9,1.6) + theme(axis.title.x=element_blank(),
                                                              axis.title.y=element_blank())
p.list[[6]] = p.list[[6]] + ylim(0.7,1.5) + xlim(0.9,1.6) + theme(axis.title.x=element_blank(),
                                                              axis.title.y=element_blank())
p.list[[10]] = p.list[[10]] + ylim(0.7,1.5) + xlim(0.9,1.6) + theme(axis.title.x=element_blank(),
                                                                axis.title.y=element_blank())

p.list[[9]] = p.list[[9]] + ylim(0.7,1.5) + xlim(0.9,1.6) + theme(axis.title.x=element_blank(),
                                                              axis.title.y=element_blank())
p.list[[12]] = p.list[[12]] + ylim(0.7,1.5) + xlim(0.9,1.6) + theme(axis.title.x=element_blank(),
                                                                axis.title.y=element_blank())
p.list[[14]] = p.list[[14]] + ylim(0.7,1.5) + xlim(0.9,1.6) + theme(axis.title.x=element_blank(),
                                                                axis.title.y=element_blank())

p.list[[8]] = p.list[[8]] + ylim(0.7,1.5) + xlim(0.9,1.6) + theme(axis.title.x=element_blank(),
                                                              axis.title.y=element_blank())
p.list[[13]] = p.list[[13]] + ylim(0.7,1.5) + xlim(0.9,1.6) + theme(axis.title.x=element_blank(),
                                                                axis.title.y=element_blank())


c1title = textGrob("Leave one out")
c2title = textGrob("Leave two out")
c3title = textGrob("Leave three out")
c4title = textGrob("Leave four out")

ylabel = textGrob('Model\nprediction',rot=90)
xlabel = textGrob('Subject Acc')
xlabel2 = textGrob('Subject Acc',vjust=-6)



grid.arrange(p.list[[3]],  #1
             p.list[[2]],  #2
             p.list[[5]],  #3
             p.list[[7]],  #4
             p.list[[11]], #5
             p.list[[1]],  #6
             p.list[[4]],  #7
             p.list[[6]],  #8
             p.list[[10]], #9
             p.list[[9]],  #10
             p.list[[12]], #11
             p.list[[14]], #12
             p.list[[8]],  #13
             p.list[[13]], #14
             c1title,      #15
             c2title,      #16
             c3title,      #17
             c4title,      #18
             xlabel,       #19
             xlabel2,       #20
             xlabel2,       #21
             xlabel2,       #22
             ylabel,       #23
             ylabel,       #24
             ylabel,       #25
             ylabel,       #26
             ylabel,       #27
             layout_matrix=lay2,
             heights = c(0.25,1,1,1,1,1,0.25),
             widths = c(0.1,1,1,1,1))
















