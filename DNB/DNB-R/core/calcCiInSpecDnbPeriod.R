#! /usr/bin/Rscript --no-save
#
#' @description give a dnb period,get module gene ids ,calc its ci value in each period
#' @author : star qiu
#' @date 2014.8.1
#' 
#' 

BASE.PATH <- "~/z/"
# make sure all data are included in this directory
# BASE.PATH <- "D:\\x\\"

PERIOD.COUNT <- 4
PERIOD.SAMPLE.COUNT <- 3
# PERIOD.COUNT <- 5 
# PERIOD.SAMPLE.COUNT <- 5 
PCC.OUT.AMOUNT <- 50
DNB.PERIOD <- 4
HAS.CONTROL.EXAMPLE <- TRUE 
STATE <- c("case","control") 

init <- function(args){
  len <- length(args)
  for (i in seq(1,len,by=2)){
    set.key.value(args[i],args[i+1])
  }
}

set.key.value  <- function(key,value){
  switch(key,
         "-p" = ,
         "--base.path" = BASE.PATH <<- value,
         "--period.count" = PERIOD.COUNT <<- as.integer(value),
         "--period.sample.count" = PERIOD.SAMPLE.COUNT <<- as.integer(value),
         "--pcc.out.amount" = PCC.OUT.AMOUNT <<- as.integer(value),
         "--dnb.period" = DNB.PERIOD <<- as.integer(value),
         "--has.control.example" = HAS.CONTROL.EXAMPLE <<- as.logical(value)
  )
}

print.usage <- function(){
  cat("Usage: calcCiInSpecDnbPeriod.R [-h/--help |-p/--base.path directory] \n
      [--cur.file.dir directory] [--has.control.example]\n
      [--period.count number] [--period.sample.count integer]  \n
      [--pcc.out.amount integer]\n")
  cat("Details:\n")
  cat("\t -h/--help   show the usage of gdm4Par.R \n")
  cat("\t -p/--base.path   set the work space of program .  \n")
  cat("\t --has.control.example   if you have control example , set it TRUE,otherwise FALSE.\n
      the default is TRUE\n")
  cat("\t --period.count   set the number of periods  .
      the default is 5  \n")
  cat("\t --period.sample.count   set the number of samples in every period . 
      the default is 5 \n")
  cat("\t --pcc.out.amount  set the max number of the PCC between two modules 
      we select to calculate. the default is 50 \n")
  cat("Description:\n")
  cat("\t  if -h/--help is appeared,the other parameters is ignored.
      \t  if you have multiple case files, set --file.divided TRUE
      \t  if you want have more cores ,you can set it larger value ,
      the program may run faster.
      \t  change features.sd.threshold may have suprise. it's good encough
      to the data of rat's liver.
      \n")
}


calc.pcc <- function(state,period,base.dir=BASE.PATH){
  whole.table <- read.table(paste0(base.dir,
                                   paste(state,"matrix_table",period,sep="_"),
                                   ".txt"),
                            header=TRUE)
  #   geneIds <- whole.table[,1] #as the row names and column names of matrix
  whole.table <- whole.table[,c(2:(PERIOD.SAMPLE.COUNT+1))]
  trans.matrix <- t(as.matrix(whole.table)) #matrix Transpose
  cor.matrix <- abs(cor(trans.matrix))
}


calc.ci <- function (dnb.period,period,module.file.name,base.dir=BASE.PATH) {
  module.gene.ids <- read.table(paste(base.dir,module.file.name,".txt",sep=""))[,1]
  module.gene.ids <- as.character(module.gene.ids)
  
  case.data <- read.table(paste0(base.dir,
                                 paste(STATE[1],"matrix_table",period,sep="_"),
                                 ".txt"),
                          header=TRUE)
  dnb.index <- which(as.character(case.data[,1]) %in% module.gene.ids)
  case.data.dnb <- case.data[dnb.index,-1]
  rm(case.data)
  
  control.data <- read.table(paste0(base.dir,
                                    paste(STATE[2],"matrix_table",period,sep="_"),
                                    ".txt"),
                             header=TRUE)
  control.data.dnb <- control.data[dnb.index,-1]
  rm(control.data)
  
  case.sd <- apply(case.data.dnb,1,sd)
  control.sd <- apply(control.data.dnb,1,sd)
  sd.mean <- mean(case.sd,na.rm=TRUE) / mean(control.sd,na.rm=TRUE)
  rm(case.sd)
  rm(control.sd)
  
  #control sample 
  control.cor.table <- calc.pcc(STATE[2],period)
  #case sample
  case.cor.table <- calc.pcc(STATE[1],period)
  
  model.size <- length(dnb.index)
  control.pcc.in <- as.vector(control.cor.table[dnb.index,dnb.index])
  control.pcc.out <- as.vector(control.cor.table[-dnb.index,dnb.index])
  rm(control.cor.table)
  
  case.pcc.in <- as.vector(case.cor.table[dnb.index,dnb.index])
  case.pcc.out <- as.vector(case.cor.table[-dnb.index,dnb.index])
  rm(case.cor.table)
  gc()
  
  pcc.in.mean <- (sum(case.pcc.in,na.rm=TRUE)-model.size)/(sum(control.pcc.in,na.rm=TRUE)-model.size)
  
  pcc.out <- cbind(control.pcc.out,case.pcc.out)
  pcc.out <- pcc.out[order(-pcc.out[,1]),]
  out.index <- PCC.OUT.AMOUNT*model.size
  out.index <- ifelse(out.index<=nrow(pcc.out),out.index,nrow(pcc.out))
  pcc.out <- pcc.out[1:out.index,]
  pcc.out.mean <- mean(pcc.out[,2],na.rm=TRUE)/mean(pcc.out[,1],na.rm=TRUE)   
  
  ci.max <- pcc.in.mean*sd.mean/pcc.out.mean
  write.table(ci.max,
              paste0(base.dir,
                     paste("max_ci",dnb.period,period,sep="_"),
                     ".txt"),
              row.names=FALSE,
              sep="\t",
              col.names=FALSE)
  gc()
}
calc.ci.with.one.state <- function (dnb.period,period,module.file.name,base.dir=BASE.PATH) {
  module.gene.ids <- read.table(paste(base.dir,module.file.name,".txt",sep=""))[,1]
  module.gene.ids <- as.character(module.gene.ids)
  
  case.data <- read.table(paste0(base.dir,
                                 paste(STATE[1],"matrix_table",period,sep="_"),
                                 ".txt"),
                          header=TRUE)
  dnb.index <- which(as.character(case.data[,1]) %in% module.gene.ids)
  case.data.dnb <- case.data[dnb.index,-1]
  rm(case.data)
  
  case.sd <- apply(case.data.dnb,1,sd)
  sd.mean <- mean(case.sd,na.rm=TRUE)
  rm(case.sd)

  #case sample
  case.cor.table <- calc.pcc(STATE[1],period)
  
  model.size <- length(dnb.index)
  case.pcc.in <- as.vector(case.cor.table[dnb.index,dnb.index])
  case.pcc.out <- as.vector(case.cor.table[-dnb.index,dnb.index])
  rm(case.cor.table)
  
  pcc.in.mean <- sum(case.pcc.in,na.rm=TRUE)-model.size
  
  case.pcc.out <- case.pcc.out[order(-case.pcc.out)]
  out.index <- PCC.OUT.AMOUNT*model.size
  out.index <- ifelse(out.index<length(case.pcc.out),out.index,length(case.pcc.out))
  case.pcc.out <- case.pcc.out[1:out.index]
  pcc.out.mean <- mean(case.pcc.out,na.rm=TRUE)
  
  ci.max <- pcc.in.mean*sd.mean/pcc.out.mean
  write.table(ci.max,
              paste0(base.dir,
                     paste("max_ci",dnb.period,period,sep="_"),
                     ".txt"),
              row.names=FALSE,
              sep="\t",
              col.names=FALSE)
}

calcCI <- function(){
  
  if(HAS.CONTROL.EXAMPLE){
    for (period in 1:PERIOD.COUNT) {
      calc.ci(DNB.PERIOD,
              period,
              paste("matrix_table",DNB.PERIOD,"dnb",sep="_"))
    }
  }else{
    for (period in 1:PERIOD.COUNT) {
      calc.ci.with.one.state(DNB.PERIOD,
              period,
              paste("matrix_table",DNB.PERIOD,"dnb",sep="_"))
    }
  }
  
}

mergeCiInto1File  <- function(){
  setwd(BASE.PATH)
  
  #merge ci
  ci <- numeric(length = PERIOD.COUNT)
  periods <-1:PERIOD.COUNT
  for(period in periods){
    period.name <- paste0(paste("max_ci",DNB.PERIOD,period,sep="_"),
                          ".txt")
    ci[period] <- read.table(period.name)
  }
  ci.df <- cbind(as.character(periods),unlist(ci))
  ci.df <- t(ci.df)
  write.table(ci.df,
              paste0(paste("all_ci",DNB.PERIOD,sep="_"),
                     ".txt"),
              quote=FALSE,
              sep="\t",
              row.names=FALSE,
              col.names=FALSE)
}

main <- function(){
  
  args <- commandArgs(TRUE)
  print(args)
  if ((length(args) %% 2 != 0) ){
    print.usage()
  }else {
    if(length(args) != 0){
      init(args)
    }
  }
  
  setwd(BASE.PATH)
  calcCI()
  mergeCiInto1File()
}
# system.time(main())
main()

