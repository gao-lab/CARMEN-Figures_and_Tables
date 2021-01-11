#!/bin/bash  
#-*- coding:utf-8 -*-  
############################  
#File Name: 02_get_Result_sig_pre_not_variants_info.sh
#Author: ShiFY
#Mail: shify@mail.cbi.pku.edu.cn  
#Created Time: 2018-12-02 17:12:21
############################  


less Result_sig_pre_not.csv | sed '1d' | cut -d ',' -f 2 | tr '_' '\t' | awk '{print $1":"$2"-"$2}' > tabix_list

cat tabix_list | while read s
do
tabix ./phg000830.v1.GTEx_WGS.genotype-calls-vcf.c1/GTEx_Analysis_2016-01-15_v7_WholeGenomeSeq_652Ind_GATK_HaplotypeCaller.vcf.gz ${s} >> Result_sig_pre_not_variants.vcf
done

#Check which individual has this variant.
cat Result_sig_pre_not_variants.vcf | while read s
do
out=`echo ${s} | tr ' ' '\n' | cat -n | grep '/1' | awk '{print $1}' | tr '\n' ','`
echo ${out} >> Result_sig_pre_not_variants_ID.txt
done
#Get the race of individuals
zcat phs000424.v7.pht002742.v7.p2.c1.GTEx_Subject_Phenotypes.GRU.txt.gz | grep -v '#' | cut -f 2,6 > GTEx-race-map.txt
zcat GTEx_Analysis_2016-01-15_v7_WholeGenomeSeq_652Ind_GATK_HaplotypeCaller.vcf.gz | sed -n '210p' | tr '\t' '\n' | sed '1,9d'  > vcf_title

cat vcf_title | while read s
do
grep ${s} GTEx-race-map.txt >> vcf_title_race.txt
done


#Get the CEU significant variants predicted as negative vcf
less Result_sig_pre_not_variants.vcf | cut -f 1-5 > Result_sig_pre_not_variants_slim.vcf

ipython 1_03_merge_vcf_RACE.py >> Result_sig_pre_not_variants_ID_RACE.txt

less Result_sig_pre_not_variants_ID_RACE.txt| cat -n | grep -w '\[2\]' | awk '{print $1}' > BAA_ID

Rscript 1_04_filter_BAA_left_vcf.R 


less Result_sig_pre_not_variants_slim_noBAA.vcf | tr ' ' '\t' | awk '{print $1":"$2"-"$2}' > tabix_list_noBAA

cat tabix_list_noBAA | while read s
do
tabix ALL.wgs.phase3_shapeit2_mvncall_integrated_v5b.20130502.sites.vcf.gz ${s} >> Result_sig_pre_not_variants_1KG.vcf
done

less Result_sig_pre_not_variants_1KG_slim.vcf | cut -d ' ' -f 2 | sort | uniq > CEU_rs_id.list

#Get LD variants
cd ./LD/
bash 01-get-LD-run.sh
bash 02_get_vcf.sh

#Merge all results
cd ../
bash 1_05_predict_not_ld_pos.sh  
