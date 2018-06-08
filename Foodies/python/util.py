import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def removeSpace(text):
    text = ''.join(text.split("\n"))
    split = text.split(" ")
    text = ""
    for part in split:
        if part != "":
            text += part + " "
    text = text[:-1]
    return text

def plotAUC(aucs, steps, title=None):
        
    ax = sns.tsplot(aucs, range(0, steps * len(aucs), steps), color='#a297FF')

    #plotting the two lines
    p1 = plt.axhline(y=-1,color='#a297FF', label="AUC")
    p1 = plt.axhline(y=max(aucs),color='#EF9A9A', label="max AUC")
    #p2 = plt.axvline(x=x1,color='#EF9A9A')

    #plt.setp(ax.get_legend().get_texts(), fontsize='22') # for legend text

    ax.set_ylim([0.475, 0.875])
    
    fig = plt.gcf()
    fig.set_size_inches(14, 8)
    
    if title is not None:
        ax.set_title(title)
    
    ax.set(xlabel='Iterations', ylabel='AUC')
        
    plt.legend()
    plt.show()


def plotHealthHistogram(data, title=None):
    traffic_red = '#F01A24'
    traffic_orange = '#FFA420'
    traffic_green = '#5EB20B'
        
    x0 = 5.5
    x1 = 8.5

    shadow = None
    #plotting the PDF
    if len(data) == 2:
        shadow = sns.kdeplot(data[1], color='#a297FF', bw=0.5)
        shadow_kde_x, shadow_kde_y = shadow.lines[0].get_data()
        
        ax = sns.kdeplot(data[0], color='#383838', bw=0.5)
        kde_x, kde_y = ax.lines[1].get_data()
    else:
        ax = sns.kdeplot(data, color='#383838', bw=0.5)
        kde_x, kde_y = ax.lines[0].get_data()

    #plotting the two lines
    #p1 = plt.axhline(y=0.2,color='#EF9A9A', label="max AUC")
    #p2 = plt.axvline(x=x1,color='#EF9A9A')


    ax.fill_between(kde_x, kde_y, where=(kde_x<x0), 
                    interpolate=False, color=traffic_green)

    ax.fill_between(kde_x, kde_y, where=(kde_x>=x0) & (kde_x<=x1) , 
                    interpolate=False, color=traffic_orange)

    ax.fill_between(kde_x, kde_y, where=(kde_x>=x1) , 
                    interpolate=False, color=traffic_red)

    plt.setp(ax.get_legend().get_texts(), fontsize='22') # for legend text
    
    if shadow is not None:
        shadow.fill_between(shadow_kde_x, shadow_kde_y, 
                interpolate=False, color='#a297FF', alpha=0.33)

    newlim = [ax.get_ylim()[0], ax.get_ylim()[1]*1.0]
    ax.set_ylim(newlim)
    ax.set_xlim([4,12])
    
    fig = plt.gcf()
    fig.set_size_inches(14, 8)
    
    if title is not None:
        ax.set_title(title)
    
    ax.set(xlabel='Health Score', ylabel='PDF')
        
    plt.legend()
    plt.show()

def compareFails(allInteractions, data, dataTitles, colors = ['r', 'b', 'g', 'y', 'purple']):

    data_fail_rate = []
    for i in range(len(data)):
        data_fail_rate.append([])
    
    ranges = [10, 30, 100, 500, 2000, 10000]
    
    for j in range(len(data)):
        totRecipes = len(allInteractions[0])
        failRecipes = len(data[j][0])
        data_fail_rate[j].append(failRecipes / totRecipes)
            
    for i in range(len(ranges)-1):
        totRecipes = sum(allInteractions[0].map(lambda x: 1 if x >= ranges[i] and x < ranges[i+1] else 0))

        for j in range(len(data)):
            failRecipes = sum(data[j][0].map(lambda x: 1 if x >= ranges[i] and x < ranges[i+1] else 0))
            data_fail_rate[j].append(failRecipes / totRecipes)
            
    N = len(data_fail_rate[0])

    ind = np.arange(N)  # the x locations for the groups
    width = 1 / (len(data) + 0.3)      # the width of the bars

    fig, ax = plt.subplots()
    fig.set_size_inches(16, 10)
    rects = []
    
    for i in range(len(data)):
        rects.append(ax.bar(ind + (i*width), data_fail_rate[i], width, color=colors[i]))

    # add some text for labels, title and axes ticks
    ax.set_ylabel('Failure Rate')
    ax.set_xlabel('Recipe Popularity')
    ax.set_title('Failure Rate vs Recipe Popularity')
    ax.set_xticks(ind + 2 * width)
    xticks = ["Overall"]
    for i in range(len(ranges)-1):
        xticks.append(str(ranges[i]) + "-" + str(ranges[i+1]-1))
    ax.set_xticklabels(xticks)

    ax.legend(tuple(map(lambda x: x[0], rects)), dataTitles)


    def autolabel(rects):
        """
        Attach a text label above each bar displaying its height
        """
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width()/2., 1.0*height, '%.1f' % (100 * height) + "%",
                    ha='center', va='bottom', size=8)

    for rect in rects:
        autolabel(rect)

    plt.show()


def compareFailsRate(allInteractions, data, dataTitles, colors = ['r', 'b', 'g', 'y', 'purple']):

    data_fail_rate = []
    for i in range(len(data)):
        data_fail_rate.append([])
    
    ranges = [10, 30, 100, 500, 2000, 10000]
    
            
    for i in range(len(ranges)-1):

        for j in range(len(data)):
            totRecipes = len(data[j][0])
            failRecipes = sum(data[j][0].map(lambda x: 1 if x >= ranges[i] and x < ranges[i+1] else 0))
            data_fail_rate[j].append(failRecipes / totRecipes)
            
    N = len(data_fail_rate[0])

    ind = np.arange(N)  # the x locations for the groups
    width = 1 / (len(data) + 0.3)      # the width of the bars

    fig, ax = plt.subplots()
    fig.set_size_inches(16, 10)
    rects = []
    
    for i in range(len(data)):
        rects.append(ax.bar(ind + (i*width), data_fail_rate[i], width, color=colors[i]))

    # add some text for labels, title and axes ticks
    ax.set_ylabel('Failure Rate')
    ax.set_xlabel('Recipe Popularity')
    ax.set_title('Failure Rate vs Recipe Popularity')
    ax.set_xticks(ind + 2 * width)
    xticks = []
    for i in range(len(ranges)-1):
        xticks.append(str(ranges[i]) + "-" + str(ranges[i+1]-1))
    ax.set_xticklabels(xticks)

    ax.legend(tuple(map(lambda x: x[0], rects)), dataTitles)


    def autolabel(rects):
        """
        Attach a text label above each bar displaying its height
        """
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width()/2., 1.0*height, '%.1f' % (100 * height) + "%",
                    ha='center', va='bottom', size=8)

    for rect in rects:
        autolabel(rect)

    plt.show()
    