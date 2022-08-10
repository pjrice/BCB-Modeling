



#make the thing you want the sorted indices of into a np array
tester = np.array(test['tarAcc_rmse'])

#np.argsort returns the sort index
sort_idx = np.argsort(tester)