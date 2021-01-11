library(ggplot2)
infile <- read.table("time-cost-single-core-sameCPUspeed-compare.txt",sep='\t',stringsAsFactors = F, header = T)
colnames(infile) <- c("Algorithms","Time")
infile$Method <- factor(infile$Algorithms,levels=c("DeepSEA","CARMEN","EnsembleExpr","ExPecto"))


ggplot(data=infile, aes(x=Algorithms, y=Time)) +
  geom_bar(stat="identity", fill="orange", color="black", width=0.4)+
  theme_bw()+
  theme(panel.grid.major=element_blank(),panel.grid.minor=element_blank())+
  theme(panel.grid =element_blank()) +
  theme(panel.border= element_blank()) +
  theme(axis.line= element_line(size=0.5, colour ="black"))+
  scale_y_continuous(expand = c(0, 0))+
  theme(axis.text.y=element_text(size = 7,color = "black"))+
  theme(axis.text.x=element_text(size = 7,color = "black"))+
  theme(axis.title.x = element_text(size = 7))+
  theme(axis.title.y = element_text(size = 7))+
  xlab("Algorithms")+
  ylab("Time (hours/single core)")


ggsave("Time-compare.pdf", width = 8.5, height = 6, units = "cm")

