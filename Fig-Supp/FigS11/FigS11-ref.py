import os
import sys
import seaborn
import matplotlib.pyplot as plt
plt.style.use('seaborn-ticks')
from matplotlib import transforms
import matplotlib.patheffects
from matplotlib.font_manager import FontProperties
import matplotlib as mpl
from scipy import interp
from itertools import cycle
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

matplotlib.pyplot.switch_backend('agg')
import numpy as np

from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler(feature_range=(0.1, 2))

#================alt===============================

require_name = sys.argv[1]
start_use = int(require_name.split("_")[1])-1
start_end =  int(require_name.split("_")[2])

ref_seq = "AGTAAGGTGGCCCGTGGAGTTCCTCTCTAACACTTCCTCTGTTCCTGGGACCTCTTTTTTTCCAAACCAGCCCTCTCTGAAAACGTCAACAGAGGACATTCATTGTCTCATTCCCCAGTTCTACACCAAGTTAAATACAGCAACACTGTGACCCTAATGACAGCCAGGAGATTTTCAAAGGAGTCAGGAGAAAACTCCAG"
#alt_seq = "AGTAAGGTGGCCCGTGGAGTTCCTCTCTAACACTTCCTCTGTTCCTGGGACCTCTTTTTTTCCAAACCAGCCCTCTCTGAAAACGTCAACAGAGGACATCCATTGTCTCATTCCCCAGTTCTACACCAAGTTAAATACAGCAACACTGTGACCCTAATGACAGCCAGGAGATTTTCAAAGGAGTCAGGAGAAAACTCCAG"
#ref_seq = alt_seq

ref_seq_use = ref_seq[start_use:start_end]
ref_name = "./FigS11/rs705698-deepocean-top-result/" + require_name
ref = np.loadtxt('%s.txt' % (ref_name),dtype=float)
#ref_score = np.argmax(np.bincount(ref))
dict = {'A': 0, 'C': 1, 'G': 2,'T':3}
ref_score = ref[dict[ref_seq_use[0]],0]


ref_dif = ref - ref_score
ref_delta = ref

for  i in range(ref_dif.shape[0]):
	for j in range(ref_dif.shape[1]):
		ref_delta[i,j] = ref_dif[i,j] * max(0,ref_score,ref[i,j])


#Then sum the ref_delta with columns
ref_break = -1 * np.sum(ref_delta,axis=0)

scaler.fit(ref_break.reshape(-1,1))
ref_break_scale = scaler.transform(ref_break.reshape(-1,1))

#==================Then make the used score matrix========================
ref_score_plot = []
for index_use in range(len(ref_seq_use)):
	list_tmp = []
	actual_letter = ref_seq_use[index_use]

	if actual_letter == 'A':
		list_tmp.append((actual_letter,ref_break_scale[index_use][0]))
	else:
		list_tmp.append(('A',0))

	if actual_letter == 'C':
		list_tmp.append((actual_letter,ref_break_scale[index_use][0]))
	else:
		list_tmp.append(('C',0))

	if actual_letter == 'G':
		list_tmp.append((actual_letter,ref_break_scale[index_use][0]))
	else:
		list_tmp.append(('G',0))

	if actual_letter == 'T':
		list_tmp.append((actual_letter,ref_break_scale[index_use][0]))
	else:
		list_tmp.append(('T',0))
	ref_score_plot.append(list_tmp)
	list_tmp = []	



#Now ref_delta is used to make heatmap


fin,ax0 = plt.subplots(figsize=(len(ref_score_plot), 3))

seaborn.heatmap(ref_delta, linewidth=0.5,center=0,cmap="RdBu_r",ax=ax0,yticklabels=['A','C','G','T'])


COLOR_SCHEME = {'G': 'orange', 
                'A': 'red', 
                'C': 'blue', 
                'T': 'darkgreen'}

BASES = list(COLOR_SCHEME.keys())


class Scale(matplotlib.patheffects.RendererBase):
    def __init__(self, sx, sy=None):
        self._sx = sx
        self._sy = sy

    def draw_path(self, renderer, gc, tpath, affine, rgbFace):
        affine = affine.identity().scale(self._sx, self._sy)+affine
        renderer.draw_path(gc, tpath, affine, rgbFace)


all_scores = ref_score_plot
fontfamily='Arial'
size = 20
if fontfamily == 'xkcd':
    plt.xkcd()
else:
    mpl.rcParams['font.family'] = fontfamily


font = FontProperties()
font.set_size(size)
font.set_weight('bold')

font.set_family(fontfamily)

ax0.set_xticks(np.arange(0.5,len(all_scores)+0.5,1))    
ax0.set_yticks(np.arange(0.5,4.5,1))
ax0.set_xticklabels(range(1,len(all_scores)+1), rotation=90)
ax0.set_yticklabels(['A','C','G','T'])    
#ax0.set_axis_off()

seaborn.despine(ax=ax0, trim=True)

trans_offset = transforms.offset_copy(ax0.transData, 
                                      fig=ax0, 
                                      x=1, 
                                      y=0, 
                                      units='dots')

for index, scores in enumerate(all_scores):
    yshift = 0
    for base, score in scores:
        if score == 0:
            continue
        else:
            txt = ax0.text(index+0.5, -0.2, base, transform=trans_offset, fontsize=25, color=COLOR_SCHEME[base], ha='center', fontproperties=font)

            txt.set_path_effects([Scale(1.0, score)])
            fin.canvas.draw()
            window_ext = txt.get_window_extent(txt._renderer)
            yshift = window_ext.height*score
            trans_offset = transforms.offset_copy(txt._transform, 
                                              fig=fin,
                                              y=yshift,
                                              units='points')
        trans_offset = transforms.offset_copy(ax0.transData, 
                                          fig=fin, 
                                          x=1, 
                                          y=0, 
                                          units='points')    
plt.show()



ax0.spines['right'].set_visible(False)
ax0.spines['top'].set_visible(False)
ax0.spines['bottom'].set_visible(False)
ax0.spines['left'].set_visible(False)

pp = PdfPages('%s-logo-heat.pdf' % (ref_name))
pp.savefig(fin)
pp.close()


