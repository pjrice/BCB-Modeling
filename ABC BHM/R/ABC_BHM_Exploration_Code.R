#Python Code
#Different Various Participants
#------------------------------------
dv_1 = list(truncnorm.rvs(a=0, b=1, loc=0.5  , scale=0.05, size=50)) + list(truncnorm.rvs(a=0, b=1, loc=0.5  , scale=0.05, size=50))
dv_2 = list(truncnorm.rvs(a=0, b=1, loc=0.4  , scale=0.05, size=50)) + list(truncnorm.rvs(a=0, b=1, loc=0.6  , scale=0.05, size=50))
dv_3 = list(truncnorm.rvs(a=0, b=1, loc=0.3  , scale=0.05, size=50)) + list(truncnorm.rvs(a=0, b=1, loc=0.7  , scale=0.05, size=50))
dv_4 = list(truncnorm.rvs(a=0, b=1, loc=0.2  , scale=0.05, size=50)) + list(truncnorm.rvs(a=0, b=1, loc=0.8  , scale=0.05, size=50))
dv_5 = list(truncnorm.rvs(a=0, b=1, loc=0.1  , scale=0.05, size=50)) + list(truncnorm.rvs(a=0, b=1, loc=0.9  , scale=0.05, size=50))
dv_6 = list(truncnorm.rvs(a=0, b=1, loc=0.01 , scale=0.05, size=50)) + list(truncnorm.rvs(a=0, b=1, loc=0.99, scale=0.05, size=50))
#Model Runs
#------------------------------------
Example_1 = abc_hierarchical_model(.2 , dv_1)
Example_2 = abc_hierarchical_model(.2 , dv_2)
Example_3 = abc_hierarchical_model(.2 , dv_3)   
Example_4 = abc_hierarchical_model(.2 , dv_4)
Example_5 = abc_hierarchical_model(.2 , dv_5)
Example_6 = abc_hierarchical_model(.2 , dv_6)
#Save Data
#------------------------------------
Example_1.to_csv('/home/ausmanpa/gp/BCB-Modeling/ABC BHM R Code/pyData/Example_1.csv')    
Example_2.to_csv('/home/ausmanpa/gp/BCB-Modeling/ABC BHM R Code/pyData/Example_2.csv')    
Example_3.to_csv('/home/ausmanpa/gp/BCB-Modeling/ABC BHM R Code/pyData/Example_3.csv')    
Example_4.to_csv('/home/ausmanpa/gp/BCB-Modeling/ABC BHM R Code/pyData/Example_4.csv')    
Example_5.to_csv('/home/ausmanpa/gp/BCB-Modeling/ABC BHM R Code/pyData/Example_5.csv')    
Example_6.to_csv('/home/ausmanpa/gp/BCB-Modeling/ABC BHM R Code/pyData/Example_6.csv')    
########################################################################################################################################################################################################
# R anlaysis Code
HDIofMCMC              <- function( sampleVec , credMass=0.95 ) {
  # Computes highest density interval from a sample of representative values,
  #   estimated as shortest credible interval.
  # Arguments:
  #   sampleVec
  #     is a vector of representative values from a probability distribution.
  #   credMass
  #     is a scalar between 0 and 1, indicating the mass within the credible
  #     interval that is to be estimated.
  # Value:
  #   HDIlim is a vector containing the limits of the HDI
  sortedPts = sort( sampleVec )
  ciIdxInc = ceiling( credMass * length( sortedPts ) )
  nCIs = length( sortedPts ) - ciIdxInc
  ciWidth = rep( 0 , nCIs )
  for ( i in 1:nCIs ) {
    ciWidth[ i ] = sortedPts[ i + ciIdxInc ] - sortedPts[ i ]
  }
  HDImin = sortedPts[ which.min( ciWidth ) ]
  HDImax = sortedPts[ which.min( ciWidth ) + ciIdxInc ]
  HDIlim = c( HDImin , HDImax )
  return( HDIlim )
}
#---------------------------------------------------------------------------------------------------------
# Example 1
DV_1   = c( rtruncnorm(50, .5, .05, a= 0,b=1), rtruncnorm(50, .5, .05, a= 0, b = 1) )
# Example 2
DV_2   = c( rtruncnorm(50, .4, .05, a= 0,b=1), rtruncnorm(50, .6, .05, a= 0, b = 1) )
# Example 3
DV_3   = c( rtruncnorm(50, .3, .05, a= 0,b=1), rtruncnorm(50, .7, .05, a= 0, b = 1) )
# Example 4
DV_4   = c( rtruncnorm(50, .2, .05, a= 0,b=1), rtruncnorm(50, .8, .05, a= 0, b = 1) )
# Example 5
DV_5   = c( rtruncnorm(50, .1, .05, a= 0,b=1), rtruncnorm(50, .9, .05, a= 0, b = 1) )
# Example 6
DV_6   = c( rtruncnorm(50, .01, .05, a= 0,b=1), rtruncnorm(50, .99, .05, a= 0, b = 1) )
#---------------------------------------------------------------------------------------------------------
Obs_1  = as.data.frame( cbind(Sub, DV_1) )
Obs_2  = as.data.frame( cbind(Sub, DV_2) )
Obs_3  = as.data.frame( cbind(Sub, DV_3) )
Obs_4  = as.data.frame( cbind(Sub, DV_4) )
Obs_5  = as.data.frame( cbind(Sub, DV_5) )
Obs_6  = as.data.frame( cbind(Sub, DV_6) )
#---------------------------------------------------------------------------------------------------------
#Plot the data
{
  title_size      = 14
  axis_title_size = 14
  axis_text_size  = 12
  
  Example_1_Post = ggplot(Example_1[Example_1$Sample > 5000, ], aes( Sample_Mean) ) +
    #geom_density( aes( fill = "Posterior_Mean" ) ) +
    geom_density( aes(Individual_1, fill = "Posterior Subj 1" ), alpha = .25 ) +
    geom_density( aes(Individual_2, fill = "Posterior Subj 2" ), alpha = .25 ) +
    geom_density(data = Obs_1, aes(DV_1, group = as.factor(Sub), fill = "Data"), alpha = .25) +
    labs(fill = "Parameter") +
    xlim(0,1) +
    xlab("Sample") + ylab("Value")+
    ggtitle("Posterior Samples") +
    theme(
      title      = element_text(size = title_size),
      axis.title = element_text(size = axis_title_size),
      axis.text  = element_text(size = axis_text_size)
    )
  
  Example_2_Post = ggplot(Example_2[Example_2$Sample > 5000, ], aes( Sample_Mean) ) +
    #geom_density( aes( fill = "Posterior_Mean" ) ) +
    geom_density( aes(Individual_1, fill = "Posterior Subj 1" ), alpha = .25 ) +
    geom_density( aes(Individual_2, fill = "Posterior Subj 2" ), alpha = .25 ) +
    geom_density(data = Obs_2, aes(DV_2, group = as.factor(Sub), fill = "Data"), alpha = .25) +
    labs(fill = "Parameter") +
    xlim(0,1) +
    xlab("Sample") + ylab("Value")+
    ggtitle("Posterior Samples") +
    theme(
      title      = element_text(size = title_size),
      axis.title = element_text(size = axis_title_size),
      axis.text  = element_text(size = axis_text_size)
    )
  
  Example_3_Post = ggplot(Example_3[Example_3$Sample > 5000, ], aes( Sample_Mean) ) +
    #geom_density( aes( fill = "Posterior_Mean" ) ) +
    geom_density( aes(Individual_1, fill = "Posterior Subj 1" ), alpha = .25 ) +
    geom_density( aes(Individual_2, fill = "Posterior Subj 2" ), alpha = .25 ) +
    geom_density(data = Obs_3, aes(DV_3, group = as.factor(Sub), fill = "Data"), alpha = .25) +
    labs(fill = "Parameter") +
    xlim(0,1) +
    xlab("Sample") + ylab("Value")+
    ggtitle("Posterior Samples") +
    theme(
      title      = element_text(size = title_size),
      axis.title = element_text(size = axis_title_size),
      axis.text  = element_text(size = axis_text_size)
    )
  
  Example_4_Post = ggplot(Example_4[Example_4$Sample > 5000, ], aes( Sample_Mean) ) +
    #geom_density( aes( fill = "Posterior_Mean" ) ) +
    geom_density( aes(Individual_1, fill = "Posterior Subj 1" ), alpha = .25 ) +
    geom_density( aes(Individual_2, fill = "Posterior Subj 2" ), alpha = .25 ) +
    geom_density(data = Obs_4, aes(DV_4, group = as.factor(Sub), fill = "Data"), alpha = .25) +
    labs(fill = "Parameter") +
    xlim(0,1) +
    xlab("Sample") + ylab("Value")+
    ggtitle("Posterior Samples") +
    theme(
      title      = element_text(size = title_size),
      axis.title = element_text(size = axis_title_size),
      axis.text  = element_text(size = axis_text_size)
    )
  
  Example_5_Post = ggplot(Example_5[Example_5$Sample > 5000, ], aes( Sample_Mean) ) +
    #geom_density( aes( fill = "Posterior_Mean" ) ) +
    geom_density( aes(Individual_1, fill = "Posterior Subj 1" ), alpha = .25 ) +
    geom_density( aes(Individual_2, fill = "Posterior Subj 2" ), alpha = .25 ) +
    geom_density(data = Obs_5, aes(DV_5, group = as.factor(Sub), fill = "Data"), alpha = .25) +
    labs(fill = "Parameter") +
    xlim(0,1) +
    xlab("Sample") + ylab("Value")+
    ggtitle("Posterior Samples") +
    theme(
      title      = element_text(size = title_size),
      axis.title = element_text(size = axis_title_size),
      axis.text  = element_text(size = axis_text_size)
    )
  
  
  Example_6_Post = ggplot(Example_6[Example_6$Sample > 5000, ], aes( Sample_Mean) ) +
    #geom_density( aes( fill = "Posterior_Mean" ) ) +
    geom_density( aes(Individual_1, fill = "Posterior Subj 1" ), alpha = .25 ) +
    geom_density( aes(Individual_2, fill = "Posterior Subj 2" ), alpha = .25 ) +
    geom_density(data = Obs_6, aes(DV_6, group = as.factor(Sub), fill = "Data"), alpha = .25) +
    labs(fill = "Parameter") +
    xlim(0,1) +
    xlab("Sample") + ylab("Value")+
    ggtitle("Posterior Samples") +
    theme(
      title      = element_text(size = title_size),
      axis.title = element_text(size = axis_title_size),
      axis.text  = element_text(size = axis_text_size)
    )
  
  
  
  ggarrange(Example_1_Post, 
            Example_2_Post, 
            Example_3_Post, 
            Example_4_Post, 
            Example_5_Post, 
            Example_6_Post, 
            ncol = 2, nrow = 3)
}
#Examine the 95HDI of the different simulations
{
  
  Example_1_Results = Example_1 %>%
    mutate(
      Sample_Mean_H_HDI = HDIofMCMC( Sample_Mean[Sample > 5000] )[2],
      Sample_Mean_L_HDI = HDIofMCMC( Sample_Mean[Sample > 5000] )[1],
      Sub_1_Mean_H_HDI  = HDIofMCMC( Sample_Mean[Sample > 5000] )[2],
      Sub_1_Mean_L_HDI  = HDIofMCMC( Sample_Mean[Sample > 5000] )[1],
      Sub_2_Mean_H_HDI  = HDIofMCMC( Sample_Mean[Sample > 5000] )[2],
      Sub_2_Mean_L_HDI  = HDIofMCMC( Sample_Mean[Sample > 5000] )[1]
    ) %>%
    select( Sample_Mean_H_HDI, Sample_Mean_L_HDI, Sub_1_Mean_H_HDI, Sub_1_Mean_L_HDI ,Sub_2_Mean_H_HDI,  Sub_2_Mean_L_HDI  ) %>%
    distinct( )
  
  Example_2_Results = Example_2 %>%
    mutate(
      Sample_Mean_H_HDI = HDIofMCMC( Sample_Mean[Sample > 5000] )[2],
      Sample_Mean_L_HDI = HDIofMCMC( Sample_Mean[Sample > 5000] )[1],
      Sub_1_Mean_H_HDI  = HDIofMCMC( Sample_Mean[Sample > 5000] )[2],
      Sub_1_Mean_L_HDI  = HDIofMCMC( Sample_Mean[Sample > 5000] )[1],
      Sub_2_Mean_H_HDI  = HDIofMCMC( Sample_Mean[Sample > 5000] )[2],
      Sub_2_Mean_L_HDI  = HDIofMCMC( Sample_Mean[Sample > 5000] )[1]
    ) %>%
    select( Sample_Mean_H_HDI, Sample_Mean_L_HDI, Sub_1_Mean_H_HDI, Sub_1_Mean_L_HDI ,Sub_2_Mean_H_HDI,  Sub_2_Mean_L_HDI  ) %>%
    distinct( )
  
  Example_3_Results = Example_3 %>%
    mutate(
      Sample_Mean_H_HDI = HDIofMCMC( Sample_Mean[Sample > 5000] )[2],
      Sample_Mean_L_HDI = HDIofMCMC( Sample_Mean[Sample > 5000] )[1],
      Sub_1_Mean_H_HDI  = HDIofMCMC( Sample_Mean[Sample > 5000] )[2],
      Sub_1_Mean_L_HDI  = HDIofMCMC( Sample_Mean[Sample > 5000] )[1],
      Sub_2_Mean_H_HDI  = HDIofMCMC( Sample_Mean[Sample > 5000] )[2],
      Sub_2_Mean_L_HDI  = HDIofMCMC( Sample_Mean[Sample > 5000] )[1]
    ) %>%
    select( Sample_Mean_H_HDI, Sample_Mean_L_HDI, Sub_1_Mean_H_HDI, Sub_1_Mean_L_HDI ,Sub_2_Mean_H_HDI,  Sub_2_Mean_L_HDI  ) %>%
    distinct( )
  
  Example_4_Results = Example_4 %>%
    mutate(
      Sample_Mean_H_HDI = HDIofMCMC( Sample_Mean[Sample > 5000] )[2],
      Sample_Mean_L_HDI = HDIofMCMC( Sample_Mean[Sample > 5000] )[1],
      Sub_1_Mean_H_HDI  = HDIofMCMC( Sample_Mean[Sample > 5000] )[2],
      Sub_1_Mean_L_HDI  = HDIofMCMC( Sample_Mean[Sample > 5000] )[1],
      Sub_2_Mean_H_HDI  = HDIofMCMC( Sample_Mean[Sample > 5000] )[2],
      Sub_2_Mean_L_HDI  = HDIofMCMC( Sample_Mean[Sample > 5000] )[1]
    ) %>%
    select( Sample_Mean_H_HDI, Sample_Mean_L_HDI, Sub_1_Mean_H_HDI, Sub_1_Mean_L_HDI ,Sub_2_Mean_H_HDI,  Sub_2_Mean_L_HDI  ) %>%
    distinct( )
  
  Example_5_Results = Example_5 %>%
    mutate(
      Sample_Mean_H_HDI = HDIofMCMC( Sample_Mean[Sample > 5000] )[2],
      Sample_Mean_L_HDI = HDIofMCMC( Sample_Mean[Sample > 5000] )[1],
      Sub_1_Mean_H_HDI  = HDIofMCMC( Sample_Mean[Sample > 5000] )[2],
      Sub_1_Mean_L_HDI  = HDIofMCMC( Sample_Mean[Sample > 5000] )[1],
      Sub_2_Mean_H_HDI  = HDIofMCMC( Sample_Mean[Sample > 5000] )[2],
      Sub_2_Mean_L_HDI  = HDIofMCMC( Sample_Mean[Sample > 5000] )[1]
    ) %>%
    select( Sample_Mean_H_HDI, Sample_Mean_L_HDI, Sub_1_Mean_H_HDI, Sub_1_Mean_L_HDI ,Sub_2_Mean_H_HDI,  Sub_2_Mean_L_HDI  ) %>%
    distinct( )
  
  Example_6_Results = Example_6 %>%
    mutate(
      Sample_Mean_H_HDI = HDIofMCMC( Sample_Mean[Sample > 5000] )[2],
      Sample_Mean_L_HDI = HDIofMCMC( Sample_Mean[Sample > 5000] )[1],
      Sub_1_Mean_H_HDI  = HDIofMCMC( Sample_Mean[Sample > 5000] )[2],
      Sub_1_Mean_L_HDI  = HDIofMCMC( Sample_Mean[Sample > 5000] )[1],
      Sub_2_Mean_H_HDI  = HDIofMCMC( Sample_Mean[Sample > 5000] )[2],
      Sub_2_Mean_L_HDI  = HDIofMCMC( Sample_Mean[Sample > 5000] )[1]
    ) %>%
    select( Sample_Mean_H_HDI, Sample_Mean_L_HDI, Sub_1_Mean_H_HDI, Sub_1_Mean_L_HDI ,Sub_2_Mean_H_HDI,  Sub_2_Mean_L_HDI  ) %>%
    distinct( )
  
  
}
print("Example 1 95 %HDI")
print(Example_1_Results)
print("Example 1 95 %HDI")
print(Example_2_Results)
print("Example 1 95 %HDI")
print(Example_3_Results)
print("Example 1 95 %HDI")
print(Example_4_Results)
print("Example 1 95 %HDI")
print(Example_5_Results)
print("Example 1 95 %HDI")
print(Example_6_Results)
