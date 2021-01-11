#!/bin/bash  
#-*- coding:utf-8 -*-  
############################  
#File Name: 01-run-recurrent.sh
#Author: ShiFY
#Mail: shify@mail.cbi.pku.edu.cn  
#Created Time: 2019-09-25 19:34:06
############################  
less gwas_catalog_v1.0.2-associations_e93_r2018-08-28.tsv | cut -f 2,22 | sed '1d' | sort -k2 | grep 'rs' | uniq | cut -f 2 | uniq -c | sort -k1rn | awk '{ if ($1 > 1) print $2}' > recurrent_snp.txt

