import os
import sys
import pandas as pd
import numpy as np
import matplotlib
import matplotlib as mpl
import matplotlib.pyplot as plt
import brewer2mpl
import seaborn as sns
from sklearn import preprocessing
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib import rcParams


matplotlib.pyplot.switch_backend('agg')

sns.set(style = "whitegrid")
data = pd.read_csv('./Fig2a/WXY_compare_weighted_result_new_add.csv',sep='\t')
data_sort = data.sort_values(by=['F1score'])

x = data_sort.weighted_acc
z = data_sort.F1score

y = range(1,17,1)
cm = plt.cm.get_cmap('coolwarm')


fig,ax = plt.subplots(figsize = (6,4.5))

bubble = ax.scatter(x, y, s = 200, c = z, cmap = cm, linewidth = 0.5, alpha = 1) #make bubble plot, the s is the size of bubble.
ax.grid()
cbar = fig.colorbar(bubble)
cbar.set_label('F1 Score',labelpad=-20, y=1.1,rotation=0,size=10) # set the label of the legend colorbar
cbar.ax.tick_params(labelsize=10)
ax.xaxis.set_ticks(np.arange(0.45, 0.615, 0.03))
ax.set_ylim(0,17) # To make the y axis label in the middle position
plt.yticks(y,data_sort.Tools) # Here we need use plt.yticks to match the y and label, if we use as.set_yticklabels, the label position will be wrong
ax.set_xlabel('Weighted Accuracy',fontsize=10)
ax.xaxis.set_tick_params(labelsize=10)
ax.yaxis.set_tick_params(labelsize=10)


ax.spines['top'].set_visible(False) # Do not have the spines of right
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_color('black')
ax.spines['left'].set_color('black')

ax.tick_params(top='off',bottom='on',left='on',right='off') # Do not have the scale of the right and top.

plt.tight_layout() #Make all information showed on the picture.
plt.show()
	
pp = PdfPages('./Fig2a/WXY-compare-new.pdf')
pp.savefig(fig)
pp.close()
