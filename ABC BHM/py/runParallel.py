

import multiprocessing as mp
import ABC_BHM_ACTR_parallel as abc

def abc_hierarchical_model_parallel(numChains):
    
    chainList = list(range(1,numChains+1))
    
    chainStrings = ['Chain'+str(x) for x in chainList]
    
    results = []
    
    pool = mp.Pool(None)
    #r = pool.map_async(abc.markov_chain, chainStrings, callback=results.append)
    r = pool.map(abc.markov_chain, chainStrings)
    r.wait()
    print(results)
    
    



# this will actually open three terminals, but a number of failstates have been observed, and no successes:
# 1. at least one terminal errors while loading ACT-R. At least two errors observed; 1. file exists: ../ACT-R/patches/force-local.wx64fsl. 2. some ambiguous error ("Error 2") during a force-local call(?)
# 2. all terminals successfully open, but model isn't loaded in two, and in third, model is loaded, but errors indicate parameter values were set while model was not loaded
abc_hierarchical_model_parallel(3)