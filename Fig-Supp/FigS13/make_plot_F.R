library("ggplot2")

data <- read.csv("CARMEN-F-merge.csv")
#data$Importance = -10*log(data$Importance,10)
data <- data[1:40,]
data$Feature <- factor(data$Feature, levels=rev(data$Feature))

ggplot(data,aes(Importance,Feature))+
geom_point(aes(size=Importance*100,color=Importance))+
theme(axis.text.y=element_text(size = 8,color = "black"))+
theme(axis.text.x=element_text(size = 8,color = "black"))+
xlab("Feature Importance")+
ylab("Top 40 Features in CARMEN-F")+
scale_color_gradient(low = "blue",high = "#754F44")
#scale_color_distiller(direction = -1)
#scale_color_distiller(palette = "Greens",direction = -1)

ggsave("CARMEN-F.pdf")

#ggsave("CARMEN-E.pdf", width = 8, height = 8, units = "cm")
