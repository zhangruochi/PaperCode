curFileDir <- dirname(sys.frame(1)$ofile) #get current file directory
# source(file.path(curFileDir,"gdm4Par.R"))

data <- NULL
cluster <- NULL

#linux
system(paste("Rscript",file.path(curFileDir,"calcCiInSpecDnbPeriod.R"),
             "-p" ,  "~/z/" ,
             "--period.count" , "4" ,
             "--period.sample.count" ,  "3" ,
             "--pcc.out.amount" , "50" ,
             "--dnb.period" , "2" ,
             "--has.control.example" ,"true"))
