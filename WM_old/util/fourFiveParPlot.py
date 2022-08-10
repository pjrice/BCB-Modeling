
import json

###################################################################################################################
#estimation results

with open('/home/pjrice/gp/ACTR-WM/data/parEstResults/Powell/bounded/fivePar/fivePar_estCSS.json', 'r') as fp: 
    fiveParEst = json.load(fp)
    
with open('/home/pjrice/gp/ACTR-WM/data/parEstResults/Powell/bounded/fourPar/fourPar_staticCSS.json', 'r') as fp: 
    fourParEst = json.load(fp)
    
createPlots(fiveParEst,'fiveParEst')
createPlots(fourParEst,'fourParEst')

###################################################################################################################
# five par incremental, group level

with open('/home/pjrice/gp/ACTR-WM/data/parEstResults/Powell/bounded/fivePar/group_and_perPar_corrData.json', 'r') as fp: 
    corrResults5p = json.load(fp)
    
print('\nFive par est, group level:')
modelKeys = list(corrResults5p['models'].keys())
for modelKey in modelKeys:
    
    subjMeasures_modelPreds_scatter(corrResults5p['subj'],corrResults5p['models'],modelKey,'acc')
    
    print(modelKey+' accuracy correlation: ' + 
      str(scipy.stats.pearsonr(corrResults5p['subj']['subjMeanAcc'],corrResults5p['models'][modelKey]['meanAcc'])[0]) + 
      '; p-value: ' + 
      str(scipy.stats.pearsonr(corrResults5p['subj']['subjMeanAcc'],corrResults5p['models'][modelKey]['meanAcc'])[1]))
    
print('\nFive par est, group level:')
modelKeys = list(corrResults5p['models'].keys())
for modelKey in modelKeys:
    
    subjMeasures_modelPreds_scatter(corrResults5p['subj'],corrResults5p['models'],modelKey,'rt')
    
    print(modelKey+' RT correlation: ' + 
      str(scipy.stats.pearsonr(corrResults5p['subj']['subjMeanRTs'],corrResults5p['models'][modelKey]['meanRT'])[0]) + 
      '; p-value: ' + 
      str(scipy.stats.pearsonr(corrResults5p['subj']['subjMeanRTs'],corrResults5p['models'][modelKey]['meanRT'])[1]))

###################################################################################################################
# five par incremental, group level

with open('/home/pjrice/gp/ACTR-WM/data/parEstResults/Powell/bounded/fivePar/modelPredictions.json', 'r') as fp: 
    modelPredictions = json.load(fp)
    
with open('/home/pjrice/gp/ACTR-WM/data/parEstResults/Powell/bounded/fivePar/subjMeasures.json', 'r') as fp: 
    subjMeasures = json.load(fp)

#accuracy
print('\nFive par est, group level:')
print('bll accuracy correlation: ' + 
      str(scipy.stats.pearsonr(subjMeasures['subjMeanAcc'],modelPredictions['bll']['meanAcc'])[0]) + 
      '; p-value: ' + 
      str(scipy.stats.pearsonr(subjMeasures['subjMeanAcc'],modelPredictions['bll']['meanAcc'])[1]))

print('bll,ga accuracy correlation: ' + 
      str(scipy.stats.pearsonr(subjMeasures['subjMeanAcc'],modelPredictions['bll,ga']['meanAcc'])[0]) + 
      '; p-value: ' + 
      str(scipy.stats.pearsonr(subjMeasures['subjMeanAcc'],modelPredictions['bll,ga']['meanAcc'])[1]))

print('bll,ga,ia accuracy correlation: ' + 
      str(scipy.stats.pearsonr(subjMeasures['subjMeanAcc'],modelPredictions['bll,ga,ia']['meanAcc'])[0]) + 
      '; p-value: ' + 
      str(scipy.stats.pearsonr(subjMeasures['subjMeanAcc'],modelPredictions['bll,ga,ia']['meanAcc'])[1]))

print('bll,ga,ia,lf accuracy correlation: ' + 
      str(scipy.stats.pearsonr(subjMeasures['subjMeanAcc'],modelPredictions['bll,ga,ia,lf']['meanAcc'])[0]) + 
      '; p-value: ' + 
      str(scipy.stats.pearsonr(subjMeasures['subjMeanAcc'],modelPredictions['bll,ga,ia,lf']['meanAcc'])[1]))

print('bll,ga,ia,lf,css accuracy correlation: ' + 
      str(scipy.stats.pearsonr(subjMeasures['subjMeanAcc'],modelPredictions['bll,ga,ia,lf,css']['meanAcc'])[0]) + 
      '; p-value: ' + 
      str(scipy.stats.pearsonr(subjMeasures['subjMeanAcc'],modelPredictions['bll,ga,ia,lf,css']['meanAcc'])[1]))

subjMeasures_modelPreds_scatter(subjMeasures,modelPredictions,'bll','acc')
subjMeasures_modelPreds_scatter(subjMeasures,modelPredictions,'bll,ga','acc')
subjMeasures_modelPreds_scatter(subjMeasures,modelPredictions,'bll,ga,ia','acc')
subjMeasures_modelPreds_scatter(subjMeasures,modelPredictions,'bll,ga,ia,lf','acc')
subjMeasures_modelPreds_scatter(subjMeasures,modelPredictions,'bll,ga,ia,lf,css','acc')


#RT
print('\n')
print('bll RT correlation: ' + 
      str(scipy.stats.pearsonr(subjMeasures['subjMeanRTs'],modelPredictions['bll']['meanRT'])[0]) + 
      '; p-value: ' + 
      str(scipy.stats.pearsonr(subjMeasures['subjMeanRTs'],modelPredictions['bll']['meanRT'])[1]))

print('bll,ga RT correlation: ' + 
      str(scipy.stats.pearsonr(subjMeasures['subjMeanRTs'],modelPredictions['bll,ga']['meanRT'])[0]) + 
      '; p-value: ' + 
      str(scipy.stats.pearsonr(subjMeasures['subjMeanRTs'],modelPredictions['bll,ga']['meanRT'])[1]))

print('bll,ga,ia RT correlation: ' + 
      str(scipy.stats.pearsonr(subjMeasures['subjMeanRTs'],modelPredictions['bll,ga,ia']['meanRT'])[0]) + 
      '; p-value: ' + 
      str(scipy.stats.pearsonr(subjMeasures['subjMeanRTs'],modelPredictions['bll,ga,ia']['meanRT'])[1]))

print('bll,ga,ia,lf RT correlation: ' + 
      str(scipy.stats.pearsonr(subjMeasures['subjMeanRTs'],modelPredictions['bll,ga,ia,lf']['meanRT'])[0]) + 
      '; p-value: ' + 
      str(scipy.stats.pearsonr(subjMeasures['subjMeanRTs'],modelPredictions['bll,ga,ia,lf']['meanRT'])[1]))

print('bll,ga,ia,lf,css RT correlation: ' + 
      str(scipy.stats.pearsonr(subjMeasures['subjMeanRTs'],modelPredictions['bll,ga,ia,lf,css']['meanRT'])[0]) + 
      '; p-value: ' + 
      str(scipy.stats.pearsonr(subjMeasures['subjMeanRTs'],modelPredictions['bll,ga,ia,lf,css']['meanRT'])[1]))


subjMeasures_modelPreds_scatter(subjMeasures,modelPredictions,'bll','rt')
subjMeasures_modelPreds_scatter(subjMeasures,modelPredictions,'bll,ga','rt')
subjMeasures_modelPreds_scatter(subjMeasures,modelPredictions,'bll,ga,ia','rt')
subjMeasures_modelPreds_scatter(subjMeasures,modelPredictions,'bll,ga,ia,lf','rt')
subjMeasures_modelPreds_scatter(subjMeasures,modelPredictions,'bll,ga,ia,lf,css','rt')

###################################################################################################################
# four par incremental, group level

with open('/home/pjrice/gp/ACTR-WM/data/parEstResults/Powell/bounded/fourPar/group_and_perPar_corrData.json', 'r') as fp: 
    corrResults = json.load(fp)
    
print('\nFour par est, group level:')
modelKeys = list(corrResults['models'].keys())
for modelKey in modelKeys:
    print(modelKey+' accuracy correlation: ' + 
      str(scipy.stats.pearsonr(corrResults['subj']['subjMeanAcc'],corrResults['models'][modelKey]['meanAcc'])[0]) + 
      '; p-value: ' + 
      str(scipy.stats.pearsonr(corrResults['subj']['subjMeanAcc'],corrResults['models'][modelKey]['meanAcc'])[1]))
    

subjMeasures_modelPreds_scatter(corrResults['subj'],corrResults['models'],'bll','acc')
subjMeasures_modelPreds_scatter(corrResults['subj'],corrResults['models'],'bll,ga','acc')
subjMeasures_modelPreds_scatter(corrResults['subj'],corrResults['models'],'bll,ga,ia','acc')
subjMeasures_modelPreds_scatter(corrResults['subj'],corrResults['models'],'bll,ga,ia,lf','acc')

print('\nFour par est, group level:')
modelKeys = list(corrResults['models'].keys())
for modelKey in modelKeys:
    print(modelKey+' RT correlation: ' + 
      str(scipy.stats.pearsonr(corrResults['subj']['subjMeanRTs'],corrResults['models'][modelKey]['meanRT'])[0]) + 
      '; p-value: ' + 
      str(scipy.stats.pearsonr(corrResults['subj']['subjMeanRTs'],corrResults['models'][modelKey]['meanRT'])[1]))

subjMeasures_modelPreds_scatter(corrResults['subj'],corrResults['models'],'bll','rt')
subjMeasures_modelPreds_scatter(corrResults['subj'],corrResults['models'],'bll,ga','rt')
subjMeasures_modelPreds_scatter(corrResults['subj'],corrResults['models'],'bll,ga,ia','rt')
subjMeasures_modelPreds_scatter(corrResults['subj'],corrResults['models'],'bll,ga,ia,lf','rt')

###################################################################################################################
# leave one out, group level

with open('/home/pjrice/gp/ACTR-WM/data/parEstResults/Powell/bounded/fivePar/looCorrs.json', 'r') as fp: 
    looCorrs = json.load(fp)
    
print('\nLeave one out, group level:')
modelKeys = list(looCorrs['models'].keys())
for modelKey in modelKeys:
    
    subjMeasures_modelPreds_scatter(looCorrs['subj'],looCorrs['models'],modelKey,'acc')
    
    print(modelKey+' accuracy correlation: ' + 
      str(scipy.stats.pearsonr(looCorrs['subj']['subjMeanAcc'],looCorrs['models'][modelKey]['meanAcc'])[0]) + 
      '; p-value: ' + 
      str(scipy.stats.pearsonr(looCorrs['subj']['subjMeanAcc'],looCorrs['models'][modelKey]['meanAcc'])[1]))
    
print('\nLeave one out, group level:')
modelKeys = list(looCorrs['models'].keys())
for modelKey in modelKeys:
    
    subjMeasures_modelPreds_scatter(looCorrs['subj'],looCorrs['models'],modelKey,'rt')
    
    print(modelKey+' RT correlation: ' + 
      str(scipy.stats.pearsonr(looCorrs['subj']['subjMeanRTs'],looCorrs['models'][modelKey]['meanRT'])[0]) + 
      '; p-value: ' + 
      str(scipy.stats.pearsonr(looCorrs['subj']['subjMeanRTs'],looCorrs['models'][modelKey]['meanRT'])[1]))
    

###################################################################################################################
# decremental loo

modelKeys = list(dLOO_results['models'].keys())
for modelKey in modelKeys:
    subjMeasures_modelPreds_scatter(dLOO_results['subj'],dLOO_results['models'],modelKey,'acc')

###################################################################################################################
# five par incremental, per part

with open('/home/pjrice/gp/ACTR-WM/data/parEstResults/Powell/bounded/fivePar/modelSubjCorrs.json', 'r') as fp: 
    modelSubjCorrs = json.load(fp)

perPart_modelSubjCorrs(modelSubjCorrs,'bll')
perPart_modelSubjCorrs(modelSubjCorrs,'bll,ga')
perPart_modelSubjCorrs(modelSubjCorrs,'bll,ga,ia')
perPart_modelSubjCorrs(modelSubjCorrs,'bll,ga,ia,lf')
perPart_modelSubjCorrs(modelSubjCorrs,'bll,ga,ia,lf,css')

###################################################################################################################
# four par incremental, per part

perPart_modelSubjCorrs(corrResults,'bll')
perPart_modelSubjCorrs(corrResults,'bll,ga')
perPart_modelSubjCorrs(corrResults,'bll,ga,ia')
perPart_modelSubjCorrs(corrResults,'bll,ga,ia,lf')

###################################################################################################################
# leave one out, per part

modelKeys = list(looCorrs['models'].keys())
for modelKey in modelKeys:
    perPart_modelSubjCorrs(looCorrs,modelKey)