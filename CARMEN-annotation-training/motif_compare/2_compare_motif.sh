#!bin/bash
# This is the script for compare motif using tomtom

#feature
feature=$1
#motif database
TRANSFAC_database=./db/TRANSFAC_2019.3_id.meme
JASPAR_database=./db/JASPAR2020_CORE_vertebrates_non-redundant_pfms_meme.txt
#out dir
transfac_out_dir=./result/transfac/$feature/
jaspar_out_dir=./result/jaspar/$feature/
#query motif
kernel_motif=./motif/$feature/kernels.meme
#compare using tomtom
tomtom -oc $transfac_out_dir $kernel_motif $TRANSFAC_database
tomtom -oc $jaspar_out_dir $kernel_motif $JASPAR_database