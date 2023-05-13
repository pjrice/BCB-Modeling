




import time

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


# time to run abc_hierarchical_model with 100 chain iterations:
#   original: 147 seconds
#   no (print) output in ACT-R terminal: 149 seconds :(
#   changing actr/modelFunc import calls to prep for chain parallelization: 147 sec (this is without closing the ACT-R windows)