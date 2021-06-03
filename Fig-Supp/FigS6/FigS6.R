#============================
# This script is used to analysis the common features of deepsea and CARMEN, and make the wilcox test to
# test the difference of the two methods 
#============================Load file================================================
library('reshape2')
library('ggplot2')
library(stringr)
library(ggpubr)

infile <- read.table("./FigS6/deepsea_down_sample_AUROC.txt",sep='\t',stringsAsFactors = F, header = T)
colnames(infile) <- c("Assay Categories","CARMEN Annotations","DeepSEA","DeepSEA Downsampling")
infilep <-melt(infile) 
colnames(infilep) <- c("Assay","Methods","AUROC")
infilep$Assay <- factor(infilep$Assay,levels = c("DNA Accessibility","Transcription Factor Binding","Histone Markers"))

#============================Wilcox test==============================================
#sta_result <- wilcox.test(infile$`CARMEN Annotations`,infile$DeepSEA,alternative = "greater")
#sta_result$p.value
#============================Make plot================================================
my_comparisons <- list( c("CARMEN Annotations", "DeepSEA"), c("CARMEN Annotations", "DeepSEA Downsampling"), c("DeepSEA", "DeepSEA Downsampling") )


ggboxplot(data=infilep,x="Methods",y="AUROC",facet.by = "Assay",color="Methods")+
  stat_compare_means(comparisons = my_comparisons, label = "p.signif",method = "wilcox.test")+
  theme(legend.position="top")+
  theme(legend.text=element_text(size=10))+
  theme(axis.text.x = element_blank())+
  theme(axis.title.x = element_blank())+
  theme(axis.ticks.x = element_blank())

ggsave("./FigS6/DeepSEA-downsampling-AUC-compare.pdf")

#=========================AUCPRC============================================

infile <- read.table("./FigS6/deepsea_down_sample_AUPRC.txt",sep='\t',stringsAsFactors = F, header = T)
colnames(infile) <- c("Assay Categories","CARMEN Annotations","DeepSEA","DeepSEA Downsampling")
infilep <-melt(infile) 
colnames(infilep) <- c("Assay","Methods","AUPRC")
infilep$Assay <- factor(infilep$Assay,levels = c("DNA Accessibility","Transcription Factor Binding","Histone Markers"))

#============================Wilcox test==============================================
#sta_result <- wilcox.test(infile$`CARMEN Annotations`,infile$DeepSEA,alternative = "greater")
#sta_result$p.value
#============================Make plot================================================
my_comparisons <- list( c("CARMEN Annotations", "DeepSEA"), c("CARMEN Annotations", "DeepSEA Downsampling"), c("DeepSEA", "DeepSEA Downsampling") )

ggboxplot(data=infilep,x="Methods",y="AUPRC",facet.by = "Assay",color="Methods")+
  stat_compare_means(comparisons = my_comparisons, label = "p.signif",method = "wilcox.test")+
  theme(legend.position="top")+
  theme(legend.text=element_text(size=10))+
  theme(axis.text.x = element_blank())+
  theme(axis.title.x = element_blank())+
  theme(axis.ticks.x = element_blank())

ggsave("./FigS6/DeepSEA-downsampling-AUPRC-compare.pdf")

