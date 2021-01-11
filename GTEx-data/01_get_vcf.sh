#!/bin/bash  
#-*- coding:utf-8 -*-  
############################  
#File Name: 01_get_vcf.sh
#Author: ShiFY
#Mail: shify@mail.cbi.pku.edu.cn  
#Created Time: 2019-09-25 18:34:04
############################  
less GTEx_Analysis_v7.metasoft.txt | awk '{if ($9 < 0.01) print $1}' | cut -d ',' -f 1 >> GTEx_Analysis_v7_RE2_sig_id.txt
less GTEx_Analysis_v7_RE2_sig_id.txt | sort | uniq | tr '_' '\t' | awk '{print $1,$2,".",$3,$4,"."}'| tr ' ' '\t' > GTEx_Analysis_v7_RE2_sig.vcf

less GTEx_Analysis_v7.metasoft.txt | awk '{print $1,$9}' | tr ',' ' ' | cut -f 1,3 | tr ' ' '\t' >> GTEx_Analysis_v7_RE2_id_all.txt
less GTEx_Analysis_v7_RE2_id_all.txt | sed '1d'| cut -f 1 | sort | uniq | tr '_' '\t' | awk '{print $1,$2,".",$3,$4,"."}'| tr ' ' '\t' > GTEx_Analysis_v7_RE2_all.vcf

#Run CARMEN with GTEx_Analysis_v7_RE2_all.vcf
