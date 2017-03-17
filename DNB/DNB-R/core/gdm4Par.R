#! /usr/bin/Rscript --no-save
#
#' @author : star qiu
#' @date 2014.8.1
#' 
#' 

##install necessary packages if not installed yet.
options(repos='http://cran.r-project.org') 
necessary <- c('plyr','FisherEM')
installed <- necessary %in% installed.packages()[, 'Package']
if (length(necessary[!installed]) >=1)
  install.packages(necessary[!installed])

library(plyr)
library(FisherEM)
# library(fpc)

# CUR.FILE.DIR <- NULL # current file directory
CUR.FILE.DIR <- "~/DNBWorkspace/DetectAndAnalysisDNB/src/main/resources/core"
# BASE.PATH <- "./"
# CASE.FILE.PATH <- NULL
# CONTROL.FILE.PATH <- NULL

# windows
# BASE.PATH <- "D:\\x\\"
# CASE.FILE.PATH <- "D:\\data\\sourceData\\liver_case_data.txt"
# CONTROL.FILE.PATH <- "D:\\data\\sourceData\\liver_control_data.txt"

# linux
BASE.PATH <- "~/x/"
CASE.FILE.PATH <- "/host/data/sourceData/liver_case_data.txt"
CONTROL.FILE.PATH <- "/host/data/sourceData/liver_control_data.txt"

# FILE.NAME <- "GSE64538_labeled.txt"
# PERIOD.COUNT <- 4 # the number of periods
# PERIOD.SAMPLE.COUNT <- 3 # the number of samples in every period
# FEATURES.SD.THRESHOLD <- 0.001 # the threshold of sd to select


# FILE.NAME <- "liver_labeled_data.txt"
PERIOD.COUNT <- 5 # the number of periods
PERIOD.SAMPLE.COUNT <- 5 # the number of samples in every period
FEATURES.SD.THRESHOLD <- 0.001 # the threshold of sd to select

CLUSTER.NUMBER <- 30 # the numbers of cluster
PCC.OUT.AMOUNT <- 50 # the number of pcc out we choose to calculate

STATE <- c("case","control") #case is abnormal,control is normal
STATE.COUNT <- 2 #
FILE.DEVIDED  <- FALSE #case or control file is divided?
CORES <- 6
# you can add cluster method by creating a file named paste0("algo_",CLUSTER.METHOD,".R)
# and the file should have a getCluster(data,cluster.number) method
CLUSTER.METHOD <- "hclust" 

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
         "--cur.file.dir" = CUR.FILE.DIR <<- value,
         "--file.divided" = FILE.DEVIDED <<- as.logical(value),
         "--case.file.path" = CASE.FILE.PATH <<- value,
         "--control.file.path" = CONTROL.FILE.PATH <<- value,
         "--period.count" = PERIOD.COUNT <<- as.integer(value),
         "--period.sample.count" = PERIOD.SAMPLE.COUNT <<- as.integer(value),
         "--features.sd.threshold" = FEATURES.SD.THRESHOLD <<- as.numeric(value),
         "--cluster.method" = CLUSTER.METHOD <<- value,
         "--cluster.number" = CLUSTER.NUMBER <<- as.integer(value),
         "--pcc.out.amount" = PCC.OUT.AMOUNT <<- as.integer(value),
         "--cores" = CORES <<- as.integer(value)
  )
}

print.usage <- function(){
  cat("Usage: gdm4Par.R [-h/--help |-p/--base.path directory] \n
      [--cur.file.dir directory] \n
      [--file.divided boolean]\n
      [-case.file.path file] [-control.file.path file]  \n
      [--period.count number] [--period.sample.count integer]  \n
      [--features.sd.threshold float] \n
      [--cluster.method string]  [--cluster.number integer] \n
      [--pcc.out.amount integer] [cores integer]\n")
  cat("Details:\n")
  cat("\t -h/--help   show the usage of gdm4Par.R \n")
  cat("\t -p/--base.path   set the work space of program .  \n")
  cat("\t -p/--cur.file.dir   set the current file  directory \n")
  cat("\t --file.divided   if you have multiple case files, set it TRUE,otherwise FALSE.\n
      the default is FALSE.\n")
  cat("\t --case.file.path   set the path of case data file, case is abnormal data,\n
        if you have multiple case files,use ; split them.\n")
  cat("\t --control.file.path   set the path of control data file, control is normal data,\n
       if you have multiple control files,use ; split them.\n")
  cat("\t --period.count   set the number of periods  .
      the default is 5  \n")
  cat("\t --period.sample.count   set the number of samples in every period . 
      the default is 5 \n")
  cat("\t --features.sd.threshold   set the threshold of filtering SD
      the default is 0.001 \n")
  cat("\t --cluster.method   set the name of cluster method,
       \t the default is hclust(Hierarchical cluster analysis) \n")
  cat("\t --cluster.number   set the number of cluster ,the default is 30. \n")
  cat("\t --pcc.out.amount  set the max number of the PCC between two modules 
      we select to calculate. the default is 50 \n")
  cat("\t --cores  set the number of cores we use for parallel program 
      the default is 6 \n")
  cat("Description:\n")
  cat("\t  if -h/--help is appeared,the other parameters is ignored.
      \t  if you have multiple case files, set --file.divided TRUE
      \t  if you want have more cores ,you can set it larger value ,
      the program may run faster.
      \t  change features.sd.threshold may have suprise. it's good encough
      to the data of rat's liver.
      \n")
}

divide.files.by.periods <- function(state,file.path){
  matrix.table <- read.table(file.path,header=TRUE,sep="")
  period.name <- ""
  z <- c((1-PERIOD.SAMPLE.COUNT):1)  
  
  for(i in 1:PERIOD.COUNT)  {
    z <- z+PERIOD.SAMPLE.COUNT
    z[1]<-1 #row name
    #     print(z)
    period.name <- paste0(state,"_matrix_table_",i,".txt")
    # the matrix in each state in every period
    write.table(matrix.table[z],file=period.name,
                row.names = FALSE,
                sep="\t")
  }
}

sd.test <- function(case.file.name,control.file.name,
                    file.name,features.sd.threshold=0.001){
  case.period.matrix.table <- read.table(case.file.name,header=TRUE,sep="")  
  control.period.matrix.table <- read.table(control.file.name,header=TRUE,sep="")  
  
  z.case <- c(2:ncol(case.period.matrix.table))
  z.control <- c(2:ncol(control.period.matrix.table))
  
  case.sd <- apply(case.period.matrix.table[,z.case],1,sd) 
  control.sd <- apply(control.period.matrix.table[,z.control],1,sd)
  
  no.zero.index <- which((case.sd != 0) & (control.sd != 0))
  
  gene.sd <- case.sd[no.zero.index]/control.sd[no.zero.index]
  gene.sd.log <- log(gene.sd)
  gene.sd.log.p <- unlist(lapply(gene.sd.log,pnorm,mean=mean(gene.sd.log),sd=sd(gene.sd.log)))
  high.sd.index <- which((gene.sd.log.p <= features.sd.threshold) | (gene.sd.log.p >= (1-features.sd.threshold))) 
  source.high.sd.index <- no.zero.index[high.sd.index]
  #li's method
  #   sd.log.threshold <- pnorm(features.sd.threshold/2,mean=mean(gene.sd.log),sd=sd(gene.sd.log))
  #   high.sd.index <- which(abs(gene.sd.log) >= sd.log.threshold)
  
  #  all genes 
  write.table(case.period.matrix.table[,1],
              paste0(file.name,"_all_genes.txt"),
              row.names=FALSE,
              quote = FALSE,
              sep="\t")
  # the valid genes 
  write.table(case.period.matrix.table[no.zero.index,1],
              paste0(file.name,"_genes.txt"),
              row.names=FALSE,
              quote = FALSE,
              sep="\t")
  # the sd of genes 
  write.table(gene.sd,
              paste0(file.name,"_sd.txt"),
              row.names=FALSE,
              sep="\t")
  # the sd of genes which has a big value
  write.table(gene.sd[high.sd.index],
              paste0(file.name,"_high_sd.txt"),
              row.names=FALSE,
              sep="\t")
  # the sd of case data which has a big value
  write.table(case.sd[source.high.sd.index],
              paste0("case_",file.name,"_high_sd.txt"),
              row.names=FALSE,
              sep="\t")
  # the sd of control data which has a big value
  write.table(control.sd[source.high.sd.index],
              paste0("control_",file.name,"_high_sd.txt"),
              row.names=FALSE,
              sep="\t")
  # the case data whose sd has a big value
  write.table(case.period.matrix.table[source.high.sd.index,],
              paste0("case_",file.name,"_with_high_sd.txt"),
              row.names=FALSE,
              sep="\t")
  # the  control data whose sd has a big value
  write.table(control.period.matrix.table[source.high.sd.index,],
              paste0("control_",file.name,"_with_high_sd.txt"),
              row.names=FALSE,
              sep="\t")
}

sd.test.with.one.state <- function(case.file.name, file.name, features.sd.threshold=0.001){
  case.period.matrix.table <- read.table(case.file.name,header=TRUE,sep="")  
  
  z.case <- c(2:ncol(case.period.matrix.table))
  
  case.sd <- apply(case.period.matrix.table[,z.case],1,sd) 
  
  no.zero.index <- which(case.sd != 0)
  gene.sd <- case.sd
  gene.sd.log <- log(gene.sd)
  gene.sd.log.p <- unlist(lapply(gene.sd.log,pnorm,mean=mean(gene.sd.log),sd=sd(gene.sd.log)))
  high.sd.index <- which((gene.sd.log.p <= features.sd.threshold) | (gene.sd.log.p >= (1-features.sd.threshold))) 
  source.high.sd.index <- no.zero.index[high.sd.index]
  #li's method
  #   sd.log.threshold <- pnorm(features.sd.threshold/2,mean=mean(gene.sd.log),sd=sd(gene.sd.log))
  #   high.sd.index <- which(abs(gene.sd.log) >= sd.log.threshold)
  
  # the valid genes 
  write.table(case.period.matrix.table[no.zero.index,1],
              paste0(file.name,"_genes.txt"),
              row.names=FALSE,
              sep="\t")
  # the sd of genes 
  write.table(gene.sd,
              paste0(file.name,"_sd.txt"),
              row.names=FALSE,
              sep="\t")
  # the sd of genes which has a big value
  write.table(gene.sd[high.sd.index],
              paste0(file.name,"_high_sd.txt"),
              row.names=FALSE,
              sep="\t")
  # the sd of case data which has a big value
  write.table(case.sd[source.high.sd.index],
              paste0("case_",file.name,"_high_sd.txt"),
              row.names=FALSE,
              sep="\t")
  # the case data whose sd has a big value
  write.table(case.period.matrix.table[source.high.sd.index,],
              paste0("case_",file.name,"_with_high_sd.txt"),
              row.names=FALSE,
              sep="\t")
}

get.filter.table.with.high.sd <- function(state,period){
  filter.table <- read.table(paste0(state,"_matrix_table_",period,"_with_high_sd.txt"),
                             header=TRUE,sep="")
  geneIds <- filter.table[,1] #as the row names and column names of matrix
  filter.table <- filter.table[,c(2:ncol(filter.table))]
  rownames(filter.table) <- geneIds;
  filter.table
}

calc.pcc.with.filter.table <- function(filter.table){
  trans.matrix <- t(filter.table) #matrix Transpose
  cor.matrix <- abs(cor(trans.matrix))
  colnames(cor.matrix) <- colnames(trans.matrix)
  cor.matrix
}

calc.pcc.with.state.and.period <- function(state,period){
  filter.table <- get.filter.table.with.high.sd(state,period)
  calc.pcc.with.filter.table(filter.table)
}

# getCluster <- function(data,cluster.number=30){
#   clust.result <- fem(data)
#   clust.result$cls
# }


#generate DNB 
pcc.test <- function(period){
  control.cor.table <- calc.pcc.with.state.and.period(STATE[2],period)
  genes <- colnames(control.cor.table)
  genes.number <- length(genes)
  genes.index <- 1:genes.number

  case.data <- get.filter.table.with.high.sd(STATE[1],period)
  case.cor.table <- calc.pcc.with.filter.table(case.data)
  
  cluster <- getCluster(case.data, CLUSTER.NUMBER) # this method is in algo_**.R file
  
  case.sd <- read.table(paste0("case_matrix_table_",period,"_high_sd.txt"),
                        header=TRUE,
                        sep="")
  control.sd <- read.table(paste0("control_matrix_table_",period,"_high_sd.txt"),
                           header=TRUE,
                           sep="")
  
  df.with.cluster.genes.sds <- cbind(cluster,genes.index,case.sd,control.sd)
  colnames(df.with.cluster.genes.sds) <-c("cluster","genes.index","case.sd","control.sd")
  df.aggr.by.cluster <- ddply(df.with.cluster.genes.sds,.(cluster),summarize,
                              models = paste(genes.index,collapse=","),
                              sd = mean(case.sd)/mean(control.sd))
  colnames(df.aggr.by.cluster) <-c("cluster","models","sd")
  
  cluster.aggr <- df.aggr.by.cluster$cluster
  models <- df.aggr.by.cluster$models
  cluster.number <- length(cluster.aggr)
  
  
  #the diag of table is meaningless
  diag(control.cor.table) <- NA
  diag(case.cor.table) <- NA
  
  pcc.in.mean <- numeric()
  pcc.out.mean <- numeric()
  
  if(cluster.number < 2){
    stop("the number of cluster is  less than 2,cluster failed")
  }
  
  for(cluster.index in 1:cluster.number){
    cur.model <- as.integer(unlist(strsplit(as.character(models[cluster.index]),",")))
    model.size <- length(cur.model)
    control.pcc.in <- as.vector(control.cor.table[cur.model,cur.model])
    case.pcc.in <- as.vector(case.cor.table[cur.model,cur.model])
    
    control.pcc.out <- as.vector(control.cor.table[-cur.model,cur.model])
    case.pcc.out <- as.vector(case.cor.table[-cur.model,cur.model])
    
    pcc.in.mean[cluster.index] <- (sum(case.pcc.in,na.rm=TRUE)-model.size)/(sum(control.pcc.in,na.rm=TRUE)-model.size)
    
    pcc.out <- cbind(control.pcc.out,case.pcc.out)
    pcc.out <- pcc.out[order(-pcc.out[,1]),]
    out.index <- PCC.OUT.AMOUNT*model.size
    out.index <- ifelse(out.index<=nrow(pcc.out),out.index,nrow(pcc.out))
    pcc.out <- pcc.out[1:out.index,]
    pcc.out.mean[cluster.index] <- mean(pcc.out[,2],na.rm=TRUE)/mean(pcc.out[,1],na.rm=TRUE)   
  }
  ci <- pcc.in.mean*(df.aggr.by.cluster$sd)/pcc.out.mean
  
  # the final CI value in the period
  ci.max <- max(ci)
  write.table(ci.max,
              paste0("matrix_table_",period,"_max_ci.txt"),
              row.names=FALSE,
              sep="\t",
              col.names=FALSE)
  
  # this is the gene ids in  'DNB' ,every period have a 'DNB' ,
  # but the real DNB is whose CI value is the maxima
  max.model <<- genes[as.integer(unlist(strsplit(as.character(models[which.max(ci)]),",")))]
  #   print(max.model)
  #write the dnbs in current period
  write.table(max.model,
              paste0("matrix_table_",period,"_dnb.txt"),
              row.names=FALSE,
              sep="\t",
              col.names=FALSE,
              quote=FALSE)
}

#generate DNB  for one state
pcc.test.with.one.state <- function(period){
  case.data <- get.filter.table.with.high.sd(STATE[1],period)
  case.cor.table <- calc.pcc.with.filter.table(case.data)
  
  genes <- colnames(case.cor.table)
  genes.number <- length(genes)
  genes.index <- 1:genes.number
  
  cluster <- getCluster(case.data, CLUSTER.NUMBER) # this method is in algo_**.R file
  
  case.sd <- read.table(paste0("case_matrix_table_",period,"_high_sd.txt"),
                        header=TRUE,
                        sep="")
  
  df.with.cluster.genes.sds <- cbind(cluster,genes.index,case.sd)
  colnames(df.with.cluster.genes.sds) <-c("cluster","genes.index","case.sd")
  df.aggr.by.cluster <- ddply(df.with.cluster.genes.sds,.(cluster),summarize,
                              models = paste(genes.index,collapse=","),
                              sd = mean(case.sd))
  colnames(df.aggr.by.cluster) <-c("cluster","models","sd")
  
  cluster.aggr <- df.aggr.by.cluster$cluster
  models <- df.aggr.by.cluster$models
  cluster.number <- length(cluster.aggr)
  
  
  #the diag of table is meaningless
  diag(case.cor.table) <- NA
  
  pcc.in.mean <- numeric()
  pcc.out.mean <- numeric()
  
  for(cluster.index in 1:cluster.number){
    cur.model <- as.integer(unlist(strsplit(as.character(models[cluster.index]),",")))
    model.size <- length(cur.model)
    case.pcc.in <- as.vector(case.cor.table[cur.model,cur.model])
    
    case.pcc.out <- as.vector(case.cor.table[-cur.model,cur.model])
    
    pcc.in.mean[cluster.index] <- sum(case.pcc.in,na.rm=TRUE)-model.size
    
    case.pcc.out <- case.pcc.out[order(-case.pcc.out)]
    out.index <- PCC.OUT.AMOUNT*model.size
    out.index <- ifelse(out.index<length(case.pcc.out),out.index,length(case.pcc.out))
    case.pcc.out <- case.pcc.out[1:out.index]
    pcc.out.mean[cluster.index] <- mean(case.pcc.out,na.rm=TRUE)
  }
  ci <- pcc.in.mean*(df.aggr.by.cluster$sd)/pcc.out.mean
  
  # the final CI value in the period
  ci.max <- max(ci)
  write.table(ci.max,
              paste0("matrix_table_",period,"_max_ci.txt"),
              row.names=FALSE,
              sep="\t",
              col.names=FALSE)
  
  # this is the gene ids in  'DNB' ,every period have a 'DNB' ,
  # but the real DNB is whose CI value is the maxima
  max.model <<- genes[as.integer(unlist(strsplit(as.character(models[which.max(ci)]),",")))]
  #   print(max.model)
  #write the dnbs in current period
  write.table(max.model,
              paste0("matrix_table_",period,"_dnb.txt"),
              row.names=FALSE,
              sep="\t",
              col.names=FALSE,
              quote=FALSE)
}

#find the maxima values of an arrayL
findMaxima <- function(array){
  which(diff(c(1,sign(diff(array)),-1)) == -2)
}

plot.ci <- function(){
  
  ci <<- numeric()# this is the final CI result of all periods
  periods <-1:PERIOD.COUNT
  for(i in periods){
    
    period.name <- paste0("matrix_table_",i,"_max_ci.txt")
    ci[i] <<- read.table(period.name)
  }
  names(ci) <<- as.character(seq(length(ci)))
  print("ci table:")
  print(as.table(unlist(ci)))
  write.table(ci,
              "all_ci.txt",
              row.names=FALSE,
              sep="\t",
              col.names=names(ci),
              quote=FALSE)
  ci.maxima.index <- findMaxima(unlist(ci))# this is period index where DNB in
  print("ci maxima index:")
  names(ci.maxima.index) <- as.character(ci.maxima.index)
  print(ci.maxima.index)
  write.table(t(ci.maxima.index),
              "ci_maxima_index.txt",
              row.names=FALSE,
              sep="\t",
              col.names=FALSE,
              quote=FALSE)
  png("ci.png")
  plot(periods,unlist(ci),
       xlab="period ",
       ylab="ci",
       main="ci growth",
       type="b")
  dev.off()
}

gdm <- function(){
  
  if(is.null(CASE.FILE.PATH)){
    stop("you should set --case.file.path")
  }else{
    if(is.null(CONTROL.FILE.PATH)){
      STATE.COUNT <<- 1 #no control data
    }
  }
  
  #   registerDoParallel(cores=CORES)  
  case.file.list <- NULL#an array with case files in all periods 
  control.file.list <- NULL#an array with control files in all periods 
  if(!FILE.DEVIDED){
    divide.files.by.periods(STATE[1],CASE.FILE.PATH)
    case.file.list <- paste0("case_matrix_table_",1:PERIOD.COUNT,".txt")
  }else{
    case.file.list <- strsplit(CASE.FILE.PATH,";")[[1]]
  }
  
  if(STATE.COUNT == 2){
    
    if(!FILE.DEVIDED){
      divide.files.by.periods(STATE[2],CONTROL.FILE.PATH)
      control.file.list <- paste0("control_matrix_table_",1:PERIOD.COUNT,".txt")
    }else{
      control.file.list <- strsplit(CONTROL.FILE.PATH,";")[[1]]
    }
    
    for (period in 1:PERIOD.COUNT) {
      file.name <- paste0("matrix_table_",period)
      sd.test(case.file.name = case.file.list[period],
              control.file.name = control.file.list[period],
              file.name=file.name,
              features.sd.threshold=FEATURES.SD.THRESHOLD)
      pcc.test(period)
    }
  }else{# one state
    for (period in 1:PERIOD.COUNT) {
      file.name <- paste0("matrix_table_",period)
      sd.test.with.one.state(case.file.name = case.file.list[period],
                             file.name=file.name,
                             features.sd.threshold=FEATURES.SD.THRESHOLD)
      pcc.test.with.one.state(period)
    }
  }
  plot.ci()
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
    
    #get cluster method
    print(CLUSTER.METHOD)
    print(CUR.FILE.DIR)
    if(is.null(CUR.FILE.DIR)){# execute this file directly, not via source() in other file
      CUR.FILE.DIR <- dirname(sys.frame(1)$ofile) #get current file directory
    }
    print(CUR.FILE.DIR)
    if(is.null(CUR.FILE.DIR)){
      stop("you should set current file directory by using --cur.file.dir")
    }
    source(file.path(CUR.FILE.DIR,paste0("algo_",CLUSTER.METHOD,".R")))
    
    setwd(BASE.PATH)
    print(paste("working directory : " , BASE.PATH))
    
    gdm()
  }
}
# main()
system.time(main())
