library("data.table")

args <- commandArgs(trailingOnly = TRUE)

result.dt <- fread(args[1], sep="\t", header=FALSE)
info.dt <- fread(args[2], sep="\t", header=FALSE)
setnames(result.dt, c("ID","Prob","UnmatchProb"))
setnames(info.dt, c("ID","Gene","RE2Pvalue"))
         
setkey(result.dt,"ID")
setkey(info.dt,"ID")
info_result1.dt <- info.dt[result.dt,nomatch=NA,mult="all"]

fwrite(info_result1.dt,"all_result_use.csv")


