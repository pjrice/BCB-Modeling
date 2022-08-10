
import json
import scipy.stats
import numpy as np
import matplotlib.pyplot as plt


with open('/home/pjrice/gp/ACTR-WM/data/varExp/aggregate/modelMSEs.json', 'r') as fp: modelMSEs = json.load(fp)    
with open('/home/pjrice/gp/ACTR-WM/data/varExp/aggregate/subjMeasures.json', 'r') as fp: subjMeasures = json.load(fp)    
with open('/home/pjrice/gp/ACTR-WM/data/varExp/aggregate/modelPredictions.json', 'r') as fp: modelPredictions = json.load(fp)    
with open('/home/pjrice/gp/ACTR-WM/data/varExp/perPart/modelMSEs_perPart.json', 'r') as fp: modelMSEs_perPart = json.load(fp)


def subjMeasures_modelPreds_scatter (subjMeasures,modelPredictions,modelKey,measure):
    
    if measure=='acc':
        subjMeas = 'subjMeanAcc'
        modelMeas = 'meanAcc'
        xAxisTitle = 'subj mean accuracy'
        yAxisTitle = 'model mean acc (over 100 runs)'
        plotTitle = 'Subj vs model mean acc, '+modelKey
    elif measure=='rt':
        subjMeas = 'subjMeanRTs'
        modelMeas = 'meanRT'
        xAxisTitle = 'subj mean RT'
        yAxisTitle = 'model mean RT (over 100 runs)'
        plotTitle = 'Subj vs model mean RT '+modelKey
    else:
        print('"measure" arg must be either "acc" or "rt"')
    
    plt.scatter(subjMeasures[subjMeas],modelPredictions[modelKey][modelMeas])
    m,b = np.polyfit(subjMeasures[subjMeas],modelPredictions[modelKey][modelMeas],1)
    plt.plot(subjMeasures[subjMeas], m*np.array(subjMeasures[subjMeas])+b)
    plotAnno = 'r = '+str(round(scipy.stats.pearsonr(subjMeasures[subjMeas],modelPredictions[modelKey][modelMeas])[0],2))
    plt.text(np.min(subjMeasures[subjMeas]), np.max(modelPredictions[modelKey][modelMeas]),plotAnno)
    plt.xlabel(xAxisTitle)
    plt.ylabel(yAxisTitle)
    plt.title(plotTitle)
    plt.show()

def perPart_modelSubjCorrs (modelSubjCorrs,modelKey):
    
    
    if 'cwAcc_corr' in modelSubjCorrs['models'][modelKey].keys():
        fig, axarr = plt.subplots(3,2, constrained_layout=True, sharex='col', sharey='col')
    else:
        fig, axarr = plt.subplots(2,2, constrained_layout=True, sharex='col', sharey='col')
    
    axarr[0,0].hist(modelSubjCorrs['models'][modelKey]['RT_corr'])
    axarr[0,0].set_ylabel('RTs')
    
    axarr[0,1].hist(modelSubjCorrs['models'][modelKey]['RT_pval'],bins=20)
    axarr[0,1].axvline(0.05, color='k', linestyle='dashed',linewidth=1)
    
    axarr[1,0].hist(modelSubjCorrs['models'][modelKey]['Acc_corr'])
    axarr[1,0].set_ylabel('Accuracies')
    
    
    axarr[1,1].hist(modelSubjCorrs['models'][modelKey]['Acc_pval'],bins=20)
    axarr[1,1].axvline(0.05, color='k', linestyle='dashed',linewidth=1)
        
    if 'cwAcc_corr' in modelSubjCorrs['models'][modelKey].keys():
        axarr[2,0].hist(modelSubjCorrs['models'][modelKey]['cwAcc_corr'])
        axarr[2,0].set_xlabel('Correlation between \n subject responses and \nmodel predictions')
        axarr[2,0].set_ylabel('Cond Accs')
        
        axarr[2,1].hist(modelSubjCorrs['models'][modelKey]['cwAcc_pval'],bins=20)
        axarr[2,1].axvline(0.05, color='k', linestyle='dashed',linewidth=1)
        axarr[2,1].set_xlabel('p-value of pearson r \n between subject responses and \n model predictions')
    else:
        axarr[1,0].set_xlabel('Correlation between \n subject responses and \nmodel predictions')
        axarr[1,1].set_xlabel('p-value of pearson r \n between subject responses and \n model predictions')
        

    fig.suptitle('Pearson r between subj and model responses \n with corresponding p-values for model: '+modelKey)

    plt.show()
    
    RT_pval_ratio = sum(i<0.05 for i in modelSubjCorrs['models'][modelKey]['RT_pval'])/len(modelSubjCorrs['models'][modelKey]['RT_pval'])
    Acc_pval_ratio = sum(i<0.05 for i in modelSubjCorrs['models'][modelKey]['Acc_pval'])/len(modelSubjCorrs['models'][modelKey]['Acc_pval'])
    
    print('\nPercent of '+modelKey+' model RT pearson r values with p value < 0.05: '+str(round(RT_pval_ratio*100,2))+'%')
    print('Percent of '+modelKey+' model accuracy pearson r values with p value < 0.05: '+str(round(Acc_pval_ratio*100,2))+'%')
    
    if 'cwAcc_corr' in modelSubjCorrs['models'][modelKey].keys():
        cwAcc_pval_ratio = sum(i<0.05 for i in modelSubjCorrs['models'][modelKey]['cwAcc_pval'])/len(modelSubjCorrs['models'][modelKey]['cwAcc_pval'])
        print('Percent of '+modelKey+' model condition-wise accuracy pearson r values with p value < 0.05: '+str(round(cwAcc_pval_ratio*100,2))+'%')


##########################################################################################################################################
#aggregate


#correlations between subj measures and model predictions
#accuracy
print('\n')
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

#weird thing is, differences between subjMeasures and model predictions aren't that different when including css or not
print(np.mean([i-j for i,j in zip(subjMeasures['subjMeanAcc'],modelPredictions['bll,ga,ia,lf']['meanAcc'])]))
print(np.mean([i-j for i,j in zip(subjMeasures['subjMeanAcc'],modelPredictions['bll,ga,ia,lf,css']['meanAcc'])]))    

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


#four par est

subjMeasures_modelPreds_scatter(corrResults['subj'],corrResults['models'],'bll','rt')
subjMeasures_modelPreds_scatter(corrResults['subj'],corrResults['models'],'bll,ga','rt')
subjMeasures_modelPreds_scatter(corrResults['subj'],corrResults['models'],'bll,ga,ia','rt')
subjMeasures_modelPreds_scatter(corrResults['subj'],corrResults['models'],'bll,ga,ia,lf','rt')

subjMeasures_modelPreds_scatter(corrResults['subj'],corrResults['models'],'bll','acc')
subjMeasures_modelPreds_scatter(corrResults['subj'],corrResults['models'],'bll,ga','acc')
subjMeasures_modelPreds_scatter(corrResults['subj'],corrResults['models'],'bll,ga,ia','acc')
subjMeasures_modelPreds_scatter(corrResults['subj'],corrResults['models'],'bll,ga,ia,lf','acc')



#########################################################################################################################################
#per subject

perPart_modelSubjCorrs(modelSubjCorrs,'bll')
perPart_modelSubjCorrs(modelSubjCorrs,'bll,ga')
perPart_modelSubjCorrs(modelSubjCorrs,'bll,ga,ia')
perPart_modelSubjCorrs(modelSubjCorrs,'bll,ga,ia,lf')
perPart_modelSubjCorrs(modelSubjCorrs,'bll,ga,ia,lf,css')





