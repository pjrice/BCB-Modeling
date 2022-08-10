#save/load json

with open('/home/pjrice/gp/ACTR-WM/data/parEstResults/Powell/bounded/ttBB_lf_bll_negBounds_parEstExp.json', 'w') as fp:
    json.dump(test,fp)
    
    
with open('/home/pjrice/gp/ACTR-WM/data/parEstResults/Powell/bounded/ttBB_lf_bll_negBounds_parEstExp.json', 'r') as fp:
    test = json.load(fp)


#####################################################################################


with open('/home/pjrice/gp/ACTR-WM/data/parEstResults/Powell/bounded/ttBB_positiveCSS_parEstExp.json', 'w') as fp:
    json.dump(test,fp)
    
    
with open('/home/pjrice/gp/ACTR-WM/data/parEstResults/Powell/bounded/ttBB_positiveCSS_parEstExp.json', 'r') as fp:
    test = json.load(fp)
    
    
#####################################################################################

with open('/home/pjrice/gp/ACTR-WM/data/parEstResults/Powell/bounded/chunkAcc_parEstExp.json', 'r') as fp:
    test = json.load(fp)
    
with open('/home/pjrice/gp/ACTR-WM/data/parEstResults/Powell/bounded/chunkAcc_positiveCSS_parEstExp.json', 'r') as fp:
    test = json.load(fp)
    
    
    
with open('/home/pjrice/gp/ACTR-WM/data/parEstResults/Powell/bounded/chunkAcc2_noBadSubjs_ansEnabled_parEstExp.json', 'r') as fp:
    test = json.load(fp)
    
    
with open('/home/pjrice/gp/ACTR-WM/data/parEstResults/Powell/bounded/chunkAcc2_noBadSubjs_ansEnabled_longRetrievalInterrupt2_parEstExp.json', 'r') as fp:
    test = json.load(fp)