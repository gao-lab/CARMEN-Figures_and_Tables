#============================
# This script is used to analysis the common features of deepsea and CARMEN, and make the wilcox test to
# test the difference of the two methods 
#============================Load file================================================
library('reshape2')
library('ggplot2')
library(stringr)
library(ggpubr)

infile <- read.table("./FigS11/retrained-AUC.txt",sep='\t',stringsAsFactors = F, header = T)
colnames(infile) <- c("Assay Categories","DeepSEA Testing Dataset","CARMEN Testing Dataset")
infilep <-melt(infile) 
colnames(infilep) <- c("Assay Categories","Dataset","AUROC")
infilep$`Assay Categories` <- factor(infilep$`Assay Categories`,levels = c("DNA Accessibility","Transcription Factor Binding","Histone Markers"))
infilep$`AUROC` <- as.numeric(infilep$`AUROC`)
#============================Wilcox test==============================================
sta_result <- wilcox.test(infile$`DeepSEA Testing Dataset`,infile$`CARMEN Testing Dataset`,alternative = "greater")
sta_result$p.value
#============================Make plot================================================

ggplot(infilep, aes(`Assay Categories`, AUROC, fill=factor(Dataset,levels = c("CARMEN Testing Dataset","DeepSEA Testing Dataset"))))+
  geom_boxplot()+
  stat_compare_means(label = "p.signif",aes(group = Dataset),label.y = 1.03 )+
  theme_bw()+
  theme(panel.grid.major=element_blank(),panel.grid.minor=element_blank())+
  scale_y_continuous(limits = c(0.4,1.03),breaks=seq(0.4, 1, 0.1))+
  scale_fill_manual(values=c("#CD919E","#9FB6CD")) +
  theme(axis.text.y=element_text(size = 7,color = "black"))+
  theme(axis.text.x=element_text(size = 7,color = "black"))+
  theme(axis.title.x = element_text(size = 7))+
  theme(axis.title.y = element_text(size = 7))+
  guides(fill = guide_legend(title = ""))+
  theme(panel.border= element_blank())+
  theme(axis.line= element_line(size=0.5, colour ="black"))+
  theme(legend.position="top")+
  theme(legend.text=element_text(size=7))+
  coord_cartesian(ylim = c(0.4, 1.05))+
  scale_x_discrete(labels = function(x) str_wrap(x, width = 15))


ggsave("./FigS11/retrained-AUC-compare.pdf", width = 9, height = 8, units = "cm")


#=========================AUCPRC============================================

infile <- read.table("./FigS11/retrained-AUPRC.txt",sep='\t',stringsAsFactors = F, header = T)
colnames(infile) <- c("Assay Categories","DeepSEA Testing Dataset","CARMEN Testing Dataset")
infilep <-melt(infile) 
colnames(infilep) <- c("Assay Categories","Dataset","AUPRC")
infilep$`Assay Categories` <- factor(infilep$`Assay Categories`,levels = c("DNA Accessibility","Transcription Factor Binding","Histone Markers"))
#============================Wilcox test==============================================
sta_result <- wilcox.test(infile$`DeepSEA Testing Dataset`,infile$`CARMEN Testing Dataset`,alternative = "greater")
sta_result$p.value
#============================Make plot================================================

ggplot(infilep, aes(`Assay Categories`, AUPRC, fill=factor(Dataset,levels = c("CARMEN Testing Dataset","DeepSEA Testing Dataset"))))+
  geom_boxplot()+
  stat_compare_means(label = "p.signif",aes(group = Dataset),label.y = 1.03 )+
  theme_bw()+
  theme(panel.grid.major=element_blank(),panel.grid.minor=element_blank())+
  scale_y_continuous(limits = c(0,1.03),breaks=seq(0, 1, 0.2))+
  scale_fill_manual(values=c("#CD919E","#9FB6CD")) +
  theme(axis.text.y=element_text(size = 7,color = "black"))+
  theme(axis.text.x=element_text(size = 7,color = "black"))+
  theme(axis.title.x = element_text(size = 7))+
  theme(axis.title.y = element_text(size = 7))+
  guides(fill = guide_legend(title = ""))+
  theme(panel.border= element_blank())+
  theme(axis.line= element_line(size=0.5, colour ="black"))+
  theme(legend.position="top")+
  theme(legend.text=element_text(size=7))+
  scale_x_discrete(labels = function(x) str_wrap(x, width = 15))

ggsave("./FigS11/retrained-AUPRC-compare.pdf", width = 9, height = 8, units = "cm")

