#!/bin/bash  
#-*- coding:utf-8 -*-  
############################  
#File Name: run_01.sh
#Author: ShiFY
#Mail: shify@mail.cbi.pku.edu.cn  
#Created Time: 2018-11-13 21:09:18
############################  
for pop in {"CEU","CHB","KHV","PUR","TSI","YRI"}
do
	for num in {10000..50000..10000}
	do
	cat ${pop}-LD-pairs-point75-${num} >> ${pop}-LD-point75.txt 
	done
done
