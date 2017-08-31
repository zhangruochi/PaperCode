library(ggplot2)
library(easyGgplot2)
require(Cairo)


#----------------------图（a）--------------------------------
data <- data.frame(
    ALL = c( 1.000,   1.000,   1.000,   1.000,   1.000, 0.795,   0.795,   0.795,   0.799,   0.799, 0.856,   0.856,   0.856,   0.883,   0.883, 0.906,   0.930,   0.939,   0.939,   0.939), 
    supp1 = rep(c("ALL1","ALL2","ALL3","ALL4"), each = 5),
    x = rep(c(1,2,3,4,5), times = 4)
)         

plot1 <- ggplot(data = data,aes(x = x,y = ALL, group = supp1, shape = supp1, color = supp1))    
plot1 <- plot1 + geom_line(size = 1) + geom_point(size = 2, aes(shape = supp1))

#修改坐标轴标签
plot1 <- plot1 + labs(x="(a)",y="",title = "PstartingPercentage=10%") + xlab("(a)") + theme(plot.title = element_text(size = 13, color = "black", face = "bold", vjust = 1 , hjust = 0.5)) + theme(axis.title.x = element_text(size = 13, color = "black", face = "bold", vjust = 1 , hjust = 0.5))

#设置坐标轴范围
plot1 <- plot1 + scale_y_continuous(limits = c(0.7, 1.05),breaks = seq(0,1.0,1/10))


#修改坐标轴刻度
plot1 <- plot1 + theme(axis.text.x = element_text(size = 13, color = "black", face = "bold", vjust = 0.5, hjust = 0.5)) + 
         theme(axis.text.y = element_text(size = 13, color = "black", face = "bold", vjust = 0.5, hjust = 0.5)) + 
         theme(legend.position = "top",legend.title = element_blank(),legend.text = element_text(size = 10),legend.key.size=unit(0.2,'cm'),legend.background = element_rect(colour="white",fill="white",size = 0.2),legend.direction= "horizontal")


#print(plot1)


#----------------------图（b）--------------------------------
data <- data.frame(
    ALL = c( 1.000,   1.000,   1.000,   1.000,   1.000, 0.795,   0.795,   0.795,   0.799,   0.799, 0.856,   0.863,   0.863,   0.883,   0.883, 0.906,   0.930,   0.939,   0.939,   0.939 ),
    supp1 = rep(c("ALL1","ALL2","ALL3","ALL4"), each = 5),
    x = rep(c(1,2,3,4,5), times = 4)
)         

plot2 <- ggplot(data = data,aes(x = x,y = ALL, group = supp1,shape = supp1, color = supp1))    
plot2 <- plot2 + geom_line(size = 1) + geom_point(size = 2, aes(shape = supp1))

#修改坐标轴标签
plot2 <- plot2 + labs(x="(b)",y="",title = "PstartingPercentage=20%") + xlab("(b)") + theme(plot.title = element_text(size = 13, color = "black", face = "bold", vjust = 1 , hjust = 0.5)) + theme(axis.title.x = element_text(size = 13, color = "black", face = "bold", vjust = 1 , hjust = 0.5))

#设置坐标轴范围
plot2 <- plot2 + scale_y_continuous(limits = c(0.7, 1.05),breaks = seq(0,1.0,1/10))


#修改坐标轴刻度
plot2 <- plot2 + theme(axis.text.x = element_text(size = 13, color = "black", face = "bold", vjust = 0.5, hjust = 0.5)) + 
         theme(axis.text.y = element_text(size = 13, color = "black", face = "bold", vjust = 0.5, hjust = 0.5)) + 
         theme(legend.position = "top",legend.title = element_blank(),legend.text = element_text(size = 10),legend.key.size=unit(0.2,'cm'),legend.background = element_rect(colour="white",fill="white",size = 0.2),legend.direction= "horizontal")


#print(plot2)



#----------------------图（c）--------------------------------
data <- data.frame(
    ALL = c(1.000,   1.000,   1.000,   1.000,   1.000,    0.795,   0.795,   0.796,   0.816,   0.799,   0.856,   0.863,   0.863,   0.883,   0.883,    0.906,   0.930,   0.939,   0.939,   0.939 ),
    supp1 = rep(c("ALL1","ALL2","ALL3","ALL4"), each = 5),
    x = rep(c(1,2,3,4,5), times = 4)
)         

plot3 <- ggplot(data = data,aes(x = x,y = ALL, group = supp1, shape = supp1, color = supp1))    
plot3 <- plot3 + geom_line(size = 1) + geom_point(size = 2, aes(shape = supp1))

#修改坐标轴标签
plot3 <- plot3 + labs(x="(c)",y="",title = "PstartingPercentage=30%") + xlab("(c)") + theme(plot.title = element_text(size = 13, color = "black", face = "bold", vjust = 1 , hjust = 0.5)) + theme(axis.title.x = element_text(size = 13, color = "black", face = "bold", vjust = 1 , hjust = 0.5))

#设置坐标轴范围
plot3 <- plot3 + scale_y_continuous(limits = c(0.7, 1.05),breaks = seq(0,1.0,1/10))


#修改坐标轴刻度
plot3 <- plot3 + theme(axis.text.x = element_text(size = 13, color = "black", face = "bold", vjust = 0.5, hjust = 0.5)) + 
         theme(axis.text.y = element_text(size = 13, color = "black", face = "bold", vjust = 0.5, hjust = 0.5)) + 
         theme(legend.position = "top",legend.title = element_blank(),legend.text = element_text(size = 10),legend.key.size=unit(0.2,'cm'),legend.background = element_rect(colour="white",fill="white",size = 0.2),legend.direction= "horizontal")


#print(plot3)


#----------------------图（d）--------------------------------
data <- data.frame(
    ALL  = c(  1,   1,   1,   1,   1, 0.795,   0.795,   0.809,   0.806,   0.806, 0.856,   0.863,   0.863,   0.883,   0.883, 0.91,    0.93,    0.939,   0.949,   0.949 ),
    supp1 = rep(c("ALL1","ALL2","ALL3","ALL4"), each = 5),
    x = rep(c(1,2,3,4,5), times = 4)
)         

plot4 <- ggplot(data = data,aes(x = x,y = ALL, group = supp1, shape = supp1, color = supp1))    
plot4 <- plot4 + geom_line(size = 1) + geom_point(size = 2, aes(shape = supp1))

#修改坐标轴标签
plot4 <- plot4 + labs(x="(d)",y="",title = "PstartingPercentage=40%") + xlab("(d)") + theme(plot.title = element_text(size = 13, color = "black", face = "bold", vjust = 1 , hjust = 0.5)) + theme(axis.title.x = element_text(size = 13, color = "black", face = "bold", vjust = 1 , hjust = 0.5))

#设置坐标轴范围
plot4 <- plot4 + scale_y_continuous(limits = c(0.7, 1.05),breaks = seq(0,1.0,1/10))


#修改坐标轴刻度
plot4 <- plot4 + theme(axis.text.x = element_text(size = 13, color = "black", face = "bold", vjust = 0.5, hjust = 0.5)) + 
         theme(axis.text.y = element_text(size = 13, color = "black", face = "bold", vjust = 0.5, hjust = 0.5)) + 
         theme(legend.position = "top",legend.title = element_blank(),legend.text = element_text(size = 10),legend.key.size=unit(0.2,'cm'),legend.background = element_rect(colour="white",fill="white",size = 0.2),legend.direction= "horizontal")

#print(plot4)


#----------------------图（e）--------------------------------
data <- data.frame(
    ALL  = c(   1,   1,   1,   1,   1, 0.795,   0.795,   0.809,   0.806,   0.806, 0.856,   0.863,   0.863,   0.883,   0.883, 0.91,    0.93,    0.939,   0.949,   0.949 ),
    supp1 = rep(c("ALL1","ALL2","ALL3","ALL4"), each = 5),
    x = rep(c(1,2,3,4,5), times = 4)
)         

plot5 <- ggplot(data = data,aes(x = x,y = ALL, group = supp1,shape = supp1, color = supp1))    
plot5 <- plot5 + geom_line(size = 1) + geom_point(size = 2, aes(shape = supp1))

#修改坐标轴标签
plot5 <- plot5 + labs(x="(3)",y="",title = "PstartingPercentage=50%") + xlab("(e)") + theme(plot.title = element_text(size = 13, color = "black", face = "bold", vjust = 1 , hjust = 0.5)) + theme(axis.title.x = element_text(size = 13, color = "black", face = "bold", vjust = 1 , hjust = 0.5))

#设置坐标轴范围
plot5 <- plot5 + scale_y_continuous(limits = c(0.7, 1.05),breaks = seq(0,1.0,1/10))


#修改坐标轴刻度
plot5 <- plot5 + theme(axis.text.x = element_text(size = 13, color = "black", face = "bold", vjust = 0.5, hjust = 0.5)) + 
         theme(axis.text.y = element_text(size = 13, color = "black", face = "bold", vjust = 0.5, hjust = 0.5)) + 
         theme(legend.position = "top",legend.title = element_blank(),legend.text = element_text(size = 10),legend.key.size=unit(0.2,'cm'),legend.background = element_rect(colour="white",fill="white",size = 0.2),legend.direction= "horizontal")


#print(plot5)

ggsave(file = "figure_3.png", plot = ggplot2.multiplot(plot1,plot2,plot3,plot4,plot5, cols = 2)) 
ggsave(file = "figure_3.svg", plot = ggplot2.multiplot(plot1,plot2,plot3,plot4,plot5, cols = 2)) 

