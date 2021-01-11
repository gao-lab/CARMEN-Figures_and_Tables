#!/bin/bash


less GTEx-v7-CARMEN.predict.csv | sed '1d' | tr ',' '\t' | awk '{print $3"_"$2"_"$6"_"$7"_b37",$9,$10}' | sed 's/chr//g' | tr ' ' '\t' > CARMAN.Predict.csv

less GTEx_Analysis_v7_RE2_id_all.txt | sed '1d' > GTEx_v7_info.csv

Rscript 03_merged_all_result.R CARMAN.Predict.csv GTEx_v7_info.csv



