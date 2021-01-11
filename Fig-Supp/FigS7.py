#!/usr/bin/python  
#-*- coding:utf-8 -*-  
############################  
#File Name: 05_sta_population_get_result_distribution.py
#Author: ShiFY
#Mail: shify@mail.cbi.pku.edu.cn  
#Created Time: 2019-08-13 09:27:06
############################  

import pandas as pd
import seaborn as sns, numpy as np
import matplotlib
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
matplotlib.pyplot.switch_backend('agg')


fig,ax = plt.subplots()

eur = pd.read_csv("./FigS7/04-01-European-result.txt",header=None)
han = pd.read_csv("./FigS7/04-02-Han-result.txt",header=None)
afi = pd.read_csv("./FigS7/04-03-African-result.txt",header=None)

all_data = pd.concat([eur,han,afi],axis=0)
all_data_filter = all_data.loc[all_data.iloc[:,18] < 0.005,:]
all_data_filter.loc[:,20] = all_data_filter.iloc[:,19] - all_data_filter.iloc[:,18]
all_data_filter_score = all_data_filter.dropna(axis=0,how='any')
sig_num = pd.unique(all_data_filter_score.loc[all_data_filter_score.iloc[:,20] > 0.005,2]).shape[0] #45.33%
sig_num_2 = pd.unique(all_data_filter_score.loc[all_data_filter_score.iloc[:,20] > 0.15,2]).shape[0] #6.65%
all_num = pd.unique(all_data.iloc[:,2]).shape[0]
rate1 = float(sig_num)/all_num
rate2 = float(sig_num_2)/all_num

all_data_filter_score = all_data_filter.iloc[:,19] - all_data_filter.iloc[:,18]
all_data_filter_score = all_data_filter_score.dropna(axis=0,how='any')
#all_data_filter_score = 10 * np.log10(all_data_filter_score + 0.005)

#plt.axes().yaxis.set_tick_params(which='minor', right = 'off')
#plt.axes().yaxis.set_tick_params(which='minor', left = 'off')
#ax.hist(all_data_filter_score, 200, facecolor='orange', alpha=0.75)
#plt.yscale('log', nonposy='clip')
#plt.xlim(-50, 0)

ax.grid(False)
ax.spines['top'].set_visible(False) # Do not have the spines of right
ax.spines['right'].set_visible(False)
ax.tick_params(top='off',bottom='on',left='on',right='off') # Do not have the scale of the right and top.
ax.spines['bottom'].set_linewidth(1)
ax.spines['left'].set_linewidth(1)
ax.hist(all_data_filter_score, 200, facecolor='orange', edgecolor='gray', linewidth = 0.2, alpha=0.75)
ax.set_yscale('log', nonposy='clip')
ax.tick_params(axis='y', which='minor', right=False)
ax.tick_params(axis='y', which='minor', left=False)
ax.spines['left'].set_position(('data',0))
plt.xlabel("Difference in CARMEN Score between High-Linkage SNPs and Lead SNPs")
plt.ylabel("Log of the Number of SNPs")





"""
plt.annotate('45.33%', 
         xy=(0.005,0.01), xytext=(50,320), 
         textcoords='offset points', ha='center', va='top',
         arrowprops=dict(arrowstyle='<-',color='red',connectionstyle="angle,angleA=0,angleB=90,rad=1"))

plt.annotate('6.65%',
         xy=(0.15,0.01), xytext=(60,220),
         textcoords='offset points', ha='center', va='top',
         arrowprops=dict(arrowstyle='<-',color='blue',connectionstyle="angle,angleA=0,angleB=90,rad=1"))
"""

pp = PdfPages('./FigS7/04-histogram.pdf')
pp.savefig(fig)
pp.close()


