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