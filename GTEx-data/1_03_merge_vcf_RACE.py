#!/usr/bin/python  
#-*- coding:utf-8 -*-  
############################  
#File Name: 03_merge_vcf_RACE.py
#Author: ShiFY
#Mail: shify@mail.cbi.pku.edu.cn  
#Created Time: 2018-12-02 19:48:55
############################  
import pandas as pd
import numpy as np

data = pd.read_table('./phg000830.v1.GTEx_WGS.genotype-calls-vcf.c1/vcf_title_race.txt',header=None,sep='\t')

f = open('Result_sig_pre_not_variants_ID.txt','r')

for line in f:
    input_list = line.strip()
    input_use = np.array(input_list.split(',')[0:(len(input_list.split(','))-1)],dtype=int) - 10
    input_out = data.ix[input_use,1].unique()
    print input_out
f.close()

