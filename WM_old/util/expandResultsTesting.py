

    
with open('/home/pjrice/gp/ACTR-WM/data/parEstResults/Powell/bounded/chunkAcc2_noBadSubjs_ansEnabled_parEstExp.json', 'r') as fp:
    test = json.load(fp)

remList = ['allRT_rmse', 'allAcc_rmse', 'bbAcc_rmse','bbRT_rmse','tarRT_rmse','lurRT_rmse','nlrRT_rmse','tarAcc_rmse','lurAcc_rmse','nlrAcc_rmse','model_tarRT_mean','model_lurRT_mean','model_nlrRT_mean','subj_tarRT_mean','subj_lurRT_mean','subj_nlrRT_mean','model_tarAcc_mean','model_lurAcc_mean','model_nlrAcc_mean','subj_tarAcc_mean','subj_lurAcc_mean','subj_nlrAcc_mean','rtDiff_mean']

[test.pop(key) for key in remList]

baseDict = test

del(test)

#test = expandEstResults(baseDict)


[test, all_model_tarRT_means, all_model_lurRT_means, all_model_nlrRT_means] = expandEstResults_bootstrap(baseDict)

themeans = [np.mean(x) for x in all_model_tarRT_means]