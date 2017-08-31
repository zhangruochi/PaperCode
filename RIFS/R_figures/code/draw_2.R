library(ggplot2)
library(easyGgplot2)
require(Cairo)


data = data.frame(
    group_labels = rep(c("ALL2","ALL3"),each = 2),
    #color= rep(c('#808080','#808080',"#000000","#000000"),
    legend = rep(c("IFS(i)","IFS(0)"), times = 2),
    IFS_K = c(0.795,0.863,0.770,0.850)
)


#----------------------图（a）--------------------------------
plot1 <- ggplot(data = data)    
plot1 <- plot1 + geom_bar( aes(x = group_labels,y = IFS_K, fill = legend), position = "dodge",stat="identity",width = 0.5)  + scale_fill_manual(values=c("#808080", "#000000")) 

#修改坐标轴标签
plot1 <- plot1 + labs(x="(a)",y="",title = "") + xlab("(a)") + theme(axis.title.x = element_text(size = 15, color = "black", face = "bold", vjust = 1 , hjust = 0.5))

#设置坐标轴范围
plot1 <- plot1 + scale_y_continuous(limits=c(0, 1),breaks=seq(0,1,1/5))

#修改坐标轴刻度
plot1 <- plot1 + theme(axis.text.x = element_text(size = 10, color = "black", face = "bold", vjust = 0.5, hjust = 0.5)) + 
         theme(axis.text.y = element_text(size = 10, color = "black", face = "bold", vjust = 0.5, hjust = 0.5)) +
         theme(legend.position = c(.5,.92),legend.title = element_blank(),legend.text = element_text(size = 10),legend.key.size=unit(0.3,'cm'),legend.background = element_rect(colour="white",fill="white",size = 0.5), legend.direction = "horizontal")


#修改图片title
#plot1 <- plot1 + theme( plot.title = element_text(size = 16, face = "bold")) 
#print(plot1)


#----------------------图（b）--------------------------------
data <- data.frame(
    T1D <- c(0.656 ,0.667 ,0.654 ,0.708 ,0.742 ,0.786 ),
    x_2 = c(757,758,759,760,761,762)
)         

plot2 <- ggplot(data = data)    
plot2 <- plot2 + geom_line( aes(x = x_2,y = T1D), color = "black") + geom_point(aes(x = x_2,y = T1D ),size = 4, shape = 15)

#修改坐标轴标签
plot2 <- plot2 + labs(x="(b)",y="",title = "")+ xlab("(b)") + theme(axis.title.x = element_text(size = 15, color = "black", face = "bold", vjust = 1 , hjust = 0.5))

#设置坐标轴范围
plot2 <- plot2 + scale_y_continuous(limits=c(0.5, 1.0),breaks=seq(0,1,1/10))

#修改坐标轴刻度
plot2 <- plot2 + theme(axis.text.x = element_text(size = 10, color = "black", face = "bold", vjust = 0.5, hjust = 0.5)) + 
         theme(axis.text.y = element_text(size = 10, color = "black", face = "bold", vjust = 0.5, hjust = 0.5))

#print(plot2)



#----------------------图（c）--------------------------------

data <- data.frame(
    Colon = c(0.757 ,0.836 ,0.855 ,0.840 ,0.869 ,0.869),
    x = c(37,38,39,40,41,42)
)         

plot3 <- ggplot(data = data)    
plot3 <- plot3 + geom_line( aes(x = x,y = Colon )) + geom_point(aes(x = x,y = Colon ),size=4, shape=15)


plot3 <- plot3 + labs(x="(c)",y="",title = "")

#设置坐标轴范围
plot3 <- plot3 + scale_y_continuous(limits=c(0.5, 1.0),breaks = seq(0,1,1/10))

#修改坐标轴标签
plot3 <- plot3 + xlab("(c)") + theme(axis.title.x = element_text(size = 15, color = "black", face = "bold", vjust = 1 , hjust = 0.5))

#修改坐标轴刻度
plot3 <- plot3 + theme(axis.text.x = element_text(size = 10, color = "black", face = "bold", vjust = 0.5, hjust = 0.5)) + 
         theme(axis.text.y = element_text(size = 10, color = "black", face = "bold", vjust = 0.5, hjust = 0.5))

#print(plot3)


#----------------------图（d）--------------------------------
data <- data.frame(
    ALL = c(1.000,1.000,1.000,1.000,1.000,0.795,0.795,0.797,0.797,0.797,0.883,0.883,0.883,0.883,0.883,0.939,0.939,0.939,0.948,0.939),
    supp1 = rep(c("ALL1","ALL2","ALL3","ALL4"), each = 5),
    x = rep(c(0.15,0.25,0.35,0.45,0.55), times = 4)
)         

plot4 <- ggplot(data = data,aes(x = x,y = ALL, group = supp1))    
plot4 <- plot4 + geom_line() + geom_point(size = 4, aes(shape = supp1))


plot4 <- plot4 + labs(x="(d)",y="",title = "")

#设置坐标轴范围
plot4 <- plot4 + scale_y_continuous(limits = c(0.75, 1.05),breaks = seq(0,1.0,1/20)) + scale_x_continuous(limits=c(0.15, 0.55),breaks = seq(0.15,0.55,0.1),labels = c("15%","25%","35%","45%","55%"))

#修改坐标轴标签
plot4 <- plot4 + xlab("(d)") + theme(axis.title.x = element_text(size = 15, color = "black", face = "bold", vjust = 1 , hjust = 0.5))

#修改坐标轴刻度
plot4 <- plot4 + theme(axis.text.x = element_text(size = 10, color = "black", face = "bold", vjust = 0.5, hjust = 0.5)) + 
         theme(axis.text.y = element_text(size = 10, color = "black", face = "bold", vjust = 0.5, hjust = 0.5)) + 
         theme(legend.position = c(.5,.92),legend.title = element_blank(),legend.text = element_text(size = 10),legend.key.size=unit(0.3,'cm'),legend.background = element_rect(colour="white",fill="white",size = 0.3),legend.direction= "horizontal")

#print(plot4)

#ggplot2.multiplot(plot1,plot2,plot3,plot4, cols=2)

ggsave(file = "figure_2.png", plot = ggplot2.multiplot(plot1,plot2,plot3,plot4, cols=2)) 
ggsave(file = "figure_2.svg", plot = ggplot2.multiplot(plot1,plot2,plot3,plot4, cols=2)) 







