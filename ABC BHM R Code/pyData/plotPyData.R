library(ggplot2)
library(ggpubr)


Obs = read.csv('/home/ausmanpa/gp/BCB-Modeling/ABC BHM R Code/pyData/partData.csv')
colnames(Obs) = c("X","Sub","dvSteady",'DV')

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
Tuning_05 = read.csv('/home/ausmanpa/gp/BCB-Modeling/ABC BHM R Code/pyData/tuning05.csv')
colnames(Tuning_05) = c("X","Sample","Sample_Mean","Individual_1","Individual_2","Chain")
Tuning_10 = read.csv('/home/ausmanpa/gp/BCB-Modeling/ABC BHM R Code/pyData/tuning10.csv')
colnames(Tuning_10) = c("X","Sample","Sample_Mean","Individual_1","Individual_2","Chain")
Tuning_15 = read.csv('/home/ausmanpa/gp/BCB-Modeling/ABC BHM R Code/pyData/tuning15.csv')
colnames(Tuning_15) = c("X","Sample","Sample_Mean","Individual_1","Individual_2","Chain")
Tuning_20 = read.csv('/home/ausmanpa/gp/BCB-Modeling/ABC BHM R Code/pyData/tuning20.csv')
colnames(Tuning_20) = c("X","Sample","Sample_Mean","Individual_1","Individual_2","Chain")





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
