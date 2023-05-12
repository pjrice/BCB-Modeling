# R packages 
#These packages are used for plotting the data
library(ggplot2)
library(ggpubr)
#I use this to get a truncated normal distribution, 
#however I could have just used a beta ditribution
library(truncnorm)
#coda package is used to compute the Gelman & Rubin Statistic
library(coda)
#ABC Sampling Functions
#--------------------------------------------------------------------------------------------------------------------
Sample_Prior           = function(){
#Sample Prior function
#   - ARGUMENTS - takes in no arguments 
#   - RETURNS   - a list of a parameter values samples from the predetermined parameters value
  
Parameters =   rbeta(1, 1, 1) # sample value from beta distribution with flat priors 

#As we develop models with more parameters we will have to modify how we store the parameter values,
# either in a list.
return(Parameters) 
}
Hamiltonion_Sampling   = function(Individual_1_History, Individual_2_History, Sample, Sample_Prev, i){
  #ARGUMENTS: 
  #     - Individual_1_History, This is a list of posterior samples representing the individual subject 1
  #     - Individual_2_History, This is a list of posterior samples representing the individual subject 2
  #     - Sample              , Current population mean parameter 
  #     - Sample_Prev         , Previously accepted population mean parameter
  #     - i                   , represents the iteration of the Markov Chain
   
  #RETURN
  #     - Returns the liklihood ratio for the population parameter

  #Compute the likelihood ratio between the previous sample parameter and the current sample
  #Current likelihood value
  Current_Sample   = sum( dbeta( c(Individual_1_History[i-1], Individual_2_History[i-1]),      Sample * 2, (1 - Sample)      * 2, log = T )  ) 
  #Previous likelihoood value
  Previous_Sample  = sum( dbeta( c(Individual_1_History[i-1], Individual_2_History[i-1]), Sample_Prev * 2, (1 - Sample_Prev) * 2, log = T )  )
  #Compute Likelihood ratio
  Likelihood_Ratio = Current_Sample - Previous_Sample
  return(Likelihood_Ratio)
}
Markov_Chain           = function(Tuning, DV){
  # ARGUMENTS
  #  - Tuning Parameter , Tuning parameter for the ABC sampling algorithm
  #  - DV               , Data that the model is fitting
  #RETURN
  #   -Returns the estimated parameter values for a single Markov Chain
   
  # Markov_Chain funtion runs a single instance of a markov chain of the given model 
  # and is called in the main model function inorder to implement multiple markov Chains
  
  for(i in 1:10000){ #Markov Chain iterates for 10000 times, in the future add Markov chain length as an argument in the function

    print(i)
    
    
    #Estimate the Sample Parameter
    if(i == 1){ #if i is equal to 1 then initialize sample variable from the prior
      
      Sample       = Sample_Prior()
      
    } else { #if i is not equal to 1, then determine the Sample parameter VIA Hamiltonion sampling. 
      
      Sample       =  Sample_Prior()      # Take one sample from Prior distribution
      Sample_Prev  = Sample_History[i-1]  # From the previous value (i-1) Sample_History array 
      
      r = Hamiltonion_Sampling( Individual_1_History, Individual_2_History, Sample, Sample_Prev, i )  # the likelihood ratio between the current and previous value

      # if r (likelihood ratio) is less than randomly sampled value then or equal to the liklihood ratio 
      # then we keep the newly sampled value else we keep the previous Sample Value
      if( log(runif(1, 0,1))  <= r){ Sample } else {Sample = Sample_Prev } 
      
    }
    
    #Sample parameters for Individual participants, keep in mind that for this example we are holding the rate parameter constant 
    Individual_1 = rbeta(1, Sample[1] * 10, (1-Sample[1]) * 10) # Individual_1, Sampled value for individual 1
    Individual_2 = rbeta(1, Sample[1] * 10, (1-Sample[1]) * 10) # Individual_2, Sampled value for indiivdual 2
    
    #-----------------------------------------------------------------------------------------------
    # Once we get this formulation integrated with ACT-R would go here
    
    #--------------------------------Send Parameters to ACT-R here------------------------
    #---------------------------------ACT-R Model Returns behavior------------------------
    #---------Summerize behavior in a meaninful way to compare against participants data
    #-----------------------------------------------------------------------------------------------
    
    #Compute the residual between model predictions and observed data
    Distance_1 = sqrt(  mean(   (DV[1:50]  - Individual_1[1])^2 ) )  # Root Mean Squared Deviation between Individual_1 parameter and Subject 1's Data
    Distance_2 = sqrt(  mean( (DV[51:100]  - Individual_2[1])^2 ) )  # Root Mean Squared Deviation between Individual_2 parameter and Subject 1's Data  
    
    #add together residual from all participants
    Distance = Distance_1 + Distance_2   # Add the distances together
    
    if(i == 1){Distance_Post = 0} #if i == 1 then intialize Distance_Post to 0
    
    #Compute Liklihood ratio to ABC sampling
    alpha    = dnorm(Distance/Tuning, log = T) - dnorm(Distance_Post/Tuning, log = T) # generate the likelihood ratio for individual participants using the Distance variable and the Tuning Parameter
    #Sample random value
    p        = log( runif(1, 0 , 1) ) #Sample random variable to compare against alpha variable
    
    #Save the model results
    if(i == 1){ #if i is 1 then we initialize 4 differnt array that store the results for each markov chain
      Sample_History         = Sample
      Individual_1_History   = Individual_1[1]
      Individual_2_History   = Individual_2[1]
      Distance_Post          = Distance
      
    } else { #if i is not equal to 1, then we store the results based on the p and alpha variable
      
      if(p <= alpha){ # if p is less then alpha then we store the newly sampled parameter values
        Sample_History         = c(Sample_History, Sample )
        Individual_1_History   = c(Individual_1_History, Individual_1[1] ) 
        Individual_2_History   = c(Individual_2_History, Individual_2[1] )
        Distance_Post = Distance  
        
      } else { # if  p is greater and alpha then we store the previously sampled values
        Sample_History         = c(Sample_History      , Sample_History[i-1] )
        Individual_1_History   = c(Individual_1_History, Individual_1_History[i-1] ) 
        Individual_2_History   = c(Individual_2_History, Individual_2_History[i-1] )
        
      }
    }
  
    
  }
  
  #Once the markov chain is finished then we store the results into a data frame 
  Chain           = as.data.frame( cbind(1:length(Sample_History), Sample_History, Individual_1_History, Individual_2_History))
  #rename the columnes of the dataframe
  colnames(Chain) = c("Sample", "Sample_Mean", "Individual_1", "Individual_2")
  #Return the Chain varaible
  return(Chain)
}
ABC_Hierarchical_Model = function(Tuning, DV){
  #This funciton runs the individual markov chains, given the data and tuning parameters 
  #PARAMETERS
  #Tuning parmaeters: Parmaeter controls the likelihood function for the ABC samplers
  #DV: the Data for the Individual participants
  #Note: this could be paralized in the future
  #RETURNS
  # The results from the ABC BHM Model
  Chain_1 = Markov_Chain(Tuning, DV)  # Run chain 1
  Chain_2 = Markov_Chain(Tuning, DV)  # Run chain 2
  Chain_3 = Markov_Chain(Tuning, DV)  # Run chain 3
  
  #label the Chains
  Chain_1$Chain = 1 
  Chain_2$Chain = 2
  Chain_3$Chain = 3
  
  #Rbind the data together
  Data = rbind(Chain_1, Chain_2, Chain_3) 
  #Return the data together.s
  return(Data)  
}
#--------------------------------------------------------------------------------------------------------------------
#Generate the data
Sub  = c( rep(1, 50) , rep(2, 50))
DV   = c( rep(.3, 50), rep(.7, 50) )
DV   = c( rtruncnorm(50, .3, .05, a= 0,b=1), rtruncnorm(50, .7, .05, a= 0, b = 1) )
Obs  = as.data.frame( cbind(Sub, DV) )
#--------------------------------------------------------------------------------------------------------------------
# Run the Various Model Simulation manipulating the the Turing parametetr
Tuning_05 = ABC_Hierarchical_Model(.05, DV)
Tuning_10 = ABC_Hierarchical_Model(.10, DV)
Tuning_15 = ABC_Hierarchical_Model(.15, DV)
Tuning_20 = ABC_Hierarchical_Model(.20, DV)
#--------------------------------------------------------------------------------------------------------------------
#Observse the results
#Here is the Simulated Data
{
ggplot(Obs, aes(DV, group = Sub) ) +
  geom_density(aes(fill = as.factor(Sub) ) ) + 
  xlim(0,1) +
  xlab("Ability") + ylab("Density") +
  labs(fill = "Simulated Data")  +
  ggtitle("Generated Data" ) + 
  theme(
    title      = element_text(size = 16),
    axis.title = element_text(size = 14),
    axis.text  = element_text(size = 12)
  )

}
#--------------------------------------------------------------------------------------------------------------------
#Here we observe the Markov Chain of the Various simulations
{
title_size      = 14
axis_title_size = 14
axis_text_size  = 12

Sample_Mean_Tau_05 = ggplot(Tuning_05[Tuning_05$Sample > 5000, ], aes(Sample, Sample_Mean, group = Chain) ) +
  geom_line( aes(col = as.factor(Chain) )) +
  xlab("Sample") + ylab("Value")+
  ggtitle("Tau .05: Population Mean") +
  labs(col = "Chain") +
  ylim(0,1) +
  theme(
    title      = element_text(size = title_size),
    axis.title = element_text(size = axis_title_size),
    axis.text  = element_text(size = axis_text_size)
  )

Sample_Mean_Tau_10 = ggplot(Tuning_10[Tuning_10$Sample > 5000, ], aes(Sample, Sample_Mean, group = Chain) ) +
  geom_line( aes(col = as.factor(Chain) )) +
  xlab("Sample") + ylab("Value")+
  ggtitle("Tau .1: Population Mean") +
  labs(col = "Chain") +
  ylim(0,1) +
  theme(
    title      = element_text(size = title_size),
    axis.title = element_text(size = axis_title_size),
    axis.text  = element_text(size = axis_text_size)
  )

Sample_Mean_Tau_15 = ggplot(Tuning_15[Tuning_15$Sample > 5000, ], aes(Sample, Sample_Mean, group = Chain) ) +
  geom_line( aes(col = as.factor(Chain) )) +
  xlab("Sample") + ylab("Value")+
  ggtitle("Tau .15: Population Mean") +
  labs(col = "Chain") +
  ylim(0,1) +
  theme(
    title      = element_text(size = title_size),
    axis.title = element_text(size = axis_title_size),
    axis.text  = element_text(size = axis_text_size)
  )


Sample_Mean_Tau_20 = ggplot(Tuning_20[Tuning_20$Sample > 5000, ], aes(Sample, Sample_Mean, group = Chain) ) +
  geom_line( aes(col = as.factor(Chain) )) +
  xlab("Sample") + ylab("Value")+
  ggtitle("Tau .20: Population Mean") +
  labs(col = "Chain") +
  ylim(0,1) +
  theme(
    title      = element_text(size = title_size),
    axis.title = element_text(size = axis_title_size),
    axis.text  = element_text(size = axis_text_size)
  )


ggarrange(Sample_Mean_Tau_05, 
          Sample_Mean_Tau_10, 
          Sample_Mean_Tau_15, 
          Sample_Mean_Tau_20,
          ncol = 2, nrow = 2)
}
#--------------------------------------------------------------------------------------------------------------------------------------------
#Here we look at the estiamted posterior distribution
{
title_size      = 14
axis_title_size = 14
axis_text_size  = 12

Posterior_Tau_05 = ggplot(Tuning_05[Tuning_05$Sample > 5000, ], aes( Sample_Mean) ) +
  #geom_density( aes( fill = "Posterior_Mean" ) ) +
  geom_density( aes(Individual_1, fill = "Posterior Subj 1" ), alpha = .25 ) +
  geom_density( aes(Individual_2, fill = "Posterior Subj 2" ), alpha = .25 ) +
  geom_density(data = Obs, aes(DV, group = as.factor(Sub), fill = "Data"), alpha = .25) +
  labs(fill = "Parameter") +
  xlim(0,1) +
  xlab("Sample") + ylab("Value")+
  ggtitle("Posterior Samples") +
  theme(
    title      = element_text(size = title_size),
    axis.title = element_text(size = axis_title_size),
    axis.text  = element_text(size = axis_text_size)
  )


Posterior_Tau_10 = ggplot(Tuning_10[Tuning_10$Sample > 5000, ], aes( Sample_Mean) ) +
  #geom_density( aes( fill = "Posterior_Mean" ) ) +
  geom_density( aes(Individual_1, fill = "Posterior Subj 1" ), alpha = .25 ) +
  geom_density( aes(Individual_2, fill = "Posterior Subj 2" ), alpha = .25 ) +
  geom_density(data = Obs, aes(DV, group = as.factor(Sub), fill = "Data"), alpha = .25) +
  labs(fill = "Parameter") +
  xlim(0,1) +
  xlab("Sample") + ylab("Value")+
  ggtitle("Posterior Samples") +
  theme(
    title      = element_text(size = title_size),
    axis.title = element_text(size = axis_title_size),
    axis.text  = element_text(size = axis_text_size)
  )

Posterior_Tau_15 = ggplot(Tuning_15[Tuning_15$Sample > 5000, ], aes( Sample_Mean) ) +
  #geom_density( aes( fill = "Posterior_Mean" ) ) +
  geom_density( aes(Individual_1, fill = "Posterior Subj 1" ), alpha = .25 ) +
  geom_density( aes(Individual_2, fill = "Posterior Subj 2" ), alpha = .25 ) +
  geom_density(data = Obs, aes(DV, group = as.factor(Sub), fill = "Data"), alpha = .25) +
  labs(fill = "Parameter") +
  xlim(0,1) +
  xlab("Sample") + ylab("Value")+
  ggtitle("Posterior Samples") +
  theme(
    title      = element_text(size = title_size),
    axis.title = element_text(size = axis_title_size),
    axis.text  = element_text(size = axis_text_size)
  )

Posterior_Tau_20 = ggplot(Tuning_20[Tuning_20$Sample > 5000, ], aes( Sample_Mean) ) +
  #geom_density( aes( fill = "Posterior_Mean" ) ) +
  geom_density( aes(Individual_1, fill = "Posterior Subj 1" ), alpha = .25 ) +
  geom_density( aes(Individual_2, fill = "Posterior Subj 2" ), alpha = .25 ) +
  geom_density(data = Obs, aes(DV, group = as.factor(Sub), fill = "Data"), alpha = .25) +
  labs(fill = "Parameter") +
  xlim(0,1) +
  xlab("Sample") + ylab("Value")+
  ggtitle("Posterior Samples") +
  theme(
    title      = element_text(size = title_size),
    axis.title = element_text(size = axis_title_size),
    axis.text  = element_text(size = axis_text_size)
  )

ggarrange(Posterior_Tau_05, 
          Posterior_Tau_10, 
          Posterior_Tau_15, 
          Posterior_Tau_20,
          ncol = 2, nrow = 2)
}
#-----------------------------------------------------------------------------------------------------------------------------
{
#Here we assess the convergence of the Markov Chain

Tau_05 = mcmc.list(
  as.mcmc(Tuning_05$Sample_Mean[Tuning_05$Chain == 1]),
  as.mcmc(Tuning_05$Sample_Mean[Tuning_05$Chain == 2]),
  as.mcmc(Tuning_05$Sample_Mean[Tuning_05$Chain == 3])
)

Tau_10 = mcmc.list(
  as.mcmc(Tuning_10$Sample_Mean[Tuning_15$Chain == 1]),
  as.mcmc(Tuning_10$Sample_Mean[Tuning_15$Chain == 2]),
  as.mcmc(Tuning_10$Sample_Mean[Tuning_15$Chain == 3])
)


Tau_15 = mcmc.list(
  as.mcmc(Tuning_15$Sample_Mean[Tuning_15$Chain == 1]),
  as.mcmc(Tuning_15$Sample_Mean[Tuning_15$Chain == 2]),
  as.mcmc(Tuning_15$Sample_Mean[Tuning_15$Chain == 3])
)

Tau_20 = mcmc.list(
  as.mcmc(Tuning_20$Sample_Mean[Tuning_15$Chain == 1]),
  as.mcmc(Tuning_20$Sample_Mean[Tuning_15$Chain == 2]),
  as.mcmc(Tuning_20$Sample_Mean[Tuning_15$Chain == 3])
)


GD_05 = gelman.diag(Tau_05) 
GD_10 = gelman.diag(Tau_10)
GD_15 = gelman.diag(Tau_15)
GD_20 = gelman.diag(Tau_20)


Gelman_Diag = data.frame(
  Tau = c(.05, .1, .15, .2),
  Point.est = c(GD_05$psrf[1], GD_10$psrf[1],GD_15$psrf[1],GD_20$psrf[1]),
  Upper_CI = c(GD_05$psrf[2], GD_10$psrf[2],GD_15$psrf[2],GD_20$psrf[2])
)

ggplot(Gelman_Diag, aes(Tau, Point.est) ) +
  geom_line(aes(col = "Point.est") ) +
  geom_point(aes(col = "Point.est") )  +
  geom_line( aes(Tau, Upper_CI, col = "Upper CI") ) +
  geom_point(aes(Tau, Upper_CI, col = "Upper CI") ) +
  labs(col = "Gelman & Rubin Statistic") +
  xlab("Tau Value") + ylab("R Hat (Lower is better)") +
  ggtitle("Markov Chain Diagonstic") +
  theme(
    title = element_text(size = 16),
    axis.title = element_text(size = 14),
    axis.text  = element_text(size = 12)
  )
}
