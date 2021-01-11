# This script is used to draw the heatmap of the wet experiments validated variants

library(ggplot2)
library(reshape2)

#================Load input data ======================
data <- read.table("./Fig2candd/Wet-Curated-add-PNAS-new.txt",stringsAsFactors = F,header = T)
colnames(data) <- c("rs_id","CARMEN","CADD","DeepSEA","Eigen","Eigen-PC","FunSeq2","GWAVA-Region","GWAVA-TSS","GWAVA-Unmatch","EnsembleExpr","ExPecto","ncER","DeepFIGV-Dnase","DeepFIGV-H3K27AC","DeepFIGV-H3K4ME1","DeepFIGV-H3K4ME3")
infilep <- melt(data, id.var="rs_id")

infilep[infilep$value == 1,]$value <- "emVar"
infilep[infilep$value == 0,]$value <- "Non-emVar"
infilep[infilep$value == "NP",]$value <- "NA"

infilep$value <- factor(infilep$value,levels=c("emVar","Non-emVar","NA"))
infilep$rs_id <- factor(infilep$rs_id,levels=rev(c("rs12740374","chr1:155271252","rs1800734","rs2286798","rs2595104","chr6:32085776","rs12192087","rs339331","rs4730222","chr10:127505262","rs1421085","rs56069439","rs200996365","chrX:55054634","rs10772119","rs3176792","rs883868","rs1563351","rs4684847","rs6976","rs11745630","rs80095766","rs4784227","rs10772120")))

ggplot(infilep, aes(variable, rs_id)) +
  geom_tile(aes(fill = value),colour="white")+
  theme_classic() + 
  theme(axis.ticks = element_blank(),
        axis.line = element_blank())+
  scale_fill_manual(values=c( "darkorange","bisque","gray"))+
  guides(fill = guide_legend(title = "Prediction"))+
  theme(panel.border= element_blank())+
  theme(axis.text.x=element_text(size=10,angle=45,hjust = 1,color="black"))+
  theme(axis.text.y=element_text(size=10,color="black"))+
#  scale_x_discrete(position = "top")+
  xlab("")+
  ylab("")

ggsave("./Fig2candd/Wet-Curated.pdf", width = 18, height = 13, units = "cm")

#===================Load Luciferase data=====================

data_l <- read.table("./Fig2candd/Wet-Curated-luciferase-new.txt",stringsAsFactors = F,header = T)
colnames(data_l) <- c("rs_id","p-value(Luciferase)","CARMEN","CADD","DeepSEA","Eigen","Eigen-PC","FunSeq2","GWAVA-Region","GWAVA-TSS","GWAVA-Unmatch","EnsembleExpr","ExPecto","ncER","DeepFIGV-Dnase","DeepFIGV-H3K27AC","DeepFIGV-H3K4ME1","DeepFIGV-H3K4ME3")
id <- rev(rownames(data_l))
data_l <- cbind(id,data_l)

infilep <- melt(data_l, id.var=c("id","rs_id","p-value(Luciferase)"))

infilep[infilep$value == 1,]$value <- "emVar"
infilep[infilep$value == 0,]$value <- "Non-emVar"
infilep[infilep$value == "NP",]$value <- "NA"

infilep$value <- factor(infilep$value,levels=c("emVar","Non-emVar","NA"))
#level of rsid use bash "less Wet-Curated-luciferase-CNA.txt | cut -f 1 | sed '1d' | sed 's/^/"/g' | sed 's/$/"/g' | tr '\n' ',' | less"
#infilep$rs_id <- factor(infilep$rs_id,levels=rev(c("rs10030238","rs1044503","rs4904569","rs3734637","rs11119843","rs1451509","rs17779853","rs6565060","rs1275988","rs196067","rs2305054","rs11263841","rs10089107","rs7783216")))
infilep$id <- as.numeric(as.character(infilep$id))


ggplot(infilep, aes(variable, id)) +
  geom_tile(aes(fill = value),colour="white")+
  theme_classic() + #去掉灰快 
  theme(axis.ticks = element_blank(),
        axis.line = element_blank()) + #去掉边框
  scale_fill_manual(values=c( "darkorange","bisque","gray"))+
  guides(fill = guide_legend(title = "Prediction"))+
  theme(panel.border= element_blank())+
  theme(axis.text.x=element_text(size=10,angle=45,hjust = 1,vjust = 1.2,color="black"))+
  theme(axis.text.y=element_text(size=10,color="black"))+
  xlab("")+
  ylab("")+
  scale_y_continuous(breaks = 14:1,
                     labels = data_l$rs_id,
                     sec.axis = dup_axis(name = "p-value(Luciferase)",labels = data_l$`p-value(Luciferase)`))+
  geom_hline(aes(yintercept=4.5), colour="black", linetype="dashed")
ggsave("./Fig2candd/Wet-Curated-luciferase.pdf", width = 20, height = 13, units = "cm")
