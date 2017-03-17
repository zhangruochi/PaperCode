# commandArgs <- function(trailingOnly=FALSE) c(1,2,3) 
curFileDir <- dirname(sys.frame(1)$ofile) #get current file directory
# source(file.path(curFileDir,"gdm4Par.R"))

data <- NULL
cluster <- NULL
#linux
system(paste("Rscript",file.path(curFileDir,"gdm4Par.R"),
             "-p" ,  "~/y/" ,
             "--cur.file.dir" ,  "/home/starqiu/DNBWorkspace/DetectAndAnalysisDNB/src/main/resources/core" ,
             "--case.file.path" , "/host/data/sourceData/liver_case_data.txt",
             "--period.count" , "5" ,
             "--period.sample.count" ,  "5" ,
             "--features.sd.threshold" , "0.001" ,
             "--cluster.method" , "hclust" ,
             "--cluster.number" , "20" ,
             "--pcc.out.amount" , "50" ,
             "--cores" , "6" ,
             "--control.file.path" ,"/host/data/sourceData/liver_control_data.txt"))

#linux with one state
# system(paste("Rscript",file.path(curFileDir,"gdm4Par.R"),
#              "-p" ,  "~/x/" ,
#              "--cur.file.dir" ,  "/home/starqiu/DNBWorkspace/DetectAndAnalysisDNB/src/main/resources/core" ,
#              "--case.file.path" , "/host/data/sourceData/liver_case_data.txt",
#              "--period.count" , "5" ,
#              "--period.sample.count" ,  "5" ,
#              "--features.sd.threshold" , "0.001" ,
#              "--cluster.method" , "kmeans" ,
#              "--cluster.number" , "10" ,
#              "--pcc.out.amount" , "50" ,
#              "--cores" , "6" ))

# linux :file divided
# system(paste("Rscript",file.path(curFileDir,"gdm4Par.R"),
#              "-p" ,  "~/x/" ,
#              "-cur.file.dir" ,  "/home/starqiu/DNBWorkspace/DetectAndAnalysisDNB/src/main/resources/core" ,
#              "--file.divided" , "true" ,
#              "--case.file.path" , paste0("/host/data/sourceData/case_matrix_table_",1:5,".txt;",collapse = ""),
#              "--period.count" , "5" ,
#              "--period.sample.count" ,  "5" ,
#              "--features.sd.threshold" , "0.001" ,
#              "--cluster.method" , "hclust" ,
#              "--cluster.number" , "20" ,
#              "--pcc.out.amount" , "50" ,
#              "--cores" , "6" ,
#              "--control.file.path" ,  paste0("/host/data/sourceData/control_matrix_table_",1:5,".txt;",collapse = "")))


#windows
# system(paste("Rscript",file.path(curFileDir,"gdm4Par.R"),
#              "-p" ,  "D:\\x\\" ,
#              "--case.file.path" , "D:\\data\\sourceData\\liver_case_data.txt",
#              "--period.count" , "5" ,
#              "--period.sample.count" ,  "5" ,
#              "--features.sd.threshold" , "0.001" ,
#              "--cluster.method" , "hclust" ,
#              "--cluster.number" , "20" ,
#              "--pcc.out.amount" , "50" ,
#              "--cores" , "6" ,
#              "--control.file.path" ,"D:\\data\\sourceData\\liver_control_data.txt"))

# windows :file divided
# system(paste("Rscript",file.path(curFileDir,"gdm4Par.R"),
#              "-p" ,  "D:\\x\\"" ,
#              "--file.divided" , "true" ,
#              "--case.file.path" , paste0("D:\\data\\sourceData\\case_matrix_table_",1:5,".txt;",collapse = ""),
#              "--period.count" , "5" ,
#              "--period.sample.count" ,  "5" ,
#              "--features.sd.threshold" , "0.001" ,
#              "--cluster.method" , "hclust" ,
#              "--cluster.number" , "20" ,
#              "--pcc.out.amount" , "50" ,
#              "--cores" , "6" ,
#              "--control.file.path" ,  paste0("D:\\data\\sourceData\\control_matrix_table_",1:5,".txt;",collapse = "")))
# 
