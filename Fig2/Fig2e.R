library(ggplot2)
library(reshape2)

data <- read.table("./Fig2e/04_plot_use_file.txt",sep=',',stringsAsFactors=F,header=T)
colnames(data) <- c("name_list","CARMEN-E","CARMEN-F")
infile <- melt(data)
infile$name_list <- factor(infile$name_list,levels=rev(c("Transcription Factor Binding","Histone Markers","Evolutionary Features","DNase Accessibility","Methylation Profiles","Pysicochemical Properties")))
infile$variable <- factor(infile$variable,levels=c("CARMEN-F","CARMEN-E"))

ggplot(infile,aes(variable,value,fill=name_list))+
geom_bar(stat="identity",position="stack",width=0.3)+
theme_bw()+
theme(panel.grid.major=element_blank(),panel.grid.minor=element_blank())+
theme(axis.ticks.length=unit(0.1,'cm'))+
theme(axis.text.y=element_text(size = 7,color = "black"))+
theme(axis.text.x=element_text(size = 7,color = "black"))+
theme(legend.position="bottom")+
xlab("")+
ylab("Feature Importance Proportion")+
theme(axis.title=element_text(size = 7,color = "black"))+
theme(legend.text = element_text(size=5))+
coord_flip()+
scale_fill_brewer(palette = "Set2")+
guides(fill=guide_legend(title=NULL,reverse=TRUE))

ggsave("importance.pdf", width = 8.5, height = 6, units = "cm")
#ggsave("importance.pdf")
