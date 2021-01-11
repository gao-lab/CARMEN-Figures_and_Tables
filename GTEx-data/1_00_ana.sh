#!/bin/bash  
#-*- coding:utf-8 -*-  
############################  
#File Name: 00_ana.sh
#Author: ShiFY
#Mail: shify@mail.cbi.pku.edu.cn  
#Created Time: 2018-12-31 14:28:28
############################  
less all_result_use.csv | sed '1d' | tr '_' ',' > all_result_use_split.csv
less all_result_use.csv | sed '1d' | cut -d ',' -f 1 > tmp
paste -d ',' tmp all_result_use_split.csv > all_result_use_split_ID.csv
rm -f tmp
