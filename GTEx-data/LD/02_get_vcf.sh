#!/bin/bash  
#-*- coding:utf-8 -*-  
############################  
#File Name: 01_get_vcf.sh
#Author: ShiFY
#Mail: shify@mail.cbi.pku.edu.cn  
#Created Time: 2018-12-03 14:12:20
############################  
less CEU-LD-pairs-point75 | cut -d ',' -f 6 | sort | uniq > CEU-LD-RSID.list

vcftools --gzvcf ALL.wgs.integrated_phase1_v3.20101123.snps_indels_sv.sites.vcf.gz --snps CEU-LD-RSID.list --recode --out CEU-LD-point75.rsid.vcf

less CEU-LD-point75.rsid.vcf.recode.vcf |grep -v '#' | cut -f 1-5,8 | grep 'rs' | sed 's/^/chr/' > CEU-LD-point75.rsid.vcf

# Run CARMEN to get the infile.annotation.CARMEN.predict.csv with CEU-LD-point75.rsid.vcf

less infile.annotation.CARMEN.predict.csv | tr ',' '\t' | sed 's/chr//g' | awk '{print $3"_"$2"_"$6"_"$7"_b37",$5,$9,$10}' | sed '1d' | tr ' ' '\t' > GTEx-v7-CEU-LD.csv

less GTEx-v7-CEU-LD.csv | awk '{if ($3 > 0.5 && $4 > 0.005) print $0}' > GTEx-v7-CEU-LD-pos.csv
