
import scipy.stats
import numpy as np
import matplotlib.pyplot as plt



def createPlots (results, estName):
    """Produces a number of plots and metrics to evaluate the estimated parameters of
    the ACT-R n-back model."""
    
    #parameter value histograms
    
    #cue-stimulus similarity
    if 'css' in results.keys():
        plt.hist(results['css'], bins=30)
        plt.xlim(-1,0)
        plt.xlabel('css value')
        plt.ylabel('Frequency')
        plt.title('Estimated cue-stimulus similarity values across participants \n Method: '+estName)
        plt.show()
    
     #lf
    plt.hist(results['lf'], bins=30)
    plt.xlabel('lf value')
    plt.ylabel('Frequency')
    plt.title('Estimated lf values across participants \n Method: '+estName)
    plt.show()
    
    
    plt.hist(results['bll'], bins=30)
    plt.xlabel('bll value')
    plt.ylabel('Frequency')
    plt.title('Estimated bll values across participants \n Method: '+estName)
    plt.show()
    
    #goal buffer spreading activation
    plt.hist(results['ga'], bins=30)
    plt.xlim(-2,2)
    plt.xlabel(':ga value')
    plt.ylabel('Frequency')
    plt.title('Estimated goal buffer spr.act. values across participants \n Method: '+estName)
    plt.show()
    
    #imaginal buffer spreading activation
    plt.hist(results['ia'], bins=30)
    plt.xlim(-2,2)
    plt.xlabel(':ia value')
    plt.ylabel('Frequency')
    plt.title('Estimated imaginal buffer spr.act. values across participants \n Method: '+estName)
    plt.show()
    
    #scatter plot - goal buffer spreading activation versus imaginal buffer spreading activation
    plt.scatter(results['ga'], results['ia'])
    plt.xlim(0,2)
    plt.ylim(0,2)
    m,b = np.polyfit(results['ga'], results['ia'],1)
    plt.plot(results['ga'], m*np.array(results['ga'])+b)
    plotAnno = 'r = '+str(round(scipy.stats.pearsonr(results['ga'], results['ia'])[0],2))
    plt.text(0.1,1.75,plotAnno)
    plt.xlabel(':ga value')
    plt.ylabel(':ia value')
    plt.title('Goal spr.act. versus imaginal spr.act. \n Method: '+estName)
    plt.show()
    
    #difference between goal and imaginal buffers spreading activation
    # ga - ia
    #so, the relative influence of the goal buffer over the imaginal buffer
    #if it's positive, cues are receiving boosts over stimuli (from relatively "less negative" (or even positive) influence from goal buffer)
    #if negative, stimuli are receiving boosts over cues (from relatively "less negative" (or even positive) influence from imaginal buffer)
    ga_ia_diff = np.array(results['ga'], dtype=np.float) - np.array(results['ia'], dtype=np.float)
    plt.hist(ga_ia_diff, bins=30)
    plt.xlim(-2,2)
    plt.xlabel('ga - ia')
    plt.ylabel('Frequency')
    plt.title('Estimated relative influence of goal buffer over imaginal buffer \n Method: '+estName)
    plt.show()
    
    #scatter plot - css value versus relative influence of goal over imaginal buffer
    if 'css' in results.keys():
        plt.scatter(results['css'], ga_ia_diff)
        plt.xlim(-1,0)
        plt.ylim(-2,2)
        m,b = np.polyfit(results['css'], ga_ia_diff,1)
        plt.plot(results['css'], m*np.array(results['css'])+b)
        plotAnno = 'r = '+str(round(scipy.stats.pearsonr(results['css'], ga_ia_diff)[0],2))
        plt.text(-0.9,1.75,plotAnno)
        plt.xlabel('css value')
        plt.ylabel('ga - ia')
        plt.title('css values versus rel. influence of goal over imaginal buffer \n Method: '+estName)
        plt.show()
        
    #scatter plot - bll value versus relative influence of goal over imaginal buffer
    plt.scatter(results['bll'], ga_ia_diff)
    plt.xlim(0.2,0.8)
    plt.ylim(-2,2)
    m,b = np.polyfit(results['bll'], ga_ia_diff,1)
    plt.plot(results['bll'], m*np.array(results['bll'])+b)
    plotAnno = 'r = '+str(round(scipy.stats.pearsonr(results['bll'], ga_ia_diff)[0],2))
    plt.text(0.25,1.5,plotAnno)
    plt.xlabel('bll value')
    plt.ylabel('ga - ia')
    plt.title('bll values versus rel. influence of goal over imaginal buffer \n Method: '+estName)
    plt.show()
    
    
    #correlations between model predictions and subj measures
    plt.scatter(results['subj_meanRT'],results['model_meanRT'])
    m,b = np.polyfit(results['subj_meanRT'],results['model_meanRT'],1)
    plt.plot(results['subj_meanRT'], m*np.array(results['subj_meanRT'])+b)
    plotAnno = 'r = '+str(round(scipy.stats.pearsonr(results['subj_meanRT'],results['model_meanRT'])[0],2))
    plt.text(np.min(results['subj_meanRT']), np.max(results['model_meanRT']),plotAnno)
    plt.xlabel("subj mean RT")
    plt.ylabel("model mean RT")
    plt.title('Subject mean RT versus model-predicted mean RT')
    plt.show()
    
    plt.scatter(results['subj_meanAcc'],results['model_meanAcc'])
    m,b = np.polyfit(results['subj_meanAcc'],results['model_meanAcc'],1)
    plt.plot(results['subj_meanAcc'], m*np.array(results['subj_meanAcc'])+b)
    plotAnno = 'r = '+str(round(scipy.stats.pearsonr(results['subj_meanAcc'],results['model_meanAcc'])[0],2))
    plt.text(np.min(results['subj_meanAcc']), np.max(results['model_meanAcc']),plotAnno)
    plt.xlabel("subj mean Acc")
    plt.ylabel("model mean Acc")
    plt.title('Subject mean Acc versus model-predicted mean Acc')
    plt.show()
    
    as_subjAcc = np.arcsin(np.sqrt(results['subj_meanAcc']))
    as_modelAcc = np.arcsin(np.sqrt(results['model_meanAcc']))
    
    plt.scatter(as_subjAcc,as_modelAcc)
    m,b = np.polyfit(as_subjAcc,as_modelAcc,1)
    plt.plot(as_subjAcc, m*np.array(as_subjAcc)+b)
    plotAnno = 'r = '+str(round(scipy.stats.pearsonr(as_subjAcc,as_modelAcc)[0],2))
    plt.text(np.min(as_subjAcc), np.max(as_modelAcc),plotAnno)
    plt.xlabel("subj mean Acc, arcsine transform")
    plt.ylabel("model mean Acc, arcsine transform")
    plt.title('Subject mean Acc versus model-predicted mean Acc')
    plt.show()
    
    #RMSE histograms
    
    #RMSE computed by comparing model/subj trial-by-trial RTs
    plt.hist(results['allRT_rmse'], bins=30)
    plt.xlim(0,1)
    plt.xlabel('allRT_rmse')
    plt.ylabel('Frequency')
    plt.title('RMSE: model/subj trial-by-trial RTs \n Method: '+estName)
    plt.show()
    
    #RMSE computed by comparing model/subj trial-by-trial accuracies
    plt.hist(results['allAcc_rmse'], bins=30)
    plt.xlim(0,1)
    plt.xlabel('allAcc_rmse')
    plt.ylabel('Frequency')
    plt.title('RMSE: model/subj trial-by-trial accuracies \n Method: '+estName)
    plt.show()
    
    #RMSE computed by comparing model/subj block-by-block mean RTs
    plt.hist(results['bbRT_rmse'], bins=30)
    plt.xlim(0,1)
    plt.xlabel('bbRT_rmse')
    plt.ylabel('Frequency')
    plt.title('RMSE: model/subj block-by-block mean RTs \n Method: '+estName)
    plt.show()
    
    #RMSE computed by comparing model/subj block-by-block mean accuracies
    plt.hist(results['bbAcc_rmse'], bins=30)
    plt.xlim(0,1)
    plt.xlabel('bbAcc_rmse')
    plt.ylabel('Frequency')
    plt.title('RMSE: model/subj block-by-block mean accuracies \n Method: '+estName)
    plt.show()
    
    #RMSEs computed by comparing model/subj trial-by-trial RTs, broken up into targets/lures/nonlures
    plt.hist(results['tarRT_rmse'], bins=30, alpha=0.5, label='target')
    plt.hist(results['lurRT_rmse'], bins=30, alpha=0.5, label='lure')
    plt.hist(results['nlrRT_rmse'], bins=30, alpha=0.5, label='nonlure')
    plt.legend(loc='upper right')
    plt.xlim(0,1)
    plt.xlabel('target/lure/nonlure RT rmse')
    plt.ylabel('Frequency')
    plt.title('RMSE: model/subj trial-by-trial RTs \n split by target/lure/nonlure \n Method: '+estName)
    plt.show()
    
    #RMSEs computed by comparing model/subj trial-by-trial accuracies, broken up into targets/lures/nonlures
    plt.hist(results['tarAcc_rmse'], bins=30, alpha=0.5, label='target')
    plt.hist(results['lurAcc_rmse'], bins=30, alpha=0.5, label='lure')
    plt.hist(results['nlrAcc_rmse'], bins=30, alpha=0.5, label='nonlure')
    plt.legend(loc='upper right')
    plt.xlim(0,1)
    plt.xlabel('target/lure/nonlure accuracy rmse')
    plt.ylabel('Frequency')
    plt.title('RMSE: model/subj trial-by-trial accuracies \n split by target/lure/nonlure \n Method: '+estName)
    plt.show()
    
    #compute target/lure/nonlure mean RT RMSEs on a per-participant basis
    tarRT_RMSE = np.sqrt(np.mean((np.array(results['model_tarRT_mean']) - np.array(results['subj_tarRT_mean']))**2))
    lurRT_RMSE = np.sqrt(np.mean((np.array(results['model_lurRT_mean']) - np.array(results['subj_lurRT_mean']))**2))
    nlrRT_RMSE = np.sqrt(np.mean((np.array(results['model_nlrRT_mean']) - np.array(results['subj_nlrRT_mean']))**2))
    print('Target mean RT rmse across participants: ' + str(tarRT_RMSE))
    print('Lure mean RT rmse across participants: ' + str(lurRT_RMSE))
    print('Nonlure mean RT rmse across participants: ' + str(nlrRT_RMSE))
    
    #compute target/lure/nonlure mean accuracy RMSEs on a per-participant basis
    tarAcc_RMSE = np.sqrt(np.mean((np.array(results['model_tarAcc_mean']) - np.array(results['subj_tarAcc_mean']))**2))
    lurAcc_RMSE = np.sqrt(np.mean((np.array(results['model_lurAcc_mean']) - np.array(results['subj_lurAcc_mean']))**2))
    nlrAcc_RMSE = np.sqrt(np.mean((np.array(results['model_nlrAcc_mean']) - np.array(results['subj_nlrAcc_mean']))**2))
    print('Target mean accuracy rmse across participants: ' + str(tarAcc_RMSE))
    print('Lure mean accuracy rmse across participants: ' + str(lurAcc_RMSE))
    print('Nonlure mean accuracy rmse across participants: ' + str(nlrAcc_RMSE))
    
    #histogram of mean differences in trial-by-trial RTs
    # model - subject
    plt.hist(results['rtDiff_mean'], bins=30)
    plt.xlabel('Mean difference in RT')
    plt.ylabel('Frequency')
    plt.title('Mean difference in trial-by-trial RTs (modelRT - subjRT) \n worthwhile to estimate :lf? \n Method: '+estName)
    plt.show()
    
    #were there any that didn't converge?
    success = 'Optimization terminated successfully.'
    successCheck = [1 if x==success else 0 for x in results['converged']]
    print('There were '+str(len(successCheck)-np.sum(successCheck))+' participants that did not converge!')
    

    
    
    
    
    