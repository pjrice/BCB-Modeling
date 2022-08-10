#script to plot HCP Working Memory d prime data

#https://plotly.com/r/3d-axes/

library(tidyr)
library(plotly)
library(ggplot2)

#loads the dataframe dPrimeDF
load('/home/pjrice/Desktop/dissertation/dPrime.RData')

# axis titles
# 'axx' == 'axis x'
axx = list(title='target hits vs nonlure FAs')
axy = list(title='lure hits vs nonlure FAs')
axz = list(title='arget hits vs lure FAs')

################################################################################################################
# session 1, 2 back

ses1_2Back = dPrimeDF %>% filter(session=='ses-01' & nback=='2Back') %>% spread(dPrime_cond, dPrime_val)

ses1_2Back_fig = plot_ly(x=ses1_2Back$target, 
                         y=ses1_2Back$lure, 
                         z=ses1_2Back$tVl, 
                         type='scatter3d', 
                         mode='markers')

ses1_2Back_fig = ses1_2Back_fig %>% layout(title ='d prime, session1, 2-back',
                                           scene = list(xaxis=axx,yaxis=axy,zaxis=axz))

################################################################################################################
# session 2, 2 back
ses2_2Back = dPrimeDF %>% filter(session=='ses-02' & nback=='2Back') %>% spread(dPrime_cond, dPrime_val)

ses2_2Back_fig = plot_ly(x=ses2_2Back$target, 
                         y=ses2_2Back$lure, 
                         z=ses2_2Back$tVl, 
                         type='scatter3d', 
                         mode='markers')

ses2_2Back_fig = ses2_2Back_fig %>% layout(title ='d prime, session2, 2-back',
                                           scene = list(xaxis=axx,yaxis=axy,zaxis=axz))

################################################################################################################
# session 1, 0 back
ses1_0Back = dPrimeDF %>% filter(session=='ses-01' & nback=='0Back') %>% spread(dPrime_cond, dPrime_val)

ses1_0Back_fig = plot_ly(x=ses1_0Back$target, 
                         y=ses1_0Back$lure, 
                         z=ses1_0Back$tVl, 
                         type='scatter3d', 
                         mode='markers')

ses1_0Back_fig = ses1_0Back_fig %>% layout(title ='d prime, session1, 0-back',
                                           scene = list(xaxis=axx,yaxis=axy,zaxis=axz))

################################################################################################################
# session 2, 0 back
ses2_0Back = dPrimeDF %>% filter(session=='ses-02' & nback=='0Back') %>% spread(dPrime_cond, dPrime_val)

ses2_0Back_fig = plot_ly(x=ses2_0Back$target, 
                         y=ses2_0Back$lure, 
                         z=ses2_0Back$tVl, 
                         type='scatter3d', 
                         mode='markers')

ses2_0Back_fig = ses2_0Back_fig %>% layout(title ='d prime, session2, 0-back',
                                           scene = list(xaxis=axx,yaxis=axy,zaxis=axz))

################################################################################################################
# both sessions, 2 back
twoBack = dPrimeDF %>% filter(session=='both' & nback=='2Back') %>% spread(dPrime_cond, dPrime_val)

twoBack_fig = plot_ly(x=twoBack$target, 
                      y=twoBack$lure, 
                      z=twoBack$tVl, 
                      type='scatter3d', 
                      mode='markers')

twoBack_fig = twoBack_fig %>% layout(title ='d prime, 2-back',
                                     scene = list(xaxis=axx,yaxis=axy,zaxis=axz))

################################################################################################################
# both sessions, 0 back
zeroBack = dPrimeDF %>% filter(session=='both' & nback=='0Back') %>% spread(dPrime_cond, dPrime_val)

zeroBack_fig = plot_ly(x=zeroBack$target, 
                       y=zeroBack$lure, 
                       z=zeroBack$tVl, 
                       type='scatter3d', 
                       mode='markers')

zeroBack_fig = zeroBack_fig %>% layout(title ='d prime, 0-back',
                                     scene = list(xaxis=axx,yaxis=axy,zaxis=axz))

################################################################################################################
# session 1, both nbacks

session1 = dPrimeDF %>% filter(session=='ses-01' & nback=='both') %>% spread(dPrime_cond, dPrime_val)

session1_fig = plot_ly(x=session1$target, 
                       y=session1$lure, 
                       z=session1$tVl, 
                       type='scatter3d', 
                       mode='markers')

session1_fig = session1_fig %>% layout(title ='d prime, session 1',
                                       scene = list(xaxis=axx,yaxis=axy,zaxis=axz))

################################################################################################################
# session 2, both nbacks

session2 = dPrimeDF %>% filter(session=='ses-02' & nback=='both') %>% spread(dPrime_cond, dPrime_val)

session2_fig = plot_ly(x=session2$target, 
                       y=session2$lure, 
                       z=session2$tVl, 
                       type='scatter3d', 
                       mode='markers')

session2_fig = session2_fig %>% layout(title ='d prime, session 2',
                                       scene = list(xaxis=axx,yaxis=axy,zaxis=axz))

################################################################################################################
# both sessions, both nbacks

generalDPrime = dPrimeDF %>% filter(session=='both' & nback=='both') %>% spread(dPrime_cond, dPrime_val)

generalDPrime_fig = plot_ly(x=generalDPrime$target, 
                            y=generalDPrime$lure, 
                            z=generalDPrime$tVl, 
                            type='scatter3d', 
                            mode='markers')

generalDPrime_fig = generalDPrime_fig %>% layout(title ='d prime, both sessions, both n backs',
                                       scene = list(xaxis=axx,yaxis=axy,zaxis=axz))



################################################################################################################
################################################################################################################
# d Prime between sessions

################################################################################################################

#2-back target versus nontargets
t2b_dP = dPrimeDF %>% filter(session!='both' & nback=='2Back' & dPrime_cond=='target') %>% select(partID,session,dPrime_val) %>% spread(session,dPrime_val)
colnames(t2b_dP) = c('partID', 'ses1', 'ses2')

ggplot(t2b_dP, aes(x=ses1, y=ses2)) +
  geom_point() +
  xlab('Session 1 d Prime') +
  ylab('Session 2 d Prime') +
  ggtitle('2-back target versus nontarget d Prime between sessions')


################################################################################################################

#2-back lure versus nontargets
l2b_dP = dPrimeDF %>% filter(session!='both' & nback=='2Back' & dPrime_cond=='lure') %>% select(partID,session,dPrime_val) %>% spread(session,dPrime_val)
colnames(l2b_dP) = c('partID', 'ses1', 'ses2')

ggplot(l2b_dP, aes(x=ses1, y=ses2)) +
  geom_point() +
  xlab('Session 1 d Prime') +
  ylab('Session 2 d Prime') +
  ggtitle('2-back lure versus nontarget d Prime between sessions')

################################################################################################################

#2-back target versus lure FAs
tvl2b_dP = dPrimeDF %>% filter(session!='both' & nback=='2Back' & dPrime_cond=='tVl') %>% select(partID,session,dPrime_val) %>% spread(session,dPrime_val)
colnames(tvl2b_dP) = c('partID', 'ses1', 'ses2')

ggplot(tvl2b_dP, aes(x=ses1, y=ses2)) +
  geom_point() +
  xlab('Session 1 d Prime') +
  ylab('Session 2 d Prime') +
  ggtitle('2-back target versus lure false alarm d Prime between sessions')

################################################################################################################

#0-back target versus nontargets
t0b_dP = dPrimeDF %>% filter(session!='both' & nback=='0Back' & dPrime_cond=='target') %>% select(partID,session,dPrime_val) %>% spread(session,dPrime_val)
colnames(t0b_dP) = c('partID', 'ses1', 'ses2')

ggplot(t0b_dP, aes(x=ses1, y=ses2)) +
  geom_point() +
  xlab('Session 1 d Prime') +
  ylab('Session 2 d Prime') +
  ggtitle('0-back target versus nontarget d Prime between sessions')


################################################################################################################

#0-back lure versus nontargets
l0b_dP = dPrimeDF %>% filter(session!='both' & nback=='0Back' & dPrime_cond=='lure') %>% select(partID,session,dPrime_val) %>% spread(session,dPrime_val)
colnames(l0b_dP) = c('partID', 'ses1', 'ses2')

ggplot(l0b_dP, aes(x=ses1, y=ses2)) +
  geom_point() +
  xlab('Session 1 d Prime') +
  ylab('Session 2 d Prime') +
  ggtitle('0-back lure versus nontarget d Prime between sessions')

################################################################################################################

#2-back target versus lure FAs
tvl0b_dP = dPrimeDF %>% filter(session!='both' & nback=='0Back' & dPrime_cond=='tVl') %>% select(partID,session,dPrime_val) %>% spread(session,dPrime_val)
colnames(tvl0b_dP) = c('partID', 'ses1', 'ses2')

ggplot(tvl0b_dP, aes(x=ses1, y=ses2)) +
  geom_point() +
  xlab('Session 1 d Prime') +
  ylab('Session 2 d Prime') +
  ggtitle('0-back target versus lure false alarm d Prime between sessions')








