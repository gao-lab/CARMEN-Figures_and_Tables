#!/bin/bash  
#-*- coding:utf-8 -*-  
############################  
#File Name: 05_predict_not_ld_pos.sh
#Author: ShiFY
#Mail: shify@mail.cbi.pku.edu.cn  
#Created Time: 2018-12-06 19:33:59
############################  
less ./LD/GTEx-v7-CEU-LD-pos.csv | cut -f 2 > case_list 
less ./LD/CEU-LD-pairs-point75 | cut -d ',' -f 2-6 | sort | uniq > ./LD/CEU-LD-pairs-point75-uniq
cat case_list | while read s
do

LD_info_num=`grep ${s} ./LD/CEU-LD-pairs-point75-uniq | cut -d ',' -f 3-6 | wc -l`
if [ ${LD_info_num} -gt 1 ]
then
    for i in {1,${LD_info_num}}
        do
        LD_info=`grep -w ${s} ./LD/CEU-LD-pairs-point75-uniq | cut -d ',' -f 3-6 | head -n ${i} | tail -n 1`
        LD_id=`echo ${LD_info} | cut -d ',' -f 2`
        var_id=`grep -w ${LD_id} Result_sig_pre_not_variants_1KG.vcf | awk '{print $1"_"$2"_"$4"_"$5"_b37"}' | head -n 1`
        var_info=`grep -w "${var_id}" Result_sig_pre_not.csv | head -n 1`
        var_ld_pos=`grep -w "${s}" ./LD/infile.annotation.CARMEN.predict.csv | head -n 1 | cut -d ',' -f 5- `
        echo ${LD_info},${var_info},${var_ld_pos}
        done
else
    LD_info=`grep -w ${s} ./LD/CEU-LD-pairs-point75-uniq | cut -d ',' -f 3-6`
    LD_id=`echo ${LD_info} | cut -d ',' -f 2`
    var_id=`grep -w ${LD_id} Result_sig_pre_not_variants_1KG.vcf | awk '{print $1"_"$2"_"$4"_"$5"_b37"}' | head -n 1`
    var_info=`grep -w "${var_id}" Result_sig_pre_not.csv | head -n 1`
    var_ld_pos=`grep -w "${s}" ./LD/infile.annotation.CARMEN.predict.csv | head -n 1 | cut -d ',' -f 5- `
    echo ${LD_info},${var_info},${var_ld_pos}

fi
done
