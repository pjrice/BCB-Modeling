




import time

tic = time.time()
abc_hierarchical_model(0.2,numChainIter=100)
toc = time.time()

toc - tic


# time to run abc_hierarchical_model with 100 chain iterations:
#   original: 147 seconds
#   no (print) output in ACT-R terminal: 149 seconds :(
#   changing actr/modelFunc import calls to prep for chain parallelization: 147 sec (this is without closing the ACT-R windows)