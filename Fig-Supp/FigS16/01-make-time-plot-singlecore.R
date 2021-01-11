library(ggplot2)
library(dplyr)
data <- read.table("time-cost.txt",header=F,stringsAsFactors=F)
group_index <- as.matrix(rep(seq(5000,40000,5000),each = 5))
data_plot <- data.frame(cbind(group_index[,1],data*40/60))
colnames(data_plot) <- c("group","time")
data_plot$group <- as.numeric(as.character(data_plot$group))


summarySE <- function(data=NULL, measurevar, groupvars=NULL, na.rm=FALSE,
                      conf.interval=.95, .drop=TRUE) {
    library(plyr)

    # New version of length which can handle NA's: if na.rm==T, don't count them
    length2 <- function (x, na.rm=FALSE) {
        if (na.rm) sum(!is.na(x))
        else       length(x)
    }

    # This does the summary. For each group's data frame, return a vector with
    # N, mean, and sd
    datac <- ddply(data, groupvars, .drop=.drop,
      .fun = function(xx, col) {
        c(N    = length2(xx[[col]], na.rm=na.rm),
          mean = mean   (xx[[col]], na.rm=na.rm),
          sd   = sd     (xx[[col]], na.rm=na.rm)
        )
      },
      measurevar
    )

    # Rename the "mean" column    
    datac <- rename(datac, c("mean" = measurevar))

    datac$se <- datac$sd / sqrt(datac$N)  # Calculate standard error of the mean

    # Confidence interval multiplier for standard error
    # Calculate t-statistic for confidence interval: 
    # e.g., if conf.interval is .95, use .975 (above/below), and use df=N-1
    ciMult <- qt(conf.interval/2 + .5, datac$N-1)
    datac$ci <- datac$se * ciMult

    return(datac)
}



tgc <- summarySE(data_plot, measurevar="time", groupvars=c("group"))

ggplot(tgc, aes(x=group, y=time,colour="red")) + 
  geom_errorbar(aes(ymin=time-sd, ymax=time+sd), colour="black", width=0.6) +
  geom_line() +
  geom_point(size=1) +
  theme_bw()+
  theme(panel.grid.major=element_blank(),panel.grid.minor=element_blank())+
  theme(panel.grid =element_blank()) +
  theme(panel.border= element_blank()) +
  theme(axis.line= element_line(size=0.5, colour ="black"))+
  scale_x_continuous(breaks=seq(0,40000,5000))+
  scale_y_continuous(breaks=seq(0,161,40))+
  #ylim(0,161)+
  theme(axis.text.y=element_text(size = 7,color = "black"))+
  theme(axis.text.x=element_text(size = 7,color = "black"))+
  theme(axis.title.x = element_text(size = 7))+
  theme(axis.title.y = element_text(size = 7))+
  theme(legend.position="none")+
  xlab("Number of Variants")+
  ylab("Time (hours/single core)")


ggsave("time-cost-single-core.pdf", width = 8.5, height = 6, units = "cm")
