

import sys
# insert at 1, 0 is the script path (or '' in REPL)
#sys.path.insert(1, '/home/pjrice/gp/ACTR-WM/code/estimation')
sys.path.insert(1, 'Z:\gp\ACTR-WM\code\estimation')
from modelEstimationUtilFunctions import *

import os
#os.chdir('/home/pjrice/Downloads/ACT-R/tutorial/python')
os.chdir('C:\\Users\\Patrick\\Desktop\\ACT-R\\tutorial\\python')
import actr


def compute_model_acc_temp (cResp,mResp):
    responses = [[i[0],j[0],j[3]] for i,j in zip(cResp,mResp)]
    
    #calculate total accuracy
    totAccVec = [1 if x[0]==x[1] else 0 for x in responses]
    
    #calculate target accuracy
    tarAccVec = [1 if x[0]==x[1] else 0 for x in responses if x[2]=='target']
    
    #calculate lure accuracy
    lurAccVec = [1 if x[0]==x[1] else 0 for x in responses if x[2]=='lure']

    #calculate nonlure accuracy
    nlrAccVec = [1 if x[0]==x[1] else 0 for x in responses if x[2]=='nonlure']

    return([totAccVec, tarAccVec, lurAccVec, nlrAccVec])


def compute_model_acc_temp2 (correctRespChunks,imaginalRespChunks,targetTypes):
    """Computes the accuracy of the model by determining if a cue chunk was retrieved or not.
       If the cue chunk was retrieved, there are no other sources of noise/error in the model 
       and so the response the model makes (whether the stimulus is target or nontarget) will
       be correct. However, if a stimulus chunk was retrieved, this is counted as incorrect
       (i.e., the "mind" made an error), even though the response may seem to be correct
       (such as in the case the stimulus chunk that was retrieved does not match the current 
        nontarget stimulus)"""
    
    
    responses = [[i,j,k] for i,j,k in zip(correctRespChunks,imaginalRespChunks,targetTypes)]
    
    #calculate total accuracy
    totAccVec = [1 if x[0]==x[1] else 0 for x in responses]
    
    #calculate target accuracy
    tarAccVec = [1 if x[0]==x[1] else 0 for x in responses if x[2]=='target']
    
    #calculate lure accuracy
    lurAccVec = [1 if x[0]==x[1] else 0 for x in responses if x[2]=='lure']

    #calculate nonlure accuracy
    nlrAccVec = [1 if x[0]==x[1] else 0 for x in responses if x[2]=='nonlure']

    
    return([totAccVec, tarAccVec, lurAccVec, nlrAccVec])

def compute_model_acc_combined (correctResponses,modelResponses,correctRespChunks,imaginalRespChunks,targetTypes):
    
    
    keypressRespAccVec = [1 if i[0]==j[0] else 0 for i,j in zip(correctResponses,modelResponses)]
    
    chunkAccVec = [1 if i==j else 0 for i,j in zip(correctRespChunks,imaginalRespChunks)]
    
    combinedAccVec = [i if j==1 else 0 for i,j in zip(keypressRespAccVec,chunkAccVec)]
    
    combinedAccVecTT = [[i,j] for i,j in zip(combinedAccVec,targetTypes)]
    
    tarAccVec = [x[0] for x in combinedAccVecTT if x[1]=='target']
    lurAccVec = [x[0] for x in combinedAccVecTT if x[1]=='lure']
    nlrAccVec = [x[0] for x in combinedAccVecTT if x[1]=='nonlure']
    
    return([combinedAccVec,tarAccVec,lurAccVec,nlrAccVec])


correctRespChunksB1 = [[None,None,None],
                       ['BP_006_BP2_BA.png','NOTHING', 'NOTHING'],
                       ['BP_001_BP1_BA.png','BP_006_BP2_BA.png','NOTHING'],
                       ['BP_006_BP2_BA.png','BP_001_BP1_BA.png','NOTHING'],
                       ['BP_003_BP16_BA.png','BP_006_BP2_BA.png','NOTHING'],
                       ['BP_003_BP16_BA.png','BP_003_BP16_BA.png','NOTHING'],
                       ['BP_002_BP10_BA.png','BP_003_BP16_BA.png','NOTHING'],
                       ['BP_004_BP18_BA.png','BP_002_BP10_BA.png','NOTHING'],
                       ['BP_002_BP10_BA.png','BP_004_BP18_BA.png','NOTHING'],
                       ['BP_005_BP19_BA.png','BP_002_BP10_BA.png','NOTHING']]

correctRespChunksB2 = [[None,None,None],
                       ['TO_004_TOOL4_BA.png','NOTHING', 'NOTHING'],
                       ['TO_004_TOOL4_BA.png','TO_004_TOOL4_BA.png','NOTHING'],
                       ['TO_001_TOOL1_BA.png','TO_004_TOOL4_BA.png','NOTHING'],
                       ['TO_002_TOOL2_BA.png','TO_001_TOOL1_BA.png','NOTHING'],
                       ['TO_001_TOOL1_BA.png','TO_002_TOOL2_BA.png','NOTHING'],
                       ['TO_005_TOOL5_BA.png','TO_001_TOOL1_BA.png','NOTHING'],
                       ['TO_005_TOOL5_BA.png','TO_005_TOOL5_BA.png','NOTHING'],
                       ['TO_006_TOOL6_BA.png','TO_005_TOOL5_BA.png','NOTHING'],
                       ['TO_002_TOOL2_BA.png','TO_006_TOOL6_BA.png','NOTHING']]

correctRespChunksB3 = [[None,None,None],
                       ['FC_010_F5.png','NOTHING', 'NOTHING'],
                       ['FC_008_F4.png','FC_010_F5.png','NOTHING'],
                       ['FC_008_F4.png','FC_008_F4.png','NOTHING'],
                       ['FC_012_F6.png','FC_008_F4.png','NOTHING'],
                       ['FC_012_F6.png','FC_012_F6.png','NOTHING'],
                       ['FC_007_M4.png','FC_012_F6.png','NOTHING'],
                       ['FC_009_M5.png','FC_007_M4.png','NOTHING'],
                       ['FC_007_M4.png','FC_009_M5.png','NOTHING'],
                       ['FC_009_M5.png','FC_007_M4.png','NOTHING']]

correctRespChunksB4 = [[None,None,None],
                       ['PL_007_92026.png','NOTHING', 'NOTHING'],
                       ['PL_010_92038.png','PL_007_92026.png','NOTHING'],
                       ['PL_009_92037.png','PL_010_92038.png','NOTHING'],
                       ['PL_010_92038.png','PL_009_92037.png','NOTHING'],
                       ['PL_009_92037.png','PL_010_92038.png','NOTHING'],
                       ['PL_008_92033.png','PL_009_92037.png','NOTHING'],
                       ['PL_008_92033.png','PL_008_92033.png','NOTHING'],
                       ['PL_012_92047.png','PL_008_92033.png','NOTHING'],
                       ['PL_012_92047.png','PL_012_92047.png','NOTHING']]

correctRespChunksB5 = [[None,None,None],
                       ['TO_014_TOOL14_BA.png','NOTHING', 'NOTHING'],
                       ['TO_016_TOOL16_BA.png','TO_014_TOOL14_BA.png','NOTHING'],
                       ['TO_016_TOOL16_BA.png','TO_016_TOOL16_BA.png','NOTHING'],
                       ['TO_013_TOOL13_BA.png','TO_016_TOOL16_BA.png','NOTHING'],
                       ['TO_018_TOOL18_BA.png','TO_013_TOOL13_BA.png','NOTHING'],
                       ['TO_013_TOOL13_BA.png','TO_018_TOOL18_BA.png','NOTHING'],
                       ['TO_014_TOOL14_BA.png','TO_013_TOOL13_BA.png','NOTHING'],
                       ['TO_013_TOOL13_BA.png','TO_014_TOOL14_BA.png','NOTHING'],
                       ['TO_015_TOOL15_BA.png','TO_013_TOOL13_BA.png','NOTHING']]

correctRespChunksB6 = [[None,None,None],
                       ['FC_017_M9.png','NOTHING', 'NOTHING'],
                       ['FC_017_M9.png','FC_017_M9.png','NOTHING'],
                       ['FC_015_M8.png','FC_017_M9.png','NOTHING'],
                       ['FC_015_M8.png','FC_015_M8.png','NOTHING'],
                       ['FC_018_F9.png','FC_015_M8.png','NOTHING'],
                       ['FC_016_F8.png','FC_018_F9.png','NOTHING'],
                       ['FC_018_F9.png','FC_016_F8.png','NOTHING'],
                       ['FC_013_M7.png','FC_018_F9.png','NOTHING'],
                       ['FC_014_F7.png','FC_013_M7.png','NOTHING']]

correctRespChunksB7 = [[None,None,None],
                       ['BP_019_H14-T_BA.png','NOTHING', 'NOTHING'],
                       ['BP_024_H3-T_BA.png','BP_019_H14-T_BA.png','NOTHING'],
                       ['BP_019_H14-T_BA.png','BP_024_H3-T_BA.png','NOTHING'],
                       ['BP_025_H5-T_BA.png','BP_019_H14-T_BA.png','NOTHING'],
                       ['BP_023_H25-T_BA.png','BP_025_H5-T_BA.png','NOTHING'],
                       ['BP_025_H5-T_BA.png','BP_023_H25-T_BA.png','NOTHING'],
                       ['BP_020_H17-T_BA.png','BP_025_H5-T_BA.png','NOTHING'],
                       ['BP_020_H17-T_BA.png','BP_020_H17-T_BA.png','NOTHING'],
                       ['BP_022_H24-T_BA.png','BP_020_H17-T_BA.png','NOTHING']]

correctRespChunksB8 = [[None,None,None],
                       ['PL_017_SCENE_03.png','NOTHING', 'NOTHING'],
                       ['PL_016_SCENE_02.png','PL_017_SCENE_03.png','NOTHING'],
                       ['PL_017_SCENE_03.png','PL_016_SCENE_02.png','NOTHING'],
                       ['PL_019_SCENE_05.png','PL_017_SCENE_03.png','NOTHING'],
                       ['PL_019_SCENE_05.png','PL_019_SCENE_05.png','NOTHING'],
                       ['PL_015_SCENE_01.png','PL_019_SCENE_05.png','NOTHING'],
                       ['PL_015_SCENE_01.png','PL_015_SCENE_01.png','NOTHING'],
                       ['PL_020_SCENE_06.png','PL_015_SCENE_01.png','NOTHING'],
                       ['PL_018_SCENE_04.png','PL_020_SCENE_06.png','NOTHING']]

correctRespChunksList = [correctRespChunksB1,correctRespChunksB2,correctRespChunksB3,correctRespChunksB4,correctRespChunksB5,correctRespChunksB6,correctRespChunksB7,correctRespChunksB8]

correctRespChunks  = [triallist for blocklist in correctRespChunksList for triallist in blocklist]

correctRespChunks = [list(map(str.upper, x)) if x[0] is not None else x for x in correctRespChunks]


# some stuff to use to evaluate model responses
correctResponses = read_correct_responses('Z:\\gp\\ACTR-WM\\data\\oneBack_correctResponses.csv')
targetTypes = [x[1] for x in correctResponses]
stimTiming = create_stim_timing()


# load task device and model
path2device='Z:\\gp\\ACTR-WM\\code\\models\\twoBack\\oneBack-device.lisp'
#path2model='Z:\\gp\\ACTR-WM\\code\\models\\twoBack\\twoBack-model-main.lisp'
#path2model='Z:\\gp\\ACTR-WM\\code\\models\\twoBack\\twoBack-model-main - retrieveNBackStim.lisp'
path2model='Z:\\gp\\ACTR-WM\\code\\models\\twoBack\\twoBack-model-main - dynamicUpdateLoop.lisp'

actr.load_act_r_code(path2device)



actr.load_act_r_model(path2model)

#actr.call_command('record-history', 'retrieval-history')

# run the model
actr.call_command('runTaskFromPython')

# retrieve the responses
tempModelResponses = actr.call_command('print-resp')
tempModelResponses.reverse()

imaginalRespChunks = actr.call_command('print-imaginal-chunks')
imaginalRespChunks.reverse()
    
# get model's keypress responses, RTs, and retrieved chunks
tempResponses = [x[0] for x in tempModelResponses]
tempRTs = [x[1] for x in tempModelResponses]
tempChunkRetrievals = [x[2] for x in tempModelResponses]
    
# compute RTs by subtracting the timing of the stimuli
modelRespTimes = [round((i-j),3) if i is not None else i for i,j in zip(tempRTs,stimTiming.tolist())]
    
# clean up responses/RTs/chunk retrievals into list of lists
tempModelResponses = [[i,j,k] for i,j,k in zip(tempResponses,modelRespTimes,tempChunkRetrievals)]

modelResponses = [[i[0],i[1],i[2],j] for i,j in zip(tempModelResponses,targetTypes)]

modelRTs = np.array([x[1] for x in modelResponses], dtype=np.float)

[totAccVec,tarAccVec,lurAccVec,nlrAccVec] = compute_model_acc_temp(correctResponses,modelResponses)

[totAccVec1,tarAccVec1,lurAccVec1,nlrAccVec1] = compute_model_acc_temp2(correctRespChunks,imaginalRespChunks,targetTypes)

[totAccVec2,tarAccVec2,lurAccVec2,nlrAccVec2] = compute_model_acc_combined(correctResponses,modelResponses,correctRespChunks,imaginalRespChunks,targetTypes)

#[1 if i==j else 0 for i,j in zip(nlrAccVec,nlrAccVec1)]
#np.column_stack((nlrAccVec,nlrAccVec1))

print('')
print('Total model accuracy: '+str(sum(totAccVec)/len(totAccVec)))
print('Target model accuracy: '+str(sum(tarAccVec)/len(tarAccVec)))
print('Lure model accuracy: '+str(sum(lurAccVec)/len(lurAccVec)))
print('Nonlure model accuracy: '+str(sum(nlrAccVec)/len(nlrAccVec)))
print('')
print('Total model accuracy (chunks): '+str(sum(totAccVec1)/len(totAccVec1)))
print('Target model accuracy (chunks): '+str(sum(tarAccVec1)/len(tarAccVec1)))
print('Lure model accuracy (chunks): '+str(sum(lurAccVec1)/len(lurAccVec1)))
print('Nonlure model accuracy (chunks): '+str(sum(nlrAccVec1)/len(nlrAccVec1)))
print('')
print('Total model accuracy (combined): '+str(sum(totAccVec2)/len(totAccVec2)))
print('Target model accuracy (combined): '+str(sum(tarAccVec2)/len(tarAccVec2)))
print('Lure model accuracy (combined): '+str(sum(lurAccVec2)/len(lurAccVec2)))
print('Nonlure model accuracy (combined): '+str(sum(nlrAccVec2)/len(nlrAccVec2)))
print('')
print('Number of no response trials: '+str(sum(np.isnan(modelRTs))))
print('Model mean RT: '+str(np.nanmean(modelRTs)))

examineChunkAcc = [[i,j,k,l] for i,j,k,l in zip(correctRespChunks,imaginalRespChunks,targetTypes,totAccVec1)]


tarChunkAcc = [x for x in examineChunkAcc if x[2]=='target']
lurChunkAcc = [x for x in examineChunkAcc if x[2]=='lure']
nlrChunkAcc = [x for x in examineChunkAcc if x[2]=='nonlure']


totAccs = list()
tarAccs = list()
lurAccs = list()
nlrAccs = list()
model_runRTs = list()
for run in range(0,100):
    
    print(run)
    
    actr.load_act_r_model(path2model)

    # run the model
    actr.call_command('runTaskFromPython')

    # retrieve the responses
    tempModelResponses = actr.call_command('print-resp')
    tempModelResponses.reverse()

    imaginalRespChunks = actr.call_command('print-imaginal-chunks')
    imaginalRespChunks.reverse()
    
    # get model's keypress responses, RTs, and retrieved chunks
    tempResponses = [x[0] for x in tempModelResponses]
    tempRTs = [x[1] for x in tempModelResponses]
    tempChunkRetrievals = [x[2] for x in tempModelResponses]
    
    # compute RTs by subtracting the timing of the stimuli
    modelRespTimes = [round((i-j),3) if i is not None else i for i,j in zip(tempRTs,stimTiming.tolist())]
    
    # clean up responses/RTs/chunk retrievals into list of lists
    tempModelResponses = [[i,j,k] for i,j,k in zip(tempResponses,modelRespTimes,tempChunkRetrievals)]

    modelResponses = [[i[0],i[1],i[2],j] for i,j in zip(tempModelResponses,targetTypes)]

    modelRTs = np.array([x[1] for x in modelResponses], dtype=np.float)
    modelMeanRT = np.nanmean(modelRTs)
    
    [totAccVec2,tarAccVec2,lurAccVec2,nlrAccVec2] = compute_model_acc_combined(correctResponses,modelResponses,correctRespChunks,imaginalRespChunks,targetTypes)
    
    totAcc = sum(totAccVec2)/len(totAccVec2)
    tarAcc = sum(tarAccVec2)/len(tarAccVec2)
    lurAcc = sum(lurAccVec2)/len(lurAccVec2)
    nlrAcc = sum(nlrAccVec2)/len(nlrAccVec2)
    
    totAccs.append(totAcc)
    tarAccs.append(tarAcc)
    lurAccs.append(lurAcc)
    nlrAccs.append(nlrAcc)
    model_runRTs.append(modelMeanRT)
    
    


import matplotlib.pyplot as plt
    
fig, axs = plt.subplots(2,2,sharey=True,sharex=True)
fig.suptitle('Model accuracies across 100 runs')
axs[0,0].hist(totAccs,bins=10)
axs[0,0].set_title('Total accuracy')
axs[0,0].set_ylabel('Count')
axs[0,0].annotate('mean='+str(round(np.mean(totAccs),3)),xy=(0.7,30))

axs[0,1].hist(tarAccs,bins=7)
axs[0,1].set_title('Target accuracy')
axs[0,1].annotate('mean='+str(round(np.mean(tarAccs),3)),xy=(0.7,30))
    
axs[1,0].hist(lurAccs,bins=7)
axs[1,0].set_title('Lure accuracy')
axs[1,0].set_xlabel('acc %')
axs[1,0].set_ylabel('Count')
axs[1,0].annotate('mean='+str(round(np.mean(lurAccs),3)),xy=(0.7,30))

axs[1,1].hist(nlrAccs,bins=10)
axs[1,1].set_title('Nontarget accuracy')
axs[1,1].set_xlabel('acc %')
axs[1,1].annotate('mean='+str(round(np.mean(nlrAccs),3)),xy=(0.7,30))

plt.show()

plt.hist(model_runRTs,bins=10)
plt.title('Model RT across 100 runs')
plt.xlabel('RT (s)')
plt.ylabel('Count')
plt.annotate('mean='+str(round(np.mean(model_runRTs),3)),xy=(1.025,20))
plt.show()














