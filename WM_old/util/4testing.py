




css = 0
ga = 1
ia = 1
lf = 1
bll = 0.5
stimTiming = create_stim_timing()


actr.load_act_r_code("Z:\gp\ACTR-WM\code\models\zeroBack\zeroBack-device.lisp")

correctResponses = read_correct_responses("Z:\gp\ACTR-WM\data\zeroBack_correctResponses.csv")
targetTypes = [x[1] for x in correctResponses]

correctCueChunks = np.array(['CUE0-0','CUE1-0','CUE2-0','CUE3-0','CUE4-0','CUE5-0','CUE6-0','CUE7-0'])
correctCueChunks = np.repeat(correctCueChunks,10,axis=0).tolist()


subjResponses = read_participant_data('Z:\gp\ACTR-WM\data\sub-100307\zb_testResponses.csv')





actr.load_act_r_model("Z:\gp\ACTR-WM\code\models\zeroBack\zeroBack-model-main.lisp")








actr.load_act_r_code("Z:\gp\ACTR-WM\code\models\zeroBack\zeroBack-device.lisp")


actr.load_act_r_code("Z:\gp\ACTR-WM\code\models\zeroBack\zeroBack-device_retrievalInterrupt.lisp")


actr.load_act_r_model("Z:\gp\ACTR-WM\code\models\zeroBack\zeroBack-model-main_retrievalInterrupt.lisp")

css = 0
ga = 1
ia = 1
lf = 20
bll = 0.5
stimTiming = create_stim_timing()


for i in range(0,100):
    
    tempModelResponses = runTask(css,ga,ia,lf,bll,stimTiming)
    modelResponses = [[i[0],i[1],i[2],j] for i,j in zip(tempModelResponses,targetTypes)]
    model_tarRT = np.array([x[1] for x in modelResponses if x[3]=='target'], dtype=np.float)
    
    print(np.mean(model_tarRT))

    
    
    
    