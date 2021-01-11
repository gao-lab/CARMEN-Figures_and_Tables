data <- as.matrix(read.table('Result_sig_pre_not_variants_slim.vcf',sep='\t', header=F, stringsAsFactors=F))
BAA_id <- as.matrix(read.table('BAA_ID', header=F, stringsAsFactors=F))

data_out <- data[!(seq(1,dim(data)[1]) %in% BAA_id[,1]),]
write.table(data_out,'Result_sig_pre_not_variants_slim_noBAA.vcf',col.names=F,row.names=F,quote=F)
