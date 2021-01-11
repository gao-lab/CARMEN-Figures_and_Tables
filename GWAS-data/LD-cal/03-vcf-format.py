import numpy as np
import pandas as pd
import os
import sys

datafile = sys.argv[1]

f = open(datafile,'r')
final_list = []

for line in f:
    eline = line.strip()
    line_list = eline.split(',')
    if len(line_list) == 6:
        final_list.append(line_list)
    else:
        continue
f.close()

final_form = pd.DataFrame(final_list)
final_form.to_csv(datafile.replace('.txt','.formated.txt'),index=False,columns=None,header=False)
final_form.ix[:,5].to_csv(datafile.replace('.txt','.rsid.txt'),index=False,header=False)
