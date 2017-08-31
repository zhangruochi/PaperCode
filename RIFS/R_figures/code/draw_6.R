library(ggplot2)
library(easyGgplot2)
require(Cairo)
library(gridExtra)

data <- data.frame(
    x = c(362.925,640.24375,581.340625,615.9885417,660.8020833,625.7833333,500.01875,550.7,667.4958333,466.78125,
          306.3770833,268.325,285.0052083,290.8114583,417.7833333,378.778125,238.09375,247.3927083,241.3802083,385.4083333,221.5041667,217.5875,254.6833333,266.2958333,266.4958333,
          251.5083333,328.7760417,346.565625,288.5583333,273.7385417,270.8270833,374.1604167,247.6104167,322.9541667,259.6020833,202.5770833,262.4729167,224.190625,289.2458333,361.2604167,335.6354167,311.6520833),


    y = c(330.39375,379.39375,436.4197917,437.8375,437.9885417,466.2729167,398.68125,344.4958333,499.475,368.9729167,
          269.8854167,257.7708333,246.4166667,252.7416667,292.3270833,311.125,242.3875,227.45625,279.9479167,196.6,282.55,230.5520833,246.0229167,259.75625,258.634375,260.64375,
          235.8895833,290.0010417,202.7020833,235.9458333,287.14375,263.3083333,246.7510417,158.9979167,263.175,212.2416667,232.3302083,239.9645833,307.55,277.5354167,193.4020833,294.896875),

    color = c(rep(c("benign prostatic hyperplasia"),times = 10), rep(c("prostate carcinoma"),times = 32))
    )

    plot1 <- ggplot(data = data, mapping = aes(x = x, y = y, color = color,shape = color)) + geom_point(size = 5)

    #修改坐标轴标签
    plot1 <- plot1 + labs(x="ILMN_1708743",y="ILMN_1727184",title = "") + theme(axis.title.y  = element_text(size = 10, color = "black", face = "bold", vjust = 1 , hjust = 0.5)) + theme(axis.title.x = element_text(size = 10, color = "black", face = "bold", vjust = 1 , hjust = 0.5))

    #设置坐标轴范围
    plot1 <- plot1 + scale_x_continuous(limits = c(200, 800),breaks = seq(200,800,200))


    #修改坐标轴刻度
    plot1 <- plot1 + theme(axis.text.x = element_text(size = 15, color = "black", face = "bold", vjust = 0.5, hjust = 0.5)) + 
             theme(axis.text.y = element_text(size = 15, color = "black", face = "bold", vjust = 0.5, hjust = 0.5)) + 
             theme(legend.position = "top",legend.title = element_blank(),legend.text = element_text(size = 10),legend.key.size=unit(0.2,'cm'),legend.background = element_rect(colour="white",fill="white",size = 0.2),legend.direction= "horizontal")


#print(plot1)
ggsave("figure_6.png", plot1)
ggsave("figure_6.svg", plot1)  