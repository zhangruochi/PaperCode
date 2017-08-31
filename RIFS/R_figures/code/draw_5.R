library(ggplot2)
library(easyGgplot2)
require(Cairo)
library(gridExtra)

#----------------------图（a）--------------------------------
data <- data.frame(
    ACC =   c( 1.000,   1.000,   0.751,   0.833,   0.930,   0.758,   0.917,   0.973,   0.971,   0.945,   0.983,   0.988,   1.000,   0.880,   0.923,   1.000,   0.794,                                                                   
               1.000,   1.000,   0.751,   0.825,   0.930,   0.749,   0.917,   0.973,   0.971,   0.945,   0.983,   0.988,   1.000,   0.880,   0.925,   1.000,   0.794,                                                                         
               0.625,   0.743,   0.652,   0.809,   0.723,   0.650,   0.774,   0.765,   0.710,   0.917,   0.920,   0.761,   0.763,   0.787,   0.693,   0.471,   0.607,                                                                           
               1.000,   1.000,   0.804,   0.877,   0.948,   0.874,   0.933,   0.988,   0.997,   0.976,   1.000,   1.000,   1.000,   0.894,   0.950,   1.000,   0.828),                                                                       
    
    supp1 = rep(c("TRank","FPR","WRank","RIFS"), each = 17),

    
    
    x = rep(c("Adeno",   "ALL1",    "ALL2",   "ALL3",    "ALL4",    "CNS",
          "Colon",   "DLBCL",   "Gas",      "Gas1",    "Gas2",    "Leuk",    
          "Lym",    "Myel",    "Pros",     "Stroke",  "T1D"), times = 4)
)       

#改变因子水平
data$x <- factor(data$x, levels = c("DLBCL","Pros","Colon","Leuk","Myel","ALL1",    "ALL2",   "ALL3",    "ALL4",    "CNS", 
               "Lym","Adeno","Gas","Gas1","Gas2","T1D","Stroke"))

data$supp1 <- factor(data$supp1,levels = c("TRank","FPR","WRank","RIFS"))                

plot1 <- ggplot(data = data, aes(x = x,y = ACC, group = supp1, color = supp1))    
plot1 <- plot1 + geom_line(size = 1) + geom_point(size = 2, aes(shape = supp1))

#修改坐标轴标签
plot1 <- plot1 + labs(x="",y="mAcc",title = "") + theme(axis.title.y  = element_text(size = 10, color = "black", face = "bold", vjust = 1 , hjust = 0.5)) + theme(axis.title.x = element_text(size = 10, color = "black", face = "bold", vjust = 1 , hjust = 0.5))

#设置坐标轴范围
plot1 <- plot1 + scale_y_continuous(limits = c(0, 1.0),breaks = seq(0,1.0,1/5))


#修改坐标轴刻度
plot1 <- plot1 + theme(axis.text.x = element_text(size = 8, color = "black", face = "bold", vjust = 0.5, hjust = 0.5)) + 
         theme(axis.text.y = element_text(size = 8, color = "black", face = "bold", vjust = 0.5, hjust = 0.5)) + 
         theme(legend.position = "top",legend.title = element_blank(),legend.text = element_text(size = 10),legend.key.size=unit(0.2,'cm'),legend.background = element_rect(colour="white",fill="white",size = 0.2),legend.direction= "horizontal")


#print(plot1)

# ----------------------图（b）-------------------------------
data <- data.frame(
    f_score =  c( 1,  1, 0.82711569,  0.5547619,  0.89880952,  0.65416667,  0.93214286,  0.97979798,  0.94182504,  0.96461538,  0.94571429,  0.98571429,  1,  0.92555119,  0.91714744,  1,  0.83835047,
                1,  1, 0.82711569,  0.51690476,  0.89880952, 0.656,  0.93214286,  0.97979798,  0.94182504,  0.96461538,  0.94571429,  0.98571429, 1,  0.92555119,  0.91812626,  1,  0.83835047,
                0.49333333,  0.29666667,  0.78888889,  0.14480952,  0.5152381,   0.39214286, 0.84611111,  0.85995671,  0.91011685,  0.92310023,  0.60560714,  0.59480952, 0.76190476,  0.88034721,  0.72099456,  0.43366667,  0.72163866,
                1,  1,  0.82556234,  0.51666667,  0.93809524,  0.825, 0.94126984,  0.99090909,  0.94538749,  0.91590077,  0.93142857,  1,  1,  0.93517304,  0.95392385,  1,  0.81625269),
    
    supp1 = rep(c("TRank","FPR","WRank","RIFS"), each = 17),

    
    
    x = rep(c("Adeno",   "ALL1",    "ALL2",   "ALL3",    "ALL4",    "CNS",
          "Colon",   "DLBCL",   "Gas",      "Gas1",    "Gas2",    "Leuk",    
          "Lym",    "Myel",    "Pros",     "Stroke",  "T1D"), times = 4)
)       

#改变因子水平
data$x <- factor(data$x, levels = c("DLBCL","Pros","Colon","Leuk","Myel","ALL1",    "ALL2",   "ALL3",    "ALL4",    "CNS", 
               "Lym","Adeno","Gas","Gas1","Gas2","T1D","Stroke"))

data$supp1 <- factor(data$supp1,levels = c("TRank","FPR","WRank","RIFS"))                

plot2 <- ggplot(data = data, aes(x = x,y = f_score, group = supp1, color = supp1))    
plot2 <- plot2 + geom_line(size = 1) + geom_point(size = 2, aes(shape = supp1))

#修改坐标轴标签
plot2 <- plot2 + labs(x="(a)",y="F-score",title = "") + theme(axis.title.y = element_text(size = 10, color = "black", face = "bold", vjust = 1 , hjust = 0.5)) + theme(axis.title.x = element_text(size = 10, color = "black", face = "bold", vjust = 1 , hjust = 0.5))

#设置坐标轴范围
plot2 <- plot2 + scale_y_continuous(limits = c(0, 1.0),breaks = seq(0,1.0,1/5))


#修改坐标轴刻度
plot2 <- plot2 + theme(axis.text.x = element_text(size = 8, color = "black", face = "bold", vjust = 0.5, hjust = 0.5)) + 
         theme(axis.text.y = element_text(size = 8, color = "black", face = "bold", vjust = 0.5, hjust = 0.5)) + 
         theme(legend.position = "top",legend.title = element_blank(),legend.text = element_text(size = 10),legend.key.size=unit(0.2,'cm'),legend.background = element_rect(colour="white",fill="white",size = 0.2),legend.direction= "horizontal")


#print(plot2)






#----------------------图（d）--------------------------------
data <- data.frame(
    ACC = c(0.993,   1.000,   0.716,   0.809,   0.920,   0.768,   0.900,   0.975,   0.971,   0.958,   0.992,   1.000,   1.000,   0.918,   0.930,   0.900,   0.625,
            0.993,   1.000,   0.672,   0.810,   0.873,   0.728,   0.892,   0.975,   0.936,   0.961,   0.988,   0.985,   0.966,   0.82,  0.922,  0.791,   0.714, 
            0.961,   1.000,   0.652,   0.809,   0.785,   0.650,   0.869,   0.950,   0.893,   0.959,   0.983,   0.932,   0.892,   0.793,   0.838,   0.650,   0.633,   
            1.000,   1.000,   0.804,   0.877,   0.948,   0.874,   0.933,   0.988,   0.997,   0.976,   1.000,   1.000,   1.000,   0.894,   0.950,   1.000,   0.828),                                                                      
    
    supp1 = rep(c("Lasso","RF","Ridge","RIFS"), each = 17),

    
    
    x = rep(c("Adeno",   "ALL1",    "ALL2",   "ALL3",    "ALL4",    "CNS",
          "Colon",   "DLBCL",   "Gas",      "Gas1",    "Gas2",    "Leuk",    
          "Lym",    "Myel",    "Pros",     "Stroke",  "T1D"), times = 4)
)       

#改变因子水平
data$x <- factor(data$x, levels = c("DLBCL","Pros","Colon","Leuk","Myel","ALL1",    "ALL2",   "ALL3",    "ALL4",    "CNS", 
               "Lym","Adeno","Gas","Gas1","Gas2","T1D","Stroke"))

data$supp1 <- factor(data$supp1,levels = c("Lasso","RF","Ridge","RIFS"))                

plot4 <- ggplot(data = data, aes(x = x,y = ACC, group = supp1, color = supp1))    
plot4 <- plot4 + geom_line(size = 1) + geom_point(size = 2, aes(shape = supp1))

#修改坐标轴标签
plot4 <- plot4 + labs(x="",y="mAcc",title = "") + theme(axis.title.y = element_text(size = 10, color = "black", face = "bold", vjust = 1 , hjust = 0.5)) + theme(axis.title.x = element_text(size = 10, color = "black", face = "bold", vjust = 1 , hjust = 0.5))

#设置坐标轴范围
plot4 <- plot4 + scale_y_continuous(limits = c(0, 1.0),breaks = seq(0,1.0,1/5))


#修改坐标轴刻度
plot4 <- plot4 + theme(axis.text.x = element_text(size = 8, color = "black", face = "bold", vjust = 0.5, hjust = 0.5)) + 
         theme(axis.text.y = element_text(size = 8, color = "black", face = "bold", vjust = 0.5, hjust = 0.5)) + 
         theme(legend.position = "top",legend.title = element_blank(),legend.text = element_text(size = 10),legend.key.size=unit(0.2,'cm'),legend.background = element_rect(colour="white",fill="white",size = 0.2),legend.direction= "horizontal")


#print(plot4)

# ----------------------图（e）-------------------------------
data <- data.frame(
    f_score =  c(0.989,      1,          0.80563131,  0.24858333,  0.89047619 , 0.60666667,  0.92777778,  0.98321678,  0.9564986,   0.99230769,  0.96571429,  1,         1.,  0.94746259,  0.92661869,  0.89333333,  0.60681201,
                0.98966667,  1.,          0.79032688,  0.27927056,  0.76777092,  0.54258333,  0.92103175,  0.98278494,  0.95800827,  0.98707925,  0.9277619,   0.97590476, 0.95497619, 0.89494537,  0.91462232,  0.7915, 0.76672453,
                0.96883333,  1,        0.78888889,  0.18794841,  0.61404762,  0.37540476,  0.89246032,  0.96363636,  0.95793651,  0.98181818,  0.86221429,  0.87333333, 0.89,       0.8842881,   0.8384591,   0.69,        0.72163866,
                1,  1,  0.82556234,  0.51666667,  0.93809524,  0.825, 0.94126984,  0.99090909,  0.94538749,  0.91590077,  0.93142857,  1,  1,  0.93517304,  0.95392385,  1,  0.81625269),
    
    supp1 = rep(c("Lasso","RF","Ridge","RIFS"), each = 17),

    
    
    x = rep(c("Adeno",   "ALL1",    "ALL2",   "ALL3",    "ALL4",    "CNS",
          "Colon",   "DLBCL",   "Gas",      "Gas1",    "Gas2",    "Leuk",    
          "Lym",    "Myel",    "Pros",     "Stroke",  "T1D"), times = 4)
)       

#改变因子水平
data$x <- factor(data$x, levels = c("DLBCL","Pros","Colon","Leuk","Myel","ALL1",    "ALL2",   "ALL3",    "ALL4",    "CNS", 
               "Lym","Adeno","Gas","Gas1","Gas2","T1D","Stroke"))

data$supp1 <- factor(data$supp1,levels = c("Lasso","RF","Ridge","RIFS"))                

plot5 <- ggplot(data = data, aes(x = x,y = f_score, group = supp1, color = supp1))    
plot5 <- plot5 + geom_line(size = 1) + geom_point(size = 2, aes(shape = supp1))

#修改坐标轴标签
plot5 <- plot5 + labs(x="(b)",y= "F-score",title = "") + theme(axis.title.y = element_text(size = 10, color = "black", face = "bold", vjust = 1 , hjust = 0.5)) + theme(axis.title.x = element_text(size = 10, color = "black", face = "bold", vjust = 1 , hjust = 0.5))

#设置坐标轴范围
plot5 <- plot5 + scale_y_continuous(limits = c(0, 1.0),breaks = seq(0,1.0,1/5))


#修改坐标轴刻度
plot5 <- plot5 + theme(axis.text.x = element_text(size = 8, color = "black", face = "bold", vjust = 0.5, hjust = 0.5)) + 
         theme(axis.text.y = element_text(size = 8, color = "black", face = "bold", vjust = 0.5, hjust = 0.5)) + 
         theme(legend.position = "top",legend.title = element_blank(),legend.text = element_text(size = 10),legend.key.size=unit(0.2,'cm'),legend.background = element_rect(colour="white",fill="white",size = 0.2),legend.direction= "horizontal")


#print(plot5)



ggsave(file = "figure_5.png", plot = ggplot2.multiplot(plot1,plot2,plot4,plot5, cols=1)) 
ggsave(file = "figure_5.svg", plot = ggplot2.multiplot(plot1,plot2,plot4,plot5, cols=1)) 
