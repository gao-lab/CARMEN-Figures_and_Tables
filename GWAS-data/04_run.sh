#!/bin/bash  
#-*- coding:utf-8 -*-  
############################  
#File Name: 04_run.sh
#Author: ShiFY
#Mail: shify@mail.cbi.pku.edu.cn  
#Created Time: 2019-09-25 20:19:47
############################  
for data_path in {CEU,CHB,KHV,PUR,TSI,YRI}

do

Rscript 04_merged_all_result.R ./GWASLD/${data_path}/ ./GWASLD/${data_path}/infile.annotation.689.CARMAN.predict.unmatch.csv ./GWASLD/info/${data_path}-LD-point75.formated.txt ./GWASLD/info/GWAS-catalogue-result.csv

done
