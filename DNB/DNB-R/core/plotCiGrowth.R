# give a module gene ids ,calc its ci value

# BASE.PATH <- "/host/data/"
# make sure all data are included in this directory
# BASE.PATH <- "D:\\x\\"
BASE.PATH <- "~/x/"

PERIOD.COUNT <- 5 #we have 5 periods:4wk,8wk,12wk,16wk,20wk
PERIOD.SAMPLE.SEP <- 10 #each period has 10 samples
PERIOD.SAMPLE.COUNT <- 5 # divide into case and WKY, each have 5 samples 
PCC.OUT.AMOUNT <- 50
STATE <- c("case","control") 

calc.pcc <- function(state,period,base.dir=BASE.PATH){
  whole.table <- read.table(paste0(base.dir,state,"_matrix_table_",period,".txt"),
                            header=TRUE,sep="")
  #   geneIds <- whole.table[,1] #as the row names and column names of matrix
  whole.table <- whole.table[,c(2:(PERIOD.SAMPLE.COUNT+1))]
  trans.matrix <- t(as.matrix(whole.table)) #matrix Transpose
  cor.matrix <- abs(cor(trans.matrix))
  #   rownames(cor.matrix) <- geneIds
  #   colnames(cor.matrix) <- geneIds
  #   cor.matrix
}


calc.ci <- function (author,state,dnb.period,period,dnb.file.name,base.dir=BASE.PATH) {
  module.gene.ids <- read.table(paste0(base.dir,dnb.file.name,".txt"))[,1]
  module.gene.ids <- as.character(module.gene.ids)
  
  data <- read.table(paste(base.dir,state,"_matrix_table_",period,".txt",sep=""),
                          header=TRUE,sep="")
  dnb.index <- which(as.character(data[,1]) %in% module.gene.ids)
  data.dnb <- data[dnb.index,-1]
  rm(data)
  
  data.sd <- apply(data.dnb,1,sd)
  sd.mean <- mean(data.sd,na.rm=TRUE)
  rm(data.sd)
  
  cor.table <- calc.pcc(state,period)
  
  model.size <- length(dnb.index)
  pcc.in <- as.vector(cor.table[dnb.index,dnb.index])
  pcc.out <- as.vector(cor.table[-dnb.index,dnb.index])
  rm(cor.table)
  
  pcc.in.mean <- mean(pcc.in,na.rm=TRUE)
  
  pcc.out <- pcc.out[order(-pcc.out)]
  out.index <- PCC.OUT.AMOUNT*model.size
  out.index <- ifelse(out.index<=length(pcc.out),out.index,nrow(pcc.out))
  pcc.out <- pcc.out[1:out.index]
  pcc.out.mean <- mean(pcc.out,na.rm=TRUE) 
  
  ci.max <- pcc.in.mean*sd.mean/pcc.out.mean
  
  write.table(ci.max,
              paste0(base.dir,paste(author,state,dnb.period,period,"max_ci.txt" ,sep = "_")),
              row.names=FALSE,
              sep="\t",
              col.names=FALSE)
}

calcCI <- function(){
  # period <- 1
  # author <- "qiu"
  
  #calc Doc li's ci
  for (dnb.period in c(1,4)){
    for (period in 1:PERIOD.COUNT) {
      for (state in STATE){
        calc.ci("li",state,dnb.period,period,paste0("liver_DNB_t",dnb.period))
      }
    }
  }
  
  # BASE.PATH <- "D:\\x\\"
  #calc my ci
  for (dnb.period in 1:PERIOD.COUNT) {
    for (period in 1:PERIOD.COUNT) {
      for (state in STATE){
        calc.ci("qiu",state,dnb.period,period,paste0("matrix_table_",dnb.period,"_dnb"))
      }
    }
  }
}

mergeCiInto1File  <- function(author,state,dnb.period){
  setwd(BASE.PATH)
  
  #merge qiu's ci
  ci <- numeric(length = PERIOD.COUNT)
  periods <-1:PERIOD.COUNT
  for(i in periods){
    period.name <- paste(author,state,dnb.period,i,"max_ci.txt",sep="_")
    ci[i] <- read.table(paste(period.name,sep=""))
  }
  ci.df <- cbind(as.character(periods),unlist(ci))
  ci.df <- t(ci.df)
  write.table(ci.df,paste(author,state,dnb.period,"all_ci.txt",sep="_"),quote=FALSE,sep="\t"
              ,row.names=FALSE,col.names=FALSE)
  
  #merge li's ci
#   ci.li <- numeric(length = PERIOD.COUNT)
#   periods.li <- c(1,4)
#   for(i in periods.li){
#     period.name.li <- paste("li",state,dnb.period,i,"max_ci.txt",sep="_")
#     ci.li[i] <- read.table(period.name.li)
#   }
#   ci.df.li <- cbind(as.character(periods),unlist(ci.li))
#   ci.df.li <- t(ci.df.li)
#   write.table(ci.df.li,paste("li",state,dnb.period,"all_ci.txt",sep="_"),quote=FALSE,sep="\t"
#               ,row.names=FALSE,col.names=FALSE)
  
}

generate.states.ci <- function(author,dnb.periods){
  for(dnb.period in dnb.periods){
    for (state in STATE){
      mergeCiInto1File(author,state,dnb.period)
    }
  }
}

plot.ci.with.dnb.period <- function(author,dnb.period){
  setwd(BASE.PATH)
  
  case.ci.df<- read.table(paste(author,"case",dnb.period,"all_ci.txt",sep="_"),sep="\t")
  control.ci.df <- read.table(paste(author,"control",dnb.period,"all_ci.txt",sep="_"),sep="\t")
  
  max.val <- max(as.numeric(c(case.ci.df[2,],control.ci.df[2,])))
  
  # ci.df.li <- read.table("li_all_ci.txt",sep="\t")
  png(paste(author,dnb.period,"compare_ci.png",sep = "_"))
  plot(as.integer(case.ci.df[1,]),case.ci.df[2,],
       xlab="period",
       ylab="ci",
       main="ci growth",
       type="b",
       lty=1,
       ylim=c(0,max.val),
       col="red")
  lines(as.integer(control.ci.df[1,]),control.ci.df[2,],
        col="black",type="b",lty=1)
  legend(x=4,y=max.val, legend=c("case","control"),
         col=c("red","black"),lty=c(1,1))
  dev.off()
}


plot.ci <- function(author,dnb.periods){
  for(dnb.period in dnb.periods){
    plot.ci.with.dnb.period(author,dnb.period)
  }
}

generate.and.plot.states.ci <- function(author,dnb.periods){
  generate.states.ci(author,dnb.periods)
  plot.ci(author,dnb.periods)
}

setwd(BASE.PATH)
# calcCI()
generate.and.plot.states.ci("li",c(1,4))
generate.and.plot.states.ci("qiu",1:PERIOD.COUNT)
# generate.states.ci("li",c(1,4))
# plot.ci("li",c(1,4))
