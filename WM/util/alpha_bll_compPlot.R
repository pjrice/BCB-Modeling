


library(tidyr)
library(dplyr)
library(ggplot2)
library(ggpubr)
library(grid)
library(gridExtra)


parEsts = read.csv('Z:\\gp\\ACTR-WM\\data\\parEstResults\\Powell\\bounded\\fivePar\\fiveParEstResults.csv',header=TRUE)

alphaData = read.csv('Z:\\gp\\ACTR-WM\\data\\alphaData\\alpha_values_two_exps.csv')

alphaData$Alpha = alphaData$Alpha+0.2


bllData = parEsts %>% select(bll)

bllData$parameter='bll'

colnames(bllData) = c('value','parameter')

aData = alphaData %>% select(Alpha)
aData$parameter='alpha'
colnames(aData) = c('value','parameter')

twoParsData = rbind(bllData,aData)

meanBLL = mean(parEsts$bll)
meanAlpha = mean(alphaData$Alpha, na.rm=TRUE)

meanDF = data.frame(value=c(meanBLL,meanAlpha), parameter=c('bll','alpha'))


t.test(alphaData$Alpha,parEsts$bll,alternative='two.sided',var.equal=FALSE)
var.test(alphaData$Alpha,parEsts$bll,alternative='two.sided')

plotTitle = expression(atop('Comparison of estimated'~italic('bll')~'values and','adjusted'~alpha~'values'))

plotTitle = expression('Comparison of estimated'~italic('bll')~'values and adjusted'~alpha~'values')



ggplot(twoParsData, aes(x=value, fill=parameter)) +
  geom_histogram(position='identity',alpha=0.5) +
  #geom_vline(data=meanDF, aes(xintercept=value, color=parameter), linetype='dashed', size=2) +
  geom_segment(data=meanDF, aes(x=value, xend=value, y=0, yend=30, color=parameter), linetype='dashed', size=2) +
  #geom_bracket(xmin=meanAlpha,xmax=meanBLL,label = "t-test, p = 0.81",y.position=33,inherit.aes = FALSE,size=1,label.size=5) +
  xlab('Parameter value') +
  scale_y_continuous(limits=c(0,40), expand=c(0,0)) +
  scale_fill_discrete(labels=c(expression(alpha),expression(italic('bll')))) +
  scale_color_discrete(labels=c(expression(alpha),expression(italic('bll')))) +
  ggtitle(plotTitle) +
  theme(line = element_line(size=1),
        text = element_text(size=15),
        panel.background = element_blank(),
        panel.grid = element_blank(),
        axis.line = element_line(color='black'),
        legend.position = c(0.9,0.9),
        legend.title = element_blank(),
        aspect.ratio=1/2.75)



