rm(list=ls())

#====================================================================
#This script is used to analysis the result of CARMEN predict GTEx

#====================================================================
library("data.table")

#====================Load file and add CARMENEF======================
result.dt <- fread("all_result_use.csv")
result.dt[,`:=`(CARMENEF = result.dt[,Prob]*result.dt[,UnmatchProb]/(result.dt[,Prob]*result.dt[,UnmatchProb]+(1-result.dt[,Prob])*(1-result.dt[,UnmatchProb])))]

#===========================Filter coding variants in GTEx===============================
result.split.dt <- fread("all_result_use_split_ID.csv",header = FALSE)
setnames(result.split.dt, c("ID","Chr","Pos","Ref","Alt","Version","Gene","RE2Pvalue","Prob","UnmatchProb"))
require('TxDb.Hsapiens.UCSC.hg19.knownGene')
library(VariantAnnotation)
input <- GRanges( seqnames = Rle(paste("chr",result.split.dt$Chr,sep="")),
                  ranges   = IRanges(result.split.dt$Pos, end=result.split.dt$Pos),
                  strand   = Rle(strand("*")) )
loc <- locateVariants(input, TxDb.Hsapiens.UCSC.hg19.knownGene, CodingVariants())

result.split.filter.dt <- result.split.dt[is.na(match(paste(paste("chr",as.character(result.split.dt$Chr),sep=""),result.split.dt$Pos),
                   unique(paste(space(as(loc,"RangedData")),start(loc))))),]


result.split.filter.dt[,`:=`(CARMENEF = result.split.filter.dt[,Prob]*result.split.filter.dt[,UnmatchProb]/(result.split.filter.dt[,Prob]*result.split.filter.dt[,UnmatchProb] + (1-result.split.filter.dt[,Prob])*(1-result.split.filter.dt[,UnmatchProb])))]

#====================Get RE2 minimal variant as the significant variant of each gene.
result_sig.dt <- result.split.filter.dt[ , .SD[which.min(RE2Pvalue)], by = Gene]
result_notsig.dt <- result.split.filter.dt[!(result.split.filter.dt[,ID] %in% result_sig.dt[,ID]),]
result_notsig_ob.dt <- result_notsig.dt[RE2Pvalue>0.1]

d1 <- dim(result_sig.dt[CARMENEF > 0.005])[1]
d2 <- dim(result_sig.dt[CARMENEF <= 0.005])[1]
d3 <- dim(result_notsig.dt[CARMENEF > 0.005])[1]
d4 <- dim(result_notsig.dt[CARMENEF <= 0.005])[1]

tableR <- matrix(c(d1,d2,d3,d4),nrow = 2,ncol = 2)
z <- chisq.test(tableR)

result_notsig_ob_filter.dt <- result_notsig_ob.dt[which(result_notsig_ob.dt[,c('Prob')] > 0.5 & result_notsig_ob.dt[,c('UnmatchProb')] > 0.005)]
result_sig_pre_not <- result_sig.dt[CARMENEF <= 0.005]
result_sig_pre_not_cut <- result_sig_pre_not[which(result_sig_pre_not[,c('Prob')] < 0.5 & result_sig_pre_not[,c('UnmatchProb')] < 0.005)]
colnames(result_sig_pre_not_cut) <- c("Gene","ID","Chr","Pos","Ref","Alt","Version","RE2Pvalue","CARMEN-E","CARMEN-F","CARMEN")
fwrite(result_sig_pre_not_cut, "Result_sig_pre_not.csv")

