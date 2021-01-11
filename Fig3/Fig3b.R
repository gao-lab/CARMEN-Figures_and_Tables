library(ggplot2)
library(reshape2)
infile <- read.table("./Fig3b/rs883868-annotation.txt",sep=' ',stringsAsFactors = F, header = T)
df <- data.frame(melt(infile))
colnames(df) <- c("cellline","Allele","Affinity")


ggplot(data=df, aes(x=Allele, y=Affinity)) +
  geom_bar(aes(fill = Allele), stat="identity")+
  theme_bw()+
  scale_y_continuous(limits = c(0, 1),expand = c(0, 0))+
  theme(axis.text.y=element_text(size = 6,color = "black"))+
  theme(axis.text.x=element_text(size = 6,color = "black"))+
  theme(axis.title.x = element_text(size = 6))+
  theme(axis.title.y = element_text(size = 6))+
  xlab("Alleles of rs883868")+
  ylab("Prediction Binding Affinity of YY1")+
  facet_wrap(vars(cellline), nrow = 3)+
  scale_fill_manual("legend", values = c("T" = "#FFB90F", "C" = "#AB82FF"))+
  theme(strip.text = element_text(size=6))+
  theme(legend.position="none")+
  theme(axis.ticks.x=element_line(size=0.5))+
  theme(axis.ticks.y=element_line(size=0.5))+
  theme(panel.grid.major=element_blank(),panel.grid.minor=element_blank())



ggsave("./Fig3b/Annotation-rs883868.pdf",width = 7, height = 6, units = "cm")

