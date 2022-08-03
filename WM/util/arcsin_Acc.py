



def subjMeasures_modelPreds_arcsinAccScatter (subjMeasures,modelPredictions,modelKey):
    
    
    subjMeas = 'subjMeanAcc'
    modelMeas = 'meanAcc'
    xAxisTitle = 'subj mean accuracy, arcsine transform'
    yAxisTitle = 'model mean acc (over 100 runs), arcsine transform'
    plotTitle = 'Subj vs model mean acc, '+modelKey
    
    
    subjAcc = np.arcsin(np.sqrt(subjMeasures[subjMeas]))
    modelAcc = np.arcsin(np.sqrt(modelPredictions[modelKey][modelMeas]))
    
    plt.scatter(subjAcc,modelAcc)
    m,b = np.polyfit(subjAcc,modelAcc,1)
    plt.plot(subjAcc, m*np.array(subjAcc)+b)
    plotAnno = 'r = '+str(round(scipy.stats.pearsonr(subjAcc,modelAcc)[0],2))
    plt.text(np.min(subjAcc), np.max(modelAcc),plotAnno)
    plt.xlabel(xAxisTitle)
    plt.ylabel(yAxisTitle)
    plt.title(plotTitle)
    plt.show()
    



#five par
with open('/home/pjrice/gp/ACTR-WM/data/parEstResults/Powell/bounded/fivePar/group_and_perPar_corrData.json', 'r') as fp: 
    corrResults5p = json.load(fp)

subjMeasures_modelPreds_arcsinAccScatter(corrResults5p['subj'],corrResults5p['models'],'bll')
subjMeasures_modelPreds_arcsinAccScatter(corrResults5p['subj'],corrResults5p['models'],'bll,ga')
subjMeasures_modelPreds_arcsinAccScatter(corrResults5p['subj'],corrResults5p['models'],'bll,ga,ia')
subjMeasures_modelPreds_arcsinAccScatter(corrResults5p['subj'],corrResults5p['models'],'bll,ga,ia,lf')
subjMeasures_modelPreds_arcsinAccScatter(corrResults5p['subj'],corrResults5p['models'],'bll,ga,ia,lf,css')

#four par
with open('/home/pjrice/gp/ACTR-WM/data/parEstResults/Powell/bounded/fourPar/group_and_perPar_corrData.json', 'r') as fp: 
    corrResults = json.load(fp)

subjMeasures_modelPreds_arcsinAccScatter(corrResults['subj'],corrResults['models'],'bll')
subjMeasures_modelPreds_arcsinAccScatter(corrResults['subj'],corrResults['models'],'bll,ga')
subjMeasures_modelPreds_arcsinAccScatter(corrResults['subj'],corrResults['models'],'bll,ga,ia')
subjMeasures_modelPreds_arcsinAccScatter(corrResults['subj'],corrResults['models'],'bll,ga,ia,lf')

#leave one out
with open('/home/pjrice/gp/ACTR-WM/data/parEstResults/Powell/bounded/fivePar/looCorrs.json', 'r') as fp: 
    looCorrs = json.load(fp)
    
modelKeys = list(looCorrs['models'].keys())
for modelKey in modelKeys:
    
    subjMeasures_modelPreds_arcsinAccScatter(looCorrs['subj'],looCorrs['models'],modelKey)
    
    
#remove outlier
import copy

# five par
corrResults5p_no = copy.deepcopy(corrResults5p)

removeIdx = corrResults5p_no['subj']['subjMeanAcc'].index(0.65)
corrResults5p_no['subj']['subjMeanAcc'].pop(removeIdx)
modelKeys = list(corrResults5p_no['models'].keys())
for modelKey in modelKeys:
    corrResults5p_no['models'][modelKey]['meanAcc'].pop(removeIdx)
    subjMeasures_modelPreds_scatter(corrResults5p['subj'],corrResults5p['models'],modelKey,'acc')
    subjMeasures_modelPreds_scatter(corrResults5p_no['subj'],corrResults5p_no['models'],modelKey,'acc')
    #subjMeasures_modelPreds_arcsinAccScatter(corrResults5p_no['subj'],corrResults5p_no['models'],modelKey)
    
    
# four par
corrResults_no = copy.deepcopy(corrResults)
removeIdx = corrResults_no['subj']['subjMeanAcc'].index(0.65)
corrResults_no['subj']['subjMeanAcc'].pop(removeIdx)
modelKeys = list(corrResults_no['models'].keys())
for modelKey in modelKeys:
    corrResults_no['models'][modelKey]['meanAcc'].pop(removeIdx)
    subjMeasures_modelPreds_scatter(corrResults['subj'],corrResults['models'],modelKey,'acc')
    subjMeasures_modelPreds_scatter(corrResults_no['subj'],corrResults_no['models'],modelKey,'acc')
    #subjMeasures_modelPreds_arcsinAccScatter(corrResults_no['subj'],corrResults_no['models'],modelKey)
    
# leave one out
looCorrs_no = copy.deepcopy(looCorrs)
removeIdx = looCorrs_no['subj']['subjMeanAcc'].index(0.65)
looCorrs_no['subj']['subjMeanAcc'].pop(removeIdx)
modelKeys = list(looCorrs_no['models'].keys())
for modelKey in modelKeys:
    looCorrs_no['models'][modelKey]['meanAcc'].pop(removeIdx)
    subjMeasures_modelPreds_scatter(looCorrs['subj'],looCorrs['models'],modelKey,'acc')
    subjMeasures_modelPreds_scatter(looCorrs_no['subj'],looCorrs_no['models'],modelKey,'acc')
    #subjMeasures_modelPreds_arcsinAccScatter(looCorrs_no['subj'],looCorrs_no['models'],modelKey)









    
    
