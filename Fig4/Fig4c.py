#!/usr/bin/python  
#-*- coding:utf-8 -*-  
############################  
#File Name: 03_make_plot.py
#Author: ShiFY
#Mail: shify@mail.cbi.pku.edu.cn  
#Created Time: 2018-12-07 21:43:58
############################  
import os
import sys
import pandas as pd
import numpy as np
import matplotlib
import matplotlib as mpl
import matplotlib.pyplot as plt
import brewer2mpl
from sklearn import preprocessing
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.ticker as ticker
from matplotlib import rcParams

matplotlib.rcParams['xtick.direction'] = 'out' 
matplotlib.rcParams['ytick.direction'] = 'out'

matplotlib.pyplot.switch_backend('agg')
data_path = "./Fig4a-d/CASE-2.csv" 

#========================Load data and merge===========================================
data = pd.read_csv(data_path,header=None)
data_lead = pd.concat((data.iloc[:,2],data.iloc[:,0:2],data.iloc[:,3:5],data.iloc[:,18]),axis=1)
data_lead.columns = ['rs','chr','pos','Ref','Alt','CARMEN']
data_lead['r2'] = 1.0
data_lead['snptype'] = 'lead'
data_lead.drop_duplicates(inplace=True)

data_ld = pd.concat((data.iloc[:,10],data.iloc[:,12:16],data.iloc[:,19],data.iloc[:,9]),axis=1)
data_ld.columns = ['rs','chr','pos','Ref','Alt','CARMEN','r2']
data_ld['snptype'] = 'ld'

data_plot = pd.concat((data_lead,data_ld),axis=0)
data_plot.loc[data_plot['CARMEN'].argmax(),'snptype'] = 'best-ld'
#data_plot['size'] = (data_plot['r2'] - np.min(data_plot['r2']) + 0.1) * 10
data_plot['size'] = (data_plot['r2']) * 1000
#======================Make plot========================================================

fig,ax = plt.subplots(figsize=(3.8,2.91))
label_list = ['lead','ld','best-ld']
color_list = ['blue','salmon','orange']
marker_list = ['*','.','D']
for iterm in [1,0,2]:
    label_in = label_list[iterm]
    color_in = color_list[iterm]
    marker_in = marker_list[iterm]

    x = data_plot[data_plot['snptype'] == label_in].pos
    y = data_plot[data_plot['snptype'] == label_in]['CARMEN']
    z = data_plot[data_plot['snptype'] == label_in].size
    
    ax.scatter(x, y, s = 100, facecolors = color_in, edgecolors = 'none', marker = marker_in, linewidth = 0.5, alpha = 0.9) #make bubble plot, the s is the size of bubble.
    if label_in == 'lead':
        ax.annotate(data_plot[data_plot['snptype'] == 'lead']['rs'].values[0],(x+4000,y),fontsize=10)
    if label_in == 'best-ld':
        ax.annotate(data_plot[data_plot['snptype'] == 'best-ld']['rs'].values[0],(x+9000,y),fontsize=10)

#ax.grid()
#cbar = fig.colorbar(bubble)
#cbar.set_label('F1 Score',labelpad=-40, y=1.05,rotation=0) # set the label of the legend colorbar



ax.get_xaxis().get_major_formatter().set_useOffset(False)
ticks_num = ax.get_xticks()[1::2]
ax.set_xticks(ax.get_xticks()[1::2])
ax.set_xticklabels(ticks_num.astype('int').astype('str').tolist())
               
ax.set_ylim(-0.01,0.2500001) # To make the y axis label in the middle position
#plt.yticks(y,data_sort.Tools) # Here we need use plt.yticks to match the y and label, if we use as.set_yticklabels, the label position will be wrong
ax.set_xlabel(data.iloc[0,0], fontsize = 10)
ax.set_ylabel('CARMEN Score', fontsize = 10)

ax.spines['top'].set_visible(False) # Do not have the spines of right
ax.spines['right'].set_visible(False)
ax.tick_params(top='off',bottom='on',left='on',right='off') # Do not have the scale of the right and top.
ax.spines['bottom'].set_linewidth(1)
ax.spines['left'].set_linewidth(1)


#ax.text(.5,.95,str(sys.argv[1]), horizontalalignment='center', transform=ax.transAxes)
ax.xaxis.set_tick_params(width=1,labelsize=10)
ax.yaxis.set_tick_params(width=1,labelsize=10)

plt.tight_layout() #Make all information showed on the picture.
plt.show()

pp = PdfPages(data_path.replace('csv','pdf'))
pp.savefig(fig)
pp.close()

