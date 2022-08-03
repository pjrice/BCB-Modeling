
import json
import matplotlib.pyplot as plt


def makeRetrievalPlot (path2file, parVals):
    
    with open(path2file) as f:
        tempData = json.load(f)
        
    # data will be list of length n, where n is the number of trial the model performed
    # each element of data is a list of length 3
    #   data[n][0] == time of the retrieval, in milliseconds
    #   data[n][1] == the slot/value specifications of the retrieval request
    #   data[n][2] == a list of chunks that were considered for the retrieval. Each element of data[n][2] is a list of chunk details
    # as n increases, the list in data[n][2] increases in size m (there are more chunks to be considered for retrieval)
    # no matter the length of data[n][2], each element of data[n][2] is a list of length 4
    #   data[n][2][m][0] == the name of the chunk being considered for retrieval
    #   data[n][2][m][1] == the name of the chunk and it's slot/value pairs
    #   data[n][2][m][2] == declarative parameters for the chunk in question at time of retrieval (including activation)
    #   data[n][2][m][3] == full details of the activation computation for the chunk in quesiton (including activation with more precision)
    data = json.loads(tempData['data'])
    
    
    #get time of each retrieval - this (sort of) forms our x axis
    #for each chunk, get activation value at time of every retrieval

    
    #using the last trial, get unique chunk names
    # data[-1][2] == the list of chunks considered for retrieval on the last trial
    chunkNames = [chunkDetails[0] for chunkDetails in data[-1][2]]
    
    chunkNames.sort()
    
    #for each chunk name, parse data and at each reference, get retrieval time and activation value
    chunkActivations = dict()
    for chunkName in chunkNames:
        
        chunkActivations[chunkName] = dict()
        chunkActivations[chunkName]['retrievalTime'] = list()
        chunkActivations[chunkName]['activationValue'] = list()
        
        #loop through trials
        for tNum in range(len(data)):
            
            #loop through chunks considered for this trial
            for chunkNum in range(len(data[tNum][2])):
                
                if data[tNum][2][chunkNum][0] == chunkName:
                    chunkActivations[chunkName]['retrievalTime'].append(data[tNum][0]/1000) #convert to seconds by dividing by 1000
                    chunkActivations[chunkName]['activationValue'].append(float(data[tNum][2][chunkNum][3].split()[-1]))
    
    #make the plot
    # set up two-subplot figure and set title of fig
    fig, (ax1, ax2) = plt.subplots(1,2, sharey=True, figsize=(24,12))
    #fig.suptitle("Activation levels at retrieval for cue and stimulus chunks", fontsize='xx-large')

    #plot the stimulus activation values first in grey
    for chunkName in list(chunkActivations.keys()):
        if chunkName[0]=='S':
            ax1.plot(chunkActivations[chunkName]['retrievalTime'],chunkActivations[chunkName]['activationValue'], marker='o', label='stimulus', color='grey')
            ax2.plot(chunkActivations[chunkName]['retrievalTime'],chunkActivations[chunkName]['activationValue'], marker='o', label='stimulus', color='grey')

    #doing this in a separate loop so that chunks always print on top of stimuli
    #have to manually pass colors only because the natural order is (...brown, pink, GREY, olive,...) and grey is already used for stimuli, so we want to skip it
    #https://matplotlib.org/3.1.0/gallery/color/named_colors.html
    colors = ['tab:blue','tab:orange','tab:green','tab:red','tab:purple','tab:brown','tab:pink','tab:olive']
    cIdx = 0
    for chunkName in list(chunkActivations.keys()):
        if chunkName[0]=='C':
            ax1.plot(chunkActivations[chunkName]['retrievalTime'],chunkActivations[chunkName]['activationValue'], marker='o', label=chunkName, color=colors[cIdx])
            ax2.plot(chunkActivations[chunkName]['retrievalTime'],chunkActivations[chunkName]['activationValue'], marker='o', label=chunkName, color=colors[cIdx])
            cIdx += 1
    
    #add horizontal line at yaxis = 0
    ax1.hlines(y=0,xmin=0,xmax=125,linewidths=3)
    ax2.hlines(y=0,xmin=86525,xmax=86650,linewidths=3)
    
    #set x limits, axes labels, title, and legend for first subplot
    ax1.set_xlim(0,125)
    ax1.tick_params(axis='both',labelsize=14)
    ax1.set_xlabel("Time of retrieval (s)", fontsize=16)
    ax1.set_ylabel("Activation value at time of retrieval", fontsize=16)
    ax1.set_title('Session 1', fontsize=20)
    handles, labels = ax1.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax1.legend(by_label.values(), by_label.keys(),loc='lower left', fontsize=18)
    

    #add textbox to first subplot with parameter values
    css = parVals['css']
    ga = parVals['ga']
    ia = parVals['ia']
    lf = parVals['lf']
    bll = parVals['bll']
    textstr = '\n'.join((
        r'd = %.2f' % (bll, ),
        r'Wi = %.2f' % (ia, ),
        r'Wg = %.2f' % (ga, ),
        r'F = %.2f' % (lf, ),
        r'c = %.2f' % (css, )))
    props = dict(boxstyle='round', facecolor='white', alpha=0.5)
    ax1.text(0.8, 0.05, textstr, transform=ax1.transAxes, bbox=props, fontsize=18)
    
    for axis in ['top','bottom','left','right']:
        ax1.spines[axis].set_linewidth(2)

    #set x limits, axes labels, and title for second subplot
    ax2.set_xlim(86525,86650)
    ax2.tick_params(axis='x',labelsize=14)
    ax2.set_xlabel("Time of retrieval (s)", fontsize=16)
    ax2.set_ylabel("Activation value at time of retrieval", fontsize=16)
    ax2.set_title('Session 2', fontsize=20)
    
    for axis in ['top','bottom','left','right']:
        ax2.spines[axis].set_linewidth(2)

    #plt.xticks(fontsize=14)
    plt.show()
                    
                    
            
            
            
        
##############################################################################
# generate plot of model activation values at default parameter settings

path2file = 'Z:\\gp\\ACTR-WM\\dissertation\\figures\\data\\retrievalHistories\\zb_initParVals.json'
parVals = {'css':0, 'ga':1, 'ia':1, 'lf':2.25, 'bll':0.5}
makeRetrievalPlot(path2file,parVals)

path2file = 'Z:\\gp\\ACTR-WM\\dissertation\\figures\\data\\retrievalHistories\\zb_partParVals.json'
parVals = {'css':-0.434, 'ga':1.24, 'ia':0.343, 'lf':2.86, 'bll':0.483}
makeRetrievalPlot(path2file,parVals)

    
    
    