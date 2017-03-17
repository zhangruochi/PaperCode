# give a module gene ids ,calc its ci value

# BASE.PATH <- "/host/data/"
# make sure all data are included in this directory
BASE.PATH <- "D:\\x\\"

PERIOD.COUNT <- 5 #we have 5 periods:4wk,8wk,12wk,16wk,20wk
PERIOD.SAMPLE.SEP <- 10 #each period has 10 samples
PERIOD.SAMPLE.COUNT <- 5 # divide into case and WKY, each have 5 samples 
PCC.OUT.AMOUNT <- 50
STATE <- c("case","control") 

calc.pcc <- function(state,period,base.dir=BASE.PATH){
  whole.table <- read.table(paste(base.dir,state,"_matrix_table_",period,".txt",sep=""),
                               header=TRUE,sep="")
#   geneIds <- whole.table[,1] #as the row names and column names of matrix
  whole.table <- whole.table[,c(2:(PERIOD.SAMPLE.COUNT+1))]
  trans.matrix <- t(as.matrix(whole.table)) #matrix Transpose
  cor.matrix <- abs(cor(trans.matrix))
#   rownames(cor.matrix) <- geneIds
#   colnames(cor.matrix) <- geneIds
#   cor.matrix
}


calc.ci <- function (author,period,module.file.name,base.dir=BASE.PATH) {
  module.gene.ids <- read.table(paste(base.dir,module.file.name,".txt",sep=""),
                                sep="")[,1]
  module.gene.ids <- as.character(module.gene.ids)
  
  case.data <- read.table(paste(base.dir,STATE[1],"_matrix_table_",period,".txt",sep=""),
                        header=TRUE,sep="")
  dnb.index <- which(as.character(case.data[,1]) %in% module.gene.ids)
  case.data.dnb <- case.data[dnb.index,-1]
  rm(case.data)
  
  control.data <- read.table(paste(base.dir,STATE[2],"_matrix_table_",period,".txt",sep=""),
                        header=TRUE,sep="")
  control.data.dnb <- control.data[dnb.index,-1]
  rm(control.data)
  
  case.sd <- apply(case.data.dnb,1,sd)
  control.sd <- apply(control.data.dnb,1,sd)
  sd.mean <- mean(case.sd,na.rm=TRUE) / mean(control.sd,na.rm=TRUE)
  rm(case.sd)
  rm(control.sd)
  
  #control sample 
  control.cor.table <- calc.pcc(STATE[2],period)
#   control.cor.table <- as.matrix(control.cor.table)
  #case sample
  case.cor.table <- calc.pcc(STATE[1],period)
#   case.cor.table <- as.matrix(case.cor.table)
  
  model.size <- length(dnb.index)
  control.pcc.in <- as.vector(control.cor.table[dnb.index,dnb.index])
  control.pcc.out <- as.vector(control.cor.table[-dnb.index,dnb.index])
  rm(control.cor.table)
  
  case.pcc.in <- as.vector(case.cor.table[dnb.index,dnb.index])
  case.pcc.out <- as.vector(case.cor.table[-dnb.index,dnb.index])
  rm(case.cor.table)
  
  pcc.in.mean <- (sum(case.pcc.in,na.rm=TRUE)-model.size)/(sum(control.pcc.in,na.rm=TRUE)-model.size)
  
  pcc.out <- cbind(control.pcc.out,case.pcc.out)
  pcc.out <- pcc.out[order(-pcc.out[,1]),]
  out.index <- PCC.OUT.AMOUNT*model.size
  out.index <- ifelse(out.index<=nrow(pcc.out),out.index,nrow(pcc.out))
  pcc.out <- pcc.out[1:out.index,]
  pcc.out.mean <- mean(pcc.out[,2],na.rm=TRUE)/mean(pcc.out[,1],na.rm=TRUE)   
  
  ci.max <- pcc.in.mean*sd.mean/pcc.out.mean
  write.table(ci.max,
              paste(base.dir,author,"_",period,"_max_ci.txt",sep=""),
              row.names=FALSE,
              sep="\t",
              col.names=FALSE)
}

calcCI <- function(){
  # period <- 1
  # author <- "qiu"
  
  #calc Doc li's ci
  for (period in c(1,4)){
    calc.ci("li",period,paste("liver_DNB_t",period,sep=""))
  }
  
  # BASE.PATH <- "D:\\x\\"
  #calc my ci
  for (period in 1:PERIOD.COUNT) {
    calc.ci("qiu",period,paste("matrix_table_",period,"_dnb",sep=""))
  }
}

mergeCiInto1File  <- function(){
  setwd(BASE.PATH)
  
  #merge qiu's ci
  ci <- numeric(length = PERIOD.COUNT)
  periods <-1:PERIOD.COUNT
  for(i in periods){
    period.name <- paste("qiu_",i,"_max_ci.txt",sep="")
    ci[i] <- read.table(paste(period.name,sep=""))
  }
  ci.df <- cbind(as.character(periods),unlist(ci))
  ci.df <- t(ci.df)
  write.table(ci.df,"qiu_all_ci.txt",quote=FALSE,sep="\t"
              ,row.names=FALSE,col.names=FALSE)
  
  #merge li's ci
  ci.li <- numeric(length = PERIOD.COUNT)
  periods.li <- c(1,4)
  for(i in periods.li){
    period.name.li <- paste("li_",i,"_max_ci.txt",sep="")
    ci.li[i] <- read.table(period.name.li)
  }
  ci.df.li <- cbind(as.character(periods),unlist(ci.li))
  ci.df.li <- t(ci.df.li)
  write.table(ci.df.li,"li_all_ci.txt",quote=FALSE,sep="\t"
              ,row.names=FALSE,col.names=FALSE)

}

# 计算性能对比图
plot.ci <- function(){
  setwd(BASE.PATH)

  ci.df.qiu <- read.table("qiu_all_ci.txt",sep="\t")
  ci.df.li <- read.table("li_all_ci.txt",sep="\t")
  png("compare_ci.png")
  plot(as.integer(ci.df.qiu[1,]),ci.df.qiu[2,],
       xlab="period",
       ylab="ci",
       main="ci growth",
       type="b",
       lty=1,
       ylim=c(0,40),
       col="black")
  lines(as.integer(ci.df.li[1,]),ci.df.li[2,],
         col="red",type="b",lty=1)
  legend(x=4,y=40, legend=c("qiu's","li's"),
         col=c("black","red"),lty=c(1,1))
  dev.off()
}

setwd(BASE.PATH)
# calcCI()
# mergeCiInto1File()
plot.ci()
