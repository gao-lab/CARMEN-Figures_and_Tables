#!/bin/bash  
#-*- coding:utf-8 -*-  
############################  
#File Name: 03_format_vcf_to_use.sh
#Author: ShiFY
#Mail: shify@mail.cbi.pku.edu.cn  
#Created Time: 2018-11-21 16:02:49
############################  
for pop in {CEU,CHB,KHV,PUR,TSI,YRI}
do
grep -v '#' ${pop}-LD-point75.rsid.gatk.vcf | awk '{print $1,$2,$3,$4,$5,"."}' | tr ' ' '\t' > tmp
ipython vcf_formant_merge.py tmp >> ${pop}_use.vcf
done
rm -f tmp
