library(ggplot2)
library(easyGgplot2)
require(Cairo)


data = data.frame(
    labels = c("DLBCL","Pros","Colon","Leuk","Myel","ALL1",    "ALL2",   "ALL3",    "ALL4",    "CNS", 
               "Lym","Adeno","Gas","Gas1","Gas2","T1D","Stroke"),

    mAcc = c(0.988,0.950,0.933,1.000,0.894,1.000,0.804,0.877,0.948,0.874,1.000,1.000,0.997,0.976,1.000,0.828,1.000)
)

data$labels = factor(data$labels, levels = c("DLBCL","Pros","Colon","Leuk","Myel","ALL1",    "ALL2",   "ALL3",    "ALL4",    "CNS", 
               "Lym","Adeno","Gas","Gas1","Gas2","T1D","Stroke"))

#----------------------图（a）--------------------------------
plot1 <- ggplot(data = data) + labs(x = "", y = "mAcc",title = "") + theme(axis.title.y = element_text(size = 13, color = "black", face = "bold", vjust = 1 , hjust = 0.5))   
plot1 <- plot1 + geom_bar( aes(x = labels,y = mAcc),stat ="identity",width = 0.5 ) + geom_text(aes(x = labels, label= mAcc), stat="count", vjust = -0.5)


#设置坐标轴范围
plot1 <- plot1 + scale_y_continuous(limits=c(0, 1.1),breaks=seq(0,1,1/10))

#修改坐标轴刻度
plot1 <- plot1 + theme(axis.text.x = element_text(size = 13, color = "black", face = "bold", vjust = 0.5, hjust = 0.5)) + 
         theme(axis.text.y = element_text(size = 13, color = "black", face = "bold", vjust = 0.5, hjust = 0.5))

ggsave("figure_4.png", plot1, width = 12, height = 4)
ggsave("figure_4.svg", plot1, width = 12, height = 4)  


