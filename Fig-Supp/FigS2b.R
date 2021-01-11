
"This script is used to draw the boxplot of the CARMEN annotation models performance in AUC and AUPRC"
library(ggplot2)
library(reshape2)
library(stringr)

input <- read.table("./FigS2/CARMEN-annotation-AUC-removeENCODEblacklist.txt",header = T,stringsAsFactors = F,sep='\t')
infilep <- as.data.frame(melt(input))
colnames(infilep) <- c("Assay Categories","Variable","Value")
infilep$`Assay Categories` <- factor(infilep$`Assay Categories`,levels = c("DNA Accessibility","Transcription Factor Binding","Histone Markers","Methylation Profiles"))

ggplot(infilep, aes(`Assay Categories`, Value, fill=factor(`Assay Categories`)))+
#  geom_violin( )+
  geom_boxplot()+
  theme_bw()+
  theme(panel.grid.major=element_blank(),panel.grid.minor=element_blank())+
  scale_y_continuous(limits = c(0.5,1.03),breaks=seq(0.5, 1, 0.1))+
  scale_fill_manual(values=c("tomato","tomato","tomato","tomato")) +
  xlab("Assay Categories")+
  ylab("AUROC")+
  theme(axis.text.y=element_text(size = 6,color = "black"))+
  theme(axis.text.x=element_text(size = 6,color = "black"))+
  theme(axis.title.x = element_text(size = 6))+
  theme(axis.title.y = element_text(size = 6))+
  scale_x_discrete(labels = function(x) str_wrap(x, width = 15))+
  guides(fill = guide_legend(title = ""))+
  theme(panel.border= element_blank())+
  theme(axis.line= element_line(size=0.5, colour ="black"))+
  theme(legend.position="top")+
  theme(legend.text=element_text(size=6))

ggsave("./FigS2/Annotations-AUC-boxplot-removeENCODEblacklist.pdf", width = 8.5, height = 6, units = "cm")
#ggsave("./FigS2/Annotations-AUC-boxplot.pdf")
