library(ggplot2)
infile <- read.table("./Fig2b/WXY_compare_sensitivity_sort.txt",sep=' ',stringsAsFactors = F, header = T)
df <- data.frame(cbind(infile[,2],infile[,1]))
colnames(df) <- c("Method","Recall")
df$Method <- factor(df$Method,levels=c('ExPecto','FunSeq2','GWAVA-Region','DeepSEA','CADD','GWAVA-TSS','GWAVA-Unmatch','Eigen','EnembleExpr','Eigen-PC','DeepFIGV-H3K4ME1','DeepFIGV-H3K27AC','DeepFIGV-DNase','DeepFIGV-H3K4ME3','ncER','CARMEN'))

df$Recall <- as.numeric(as.character(df$Recall))

ggplot(data=df, aes(x=Method, y=Recall)) +
  geom_bar(stat="identity", fill="white", color="black", width=0.7)+
  theme_bw()+
  theme(panel.grid.major=element_blank(),panel.grid.minor=element_blank())+
  theme(panel.grid =element_blank()) +
  theme(panel.border= element_blank()) +
  theme(axis.line= element_line(size=0.5, colour ="black"))+
  scale_y_continuous(limits = c(0, 1),expand = c(0, 0))+
  theme(axis.text.y=element_text(size = 7,color = "black"))+
  theme(axis.text.x=element_text(size = 7,color = "black"))+
  theme(axis.title.x = element_text(size = 7))+
  theme(axis.title.y = element_text(size = 7))+
  xlab("")+
  coord_flip()


ggsave("./Fig2b/WXY-Recall-compare.pdf", width = 8.5, height = 6, units = "cm")



