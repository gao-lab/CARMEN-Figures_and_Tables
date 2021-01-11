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

matplotlib.font_manager._rebuild()
rcParams['font.size'] = 4
rcParams['font.family'] = "Arial"

sns.set(style = "whitegrid")


data = pd.read_csv('./FigS5/FigS5b.AUROC.v1.txt',sep='\t')
data.columns = ['Tools','AUROC']
data_sort = data.sort_values(by=['AUROC'])

x = data_sort.AUROC
z = data_sort.AUROC
y = range(1,17,1)
#cm = plt.cm.get_cmap('coolwarm')
#cm = sns.color_palette("hls", 18)
cm = plt.cm.jet

#fig,ax = plt.subplots(figsize = (12,12)) #make plot
fig,ax = plt.subplots(figsize = (5,4))
bubble = ax.scatter(x, y , s = x*200, c = z, cmap = cm, linewidth = 0.5, alpha = 1) #make bubble plot, the s is the size of bubble.
ax.grid()
v1 = np.linspace(z.min(), z.max(), 8, endpoint=True)
cbar = plt.colorbar(bubble,ticks=v1)
cbar.set_label('AUROC',labelpad=-20, y=1.1, rotation=0, size=10) # set the label of the legend colorbar
cbar.ax.tick_params(labelsize=10)
#cbar.ax.set_yticklabels(["{:.3%}".format(float(i)) for i in cbar.ax.get_yticklabels()])
ax.set_ylim(0,17) # To make the y axis label in the middle position
plt.yticks(y,data_sort.Tools) # Here we need use plt.yticks to match the y and label, if we use as.set_yticklabels, the label position will be wrong
ax.set_xlabel('AUROC')
#ax.set_ylabel('Tools', fontsize = 12)
ax.xaxis.set_ticks(np.arange(0.450, 0.710, 0.050))
ax.xaxis.set_tick_params(labelsize=10)
ax.yaxis.set_tick_params(labelsize=10)

ax.spines['top'].set_visible(False) # Do not have the spines of right
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_color('black')
ax.spines['left'].set_color('black')


ax.tick_params(top='off',bottom='on',left='on',right='off') # Do not have the scale of the right and top.

plt.tight_layout() #Make all information showed on the picture.
plt.show()
	
pp = PdfPages('./FigS5/BiT-compare-new-1.pdf')
pp.savefig(fig)
pp.close()
