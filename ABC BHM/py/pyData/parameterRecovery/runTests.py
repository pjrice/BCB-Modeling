import time

# test 1

tic = time.time()
tuning20 = abc_hierarchical_model(0.2,numChainIter=10000)
tuning20.to_csv('Z:\\gp\\BCB-Modeling\\ABC BHM\\py\\pyData\\parameterRecovery\\rtAndAcc\\tuning20.csv')  
toc = time.time()

toc - tic


tuning05 = abc_hierarchical_model(0.05,numChainIter=10000)
tuning05.to_csv('Z:\\gp\\BCB-Modeling\\ABC BHM\\py\\pyData\\parameterRecovery\\rtAndAcc\\tuning05.csv')  

tuning10 = abc_hierarchical_model(0.10,numChainIter=10000)
tuning10.to_csv('Z:\\gp\\BCB-Modeling\\ABC BHM\\py\\pyData\\parameterRecovery\\rtAndAcc\\tuning10.csv') 

tuning15 = abc_hierarchical_model(0.15,numChainIter=10000)
tuning15.to_csv('Z:\\gp\\BCB-Modeling\\ABC BHM\\py\\pyData\\parameterRecovery\\rtAndAcc\\tuning15.csv') 



# test 2
tuning15 = abc_hierarchical_model(0.15,numChainIter=10000)
tuning15.to_csv('Z:\\gp\\BCB-Modeling\\ABC BHM\\py\\pyData\\parameterRecovery\\rtAndAcc\\test2\\tuning15.csv') 


# test 3
parameters = {'tuning':0.15,
              'indiv_kappa':10,
              'pop_kappa':2}
modelResults = abc_hierarchical_model(parameters,numChainIter=10000)
modelResults.to_csv('Z:\\gp\\BCB-Modeling\\ABC BHM\\py\\pyData\\parameterRecovery\\test3\\RTAcc_ik10_pk2.csv')

parameters = {'tuning':0.15,
              'indiv_kappa':250,
              'pop_kappa':100}
modelResults = abc_hierarchical_model(parameters,numChainIter=10000)
modelResults.to_csv('Z:\\gp\\BCB-Modeling\\ABC BHM\\py\\pyData\\parameterRecovery\\test3\\RTAcc_ik250_pk100.csv')

parameters = {'tuning':0.15,
              'indiv_kappa':10,
              'pop_kappa':2}
modelResults = abc_hierarchical_model_RTonly(parameters,numChainIter=10000)
modelResults.to_csv('Z:\\gp\\BCB-Modeling\\ABC BHM\\py\\pyData\\parameterRecovery\\test3\\RTonly_ik10_pk2.csv')

parameters = {'tuning':0.15,
              'indiv_kappa':250,
              'pop_kappa':100}
modelResults = abc_hierarchical_model_RTonly(parameters,numChainIter=10000)
modelResults.to_csv('Z:\\gp\\BCB-Modeling\\ABC BHM\\py\\pyData\\parameterRecovery\\test3\\RTonly_ik250_pk100.csv')