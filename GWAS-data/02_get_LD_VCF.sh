#!/bin/bash
#with gatk-4.0.11.0 

for pop in {CEU,CHB,KHV,PUR,TSI,YRI}
do
gatk --java-options "-Xmx8G" SelectVariants \
        -V ../GTEx-data/ALL.wgs.phase3_shapeit2_mvncall_integrated_v5b.20130502.sites.vcf.gz \
        -O ${pop}-LD-point75.rsid.gatk.vcf\
        --keep-ids ${pop}-LD-point75.rsid.list 
done


