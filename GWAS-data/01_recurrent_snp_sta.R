library(reshape2)
gwas_recurrent_id <- read.table("recurrent_snp.txt",header = F,stringsAsFactors = F)

gwas_all <- read.csv("GWAS.2018-08-28.CARMAN.predict.csv")

gwas_all$PM <- gwas_all$Prob*gwas_all$UnmatchProb
gwas_recurrent_predict <- gwas_all[gwas_all$rs_id %in% gwas_recurrent_id[,1],]$Prob
gwas_irecurrent_predict <- gwas_all[!(gwas_all$rs_id %in% gwas_recurrent_id[,1]),]$Prob
gwas_test <- cbind(((gwas_all$rs_id %in% gwas_recurrent_id[,1])+0),gwas_all$Prob,gwas_all$UnmatchProb,gwas_all$Prob*gwas_all$UnmatchProb)
colnames(gwas_test) <- c('Recurrent_label','CARMEN-E','CARMEN-F','CARMEN')
gwas_test_plot <- melt(as.data.frame(gwas_test),id.vars = 'Recurrent_label')
gwas_test <- as.data.frame(gwas_test)

sta_result <- wilcox.test(gwas_test[gwas_test$Recurrent_label == '0',]$CARMEN,gwas_test[gwas_test$Recurrent_label == '1',]$CARMEN,alternative="less")

