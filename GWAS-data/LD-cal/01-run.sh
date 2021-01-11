#!/bin/bash  
#-*- coding:utf-8 -*-  
############################  
#File Name: run_01.sh
#Author: ShiFY
#Mail: shify@mail.cbi.pku.edu.cn  
#Created Time: 2018-11-13 21:09:18
############################  
for num in {10000..50000..10000}
do
echo ${num}
ipython 02_vcf_file_LD_calculate.py ${num}
sleep 10

done
