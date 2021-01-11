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

require_name = "./Fig3candd/" + sys.argv[1]

#require_name = "GM12878"
start_use = int(94)
start_end =  int(107)

ref_seq = "GAGGACACAGACACACACAGAGGGACAGCCTGTGAGGAAACGAGGAGAAGTACCTGTCTACAAGCCAAGGAGAGAGGCCTCAAGAGAGACCAGCCTCAATGGTGGCTTGACCTCAGACTCGCAGCCTCCAGGACTATGAGGGCATCTGTGGCTGTCGTTGAAGCCGCTCAGCTGTGGGACTTTGTTATGGCCGCCCCAGG"
alt_seq = "GAGGACACAGACACACACAGAGGGACAGCCTGTGAGGAAACGAGGAGAAGTACCTGTCTACAAGCCAAGGAGAGAGGCCTCAAGAGAGACCAGCCTCAACGGTGGCTTGACCTCAGACTCGCAGCCTCCAGGACTATGAGGGCATCTGTGGCTGTCGTTGAAGCCGCTCAGCTGTGGGACTTTGTTATGGCCGCCCCAGG"


def get_plot_matrix(seq_in,name_in):
	seq_use = seq_in[start_use:start_end]
	name_use =  name_in
	original_matrix = np.loadtxt(name_use,dtype=float)
	#ref_score = np.argmax(np.bincount(ref))
	dict_letter = {'A': 0, 'C': 1, 'G': 2,'T':3}
	original_score = original_matrix[dict_letter[seq_use[0]],0]


	dff_matrix = original_matrix - original_score
	delta_matrix = original_matrix

	for  i in range(dff_matrix.shape[0]):
		for j in range(dff_matrix.shape[1]):
			delta_matrix[i,j] = dff_matrix[i,j] * max(0,original_score,original_matrix[i,j])

	return(delta_matrix)
#Then sum the ref_delta with columns
ref_delta_matrix = get_plot_matrix(ref_seq,require_name+"-ref.txt")

alt_delta_matrix = get_plot_matrix(alt_seq,require_name+"-alt.txt")


ref_for_logo = -1 * np.sum(ref_delta_matrix,axis=0)
ref_seq_logo = ref_seq[start_use:start_end]
alt_for_logo = -1 * np.sum(alt_delta_matrix,axis=0)
alt_seq_logo = alt_seq[start_use:start_end]


# Logo scale
logo_scaler = MinMaxScaler(feature_range=(0.1, 2))

logo_scaler.fit(ref_for_logo.reshape(-1,1))
ref_logo_scale = logo_scaler.transform(ref_for_logo.reshape(-1,1))

logo_scaler.fit(alt_for_logo.reshape(-1,1))
alt_logo_scale = logo_scaler.transform(alt_for_logo.reshape(-1,1))


#==================Then make the used score matrix========================
def makeplot_function(seq_use,ref_break_scale,norm_matrix,type_query):
	ref_score_plot = []
	for index_use in range(len(seq_use)):
		list_tmp = []
		actual_letter = seq_use[index_use]
	
		if actual_letter == 'A':
			list_tmp.append((actual_letter,ref_break_scale[index_use]))
		else:
			list_tmp.append(('A',0))
	
		if actual_letter == 'C':
			list_tmp.append((actual_letter,ref_break_scale[index_use]))
		else:
			list_tmp.append(('C',0))
	
		if actual_letter == 'G':
			list_tmp.append((actual_letter,ref_break_scale[index_use]))
		else:
			list_tmp.append(('G',0))
	
		if actual_letter == 'T':
			list_tmp.append((actual_letter,ref_break_scale[index_use]))
		else:
			list_tmp.append(('T',0))
		ref_score_plot.append(list_tmp)
		list_tmp = []	
	
	
	
	#Now ref_delta is used to make heatmap
	
	
	fin,ax0 = plt.subplots(figsize=(len(ref_score_plot), 3))
	#heatmap
	seaborn.heatmap(norm_matrix, linewidth=0.5,center=0,cmap="RdBu_r",ax=ax0,yticklabels=['A','C','G','T'])
	
	#SeqLogo
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
	size = 30
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
	            txt = ax0.text(index+0.5, -0.2, base, transform=trans_offset, fontsize=30, color=COLOR_SCHEME[base], ha='center', fontproperties=font)
	
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
	
	
	pp = PdfPages('%s-logo-heat.pdf' % (require_name+type_query))
	pp.savefig(fin)
	pp.close()
	

makeplot_function(ref_seq_logo,ref_logo_scale,ref_delta_matrix,"ref")
makeplot_function(alt_seq_logo,alt_logo_scale,alt_delta_matrix,"alt")
