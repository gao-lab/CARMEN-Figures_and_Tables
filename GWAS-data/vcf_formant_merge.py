import numpy as np
import pandas as pd
import h5py
import os
import sys
import re

#=================================Training file with label===========================
datafile = sys.argv[1]

f = open(datafile,'r')
final_list = []

for line in f:
    eline = line.strip()
    line_list = eline.split('\t')
    chr=line_list[0]
    pos=line_list[1]
    rs_id = line_list[2]
    ref = line_list[3]
    alt = line_list[4]
    alt_split = re.split(",",alt)
    if len(alt_split) == 1:
        print chr+'\t'+pos+'\t'+rs_id+'\t'+ref+'\t'+alt+'\t'+"."
    else:
        for i in range(len(alt_split)):
            print chr+'\t'+pos+'\t'+rs_id+'\t'+ref+'\t'+alt_split[i]+'\t'+"."
f.close()
