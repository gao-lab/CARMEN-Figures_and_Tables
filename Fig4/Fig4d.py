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

#========================Load data and merge===========================================
data = pd.read_table("./Fig4a-d/luciferase-case2.txt")
data.columns = ["Lead-Ref","Lead-Alt","Predicted-Ref","Predicted-Alt"]
#======================Make plot========================================================

fig,ax = plt.subplots(figsize=(3.8,2.91))
f = data.boxplot(vert = True,patch_artist = True,notch = False,return_type = 'dict')

colors = ['blue', 'blue', 'orange', 'orange']
for patch, color in zip(f['boxes'], colors):
	patch.set( color='black', linewidth=1)
	patch.set(facecolor=color)

for whisker in f['whiskers']:
    whisker.set(color='black', linewidth=1,linestyle='-')
for cap in f['caps']:
    cap.set(color='black', linewidth=1)
for median in f['medians']:
    median.set(color='black', linewidth=1)
for flier in f['fliers']:
    flier.set(marker='o', color='black', alpha=1)

ax.set_ylim(0,2.5000000000001)	

ax.annotate("ns",(1.3,0.2),fontsize=10)	
ax.annotate("****",(3.3,1.9),fontsize=10)
ax.annotate("p = 7.8e-09",(3.0,2.1),fontsize=10)
ax.annotate("rs1727313",(1.0,0.4),fontsize=10)
ax.annotate("rs146239222",(3.0,2.3),fontsize=10)



ax.grid(False)
ax.spines['top'].set_visible(False) # Do not have the spines of right
ax.spines['right'].set_visible(False)
ax.tick_params(top='off',bottom='on',left='on',right='off') # Do not have the scale of the right and top.
ax.spines['bottom'].set_linewidth(1)
ax.spines['left'].set_linewidth(1)
ax.set_xticklabels(["Reference allele","Alternative allele","Reference allele","Alternative allele"], fontsize=6)
ax.set_ylabel('Luciferase activity', fontsize = 10)
plt.tight_layout()		
#plt.xticks(rotation=45,ha='right')
plt.xticks(fontsize=6)

pp = PdfPages('./Fig3a-d/CASE2-luciferase.pdf')
pp.savefig(fig)
pp.close()

