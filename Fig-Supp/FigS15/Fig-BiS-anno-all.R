#============================
# This script is used to analysis the common features of deepsea and CARMEN, and make the wilcox test to
# test the difference of the two methods 
#============================Load file================================================
library('reshape2')
library('ggplot2')
library(stringr)
library(ggpubr)

infile <- read.table("BiS-anno-all.txt",sep='\t',stringsAsFactors = F, header = T)

#============================Wilcox test==============================================
sta_result <- wilcox.test(infile[which(infile[,2] == "prediction_right"),],infile[which(infile[,2] == "prediction_wrong"),],alternative = "greater")
sta_result$p.value
#============================Make plot================================================

ggplot(infile, aes(label, `Mean.annotation.num`, fill=factor(label)))+
  geom_boxplot()+
  stat_compare_means(method = "wilcox.test",label = "p.signif",aes(group = label))+
  theme_bw()+
  theme(panel.grid.major=element_blank(),panel.grid.minor=element_blank())+
#  scale_y_continuous(limits = c(0.5,1.03),breaks=seq(0.5, 1, 0.1))+
  scale_fill_manual(values=c("#CD919E","#9FB6CD")) +
  theme(axis.text.y=element_text(size = 7,color = "black"))+
  theme(axis.text.x=element_text(size = 7,color = "black"))+
  theme(axis.title.x = element_text(size = 7))+
  theme(axis.title.y = element_text(size = 7))+
  guides(fill = guide_legend(title = ""))+
  theme(panel.border= element_blank())+
  theme(axis.line= element_line(size=0.5, colour ="black"))+
  theme(legend.position="top")+
  theme(legend.text=element_text(size=5))+
  scale_x_discrete(labels=c("prediction_right" = "Correct prediction", "prediction_wrong" = "Incorrect prediction"))+
#  xlim("Correct prediction", "Incorrect prediction")+
  xlab("CARMEN prediction results")+
  ylab("Number of cell lines or tissues")
 
# coord_cartesian(ylim = c(0.5, 1.05))+
 # scale_x_discrete(labels = function(x) str_wrap(x, width = 15))


ggsave("Bis-anno-all.pdf", width = 8, height = 8, units = "cm")

