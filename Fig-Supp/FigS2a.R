#============================
# This script is used to analysis the common features of deepsea and CARMEN, and make the wilcox test to
# test the difference of the two methods 
#============================Load file================================================
library('reshape2')
library('ggplot2')
library(stringr)
library(ggpubr)

#=====================profiles compare==================================
infile <- read.table("./FigS2/profiles-compare.txt",header = T,stringsAsFactors = F,sep=',')
colnames(infile) <- c("Profile","CARMEN Annotations","DeepSEA")
infilep <- melt(infile)
colnames(infilep) <- c("Assay Categories","Methods","Number of Profiles")
infilep$`Assay Categories` <- factor(infilep$`Assay Categories`,levels = c("DNA Accessibility","Transcription Factor Binding","Histone Markers","Meythylation Profiles"))
ggplot(infilep, aes(`Assay Categories`, `Number of Profiles`, fill=factor(Methods)))+
  geom_bar(stat="identity", position=position_dodge())+
  theme_bw()+
  theme(panel.grid.major=element_blank(),panel.grid.minor=element_blank())+
  theme(axis.text.y=element_text(size = 6,color = "black"))+
  theme(axis.text.x=element_text(size = 6,color = "black"))+
  theme(axis.title.x = element_text(size = 6))+
  theme(axis.title.y = element_text(size = 6))+
  guides(fill = guide_legend(title = ""))+
  theme(panel.border= element_blank())+
  theme(axis.line= element_line(size=0.5, colour ="black"))+
  theme(legend.position="top")+
  theme(legend.text=element_text(size=6))+
  coord_cartesian(ylim = c(0, 1300))+
  scale_x_discrete(breaks=c("0.5","1","2","3"),
          labels=c("DNA Accessibility", "Transcription Factor Binding", "Histone Markers", "Methylation Profiles"))+
  scale_x_discrete(labels = function(x) str_wrap(x, width = 15))

ggsave("./FigS2/profiles-compare.pdf", width = 8.5, height = 6, units = "cm")
