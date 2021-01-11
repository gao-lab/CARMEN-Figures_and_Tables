library("data.table")

args <- commandArgs(trailingOnly = TRUE)
work_path <- args[1]

result.dt <- fread(args[2], sep=",", header=TRUE)
info.dt <- fread(args[3], sep=",", header=FALSE)
setnames(info.dt, c("num","d_prime","population","r2","variation1","variation2"))
         
setkey(result.dt,"rs_id")
setkey(info.dt,"variation2")
info_result1.dt <- info.dt[result.dt,nomatch=NA,mult="all"]
setkey(info_result1.dt,"variation1")

leadsnp.dt <- fread(args[4],sep=',',header = TRUE)
setkey(leadsnp.dt,"rs_id")

all_result.dt <- leadsnp.dt[info_result1.dt,nomatch=NA,mult="all",allow.cartesian=TRUE]
all_result_use <- all_result.dt[,c('V1','i.V1','Comment','num','i.Comment'):=NULL]
all_result_use[,`:=`(LeadSNPProb = all_result_use[,Prob]*all_result_use[,UnmatchProb]/(all_result_use[,Prob]*all_result_use[,UnmatchProb] + (1-all_result_use[,Prob])*(1-all_result_use[,UnmatchProb])) , TargetSNPProb = all_result_use[,i.Prob]*all_result_use[,i.UnmatchProb]/(all_result_use[,i.Prob]*all_result_use[,i.UnmatchProb] + (1-all_result_use[,i.Prob])*(1-all_result_use[,i.UnmatchProb])))]
fwrite(all_result_use, paste(work_path,"all_result_use.csv",sep=""))
case_choose <- all_result_use[which(all_result_use[,c('Prob')] < 0.5 & all_result_use[,c('UnmatchProb')] < 0.005 & all_result_use[,c('i.Prob')] > 0.5 & all_result_use[,c('i.UnmatchProb')] > 0.005)]
fwrite(case_choose, paste(work_path,"case_choose.csv",sep=""))
