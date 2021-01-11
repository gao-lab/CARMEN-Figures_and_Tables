#!/usr/bin/python  
#-*- coding:utf-8 -*-  
############################  
#File Name: 01_vcf_file_LD_calculate.py
#Author: ShiFY
#Mail: shify@mail.cbi.pku.edu.cn  
#Created Time: 2018-11-12 14:46:57
############################ 
import pandas as pd
import requests, sys
import json
from pandas.io.json import json_normalize
import multiprocessing

# Change the population with "CEU","CHB","KHV","PUR","TSI","YRI" each time.
population = "CEU"
index_number = int(sys.argv[1])

input_vcf = pd.read_table('GWAS-2018-vcftools-GRCh37.vcf',header=None)
vcf_id = input_vcf.ix[:,2]

def LD_score(rs_id):
    server = "https://rest.ensembl.org"
    ext = "/ld/human/"+str(rs_id)+"/1000GENOMES:phase_3:"+str(population)+"?r2=0.75;window_size=500"
    r = requests.get(server+ext, headers={ "Content-Type" : "application/json"})

    if r.ok:
        decoded = r.json()
        if decoded:
            decoded_out = json_normalize(decoded)
            decoded_out.to_csv(str(population)+'-LD-pairs-point75-'+str(index_number), mode='a', header=False)


if index_number > 40000:
    pool = multiprocessing.Pool(30)
    pool.map(LD_score,vcf_id.ix[index_number-10000:])
else:
    pool = multiprocessing.Pool(30)
    pool.map(LD_score,vcf_id.ix[index_number-10000:index_number])
