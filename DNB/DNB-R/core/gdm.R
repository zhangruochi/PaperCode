#!  /usr/bin/Rscript --no-save
#
#' @author : star qiu
#' @date 2014.8.1
#' 
#' 
library(plyr)

#CASE.FILE.NAME <- "case_data.txt"
# CONTROL.FILE.NAME <- "control_data.txt"
CASE.FILE.NAME <- NULL
CONTROL.FILE.NAME <- NULL


# FILE.NAME <- "GSE64538_labeled.txt"
# PERIOD.COUNT <- 4 # the number of periods
# PERIOD.SAMPLE.COUNT <- 3 # the number of samples in every period
# FEATURES.SD.THRESHOLD <- 0.001 # the threshold of sd to select


# FILE.NAME <- "liver_labeled_data.txt"
PERIOD.COUNT <- 5 # the number of periods
PERIOD.SAMPLE.COUNT <- 5 # the number of samples in every period
FEATURES.SD.THRESHOLD <- 0.001 # the threshold of sd to select

CLUSTER.HCLUST.H <- 0.75 # the cluster parameter
PCC.OUT.AMOUNT <- 50 # the number of pcc out we choose to calculate

STATE <- c("case","control") #case is abnormal,control is normal
STATE.COUNT <- 2 #

init <- function(args){
  len <- length(args)
  for (i in seq(1,len,by=2)){
    set.key.value(args[i],args[i+1])
  }
}

set.key.value  <- function(key,value){
  switch(key,
         "--case.file.name" = CASE.FILE.NAME <<- value,
         "--control.file.name" = CONTROL.FILE.NAME <<- value,
         "--period.count" = PERIOD.COUNT <<- as.integer(value),
         "--period.sample.count" = PERIOD.SAMPLE.COUNT <<- as.integer(value),
         "--features.sd.threshold" = FEATURES.SD.THRESHOLD <<- as.numeric(value),
         "--cluster.hclust.h" = CLUSTER.HCLUST.H <<- as.numeric(value),
         "--pcc.out.amount" = PCC.OUT.AMOUNT <<- as.integer(value),
  )
}

print.usage <- function(){
  cat("Usage: gdm4Par.R [-h/--help ] [-control.file.name file]\n
      [-case.file.name file]  [--period.count number] \n
      [--period.sample.count number]  \n
      [--features.sd.threshold float] [--cluster.hclust.h float] \n
      [--pcc.out.amount number] \n")
  cat("Details:\n")
  cat("\t -h/--help   show the usage of gdm4Par.R \n")
  cat("\t --case.file.name   set the name of case data file, case is abnormal data,\n
      this file should be in ./sourceData directory.  \n")
  cat("\t --control.file.name   set the name of case data file, control is normal data,\n
      this file should be in ./sourceData directory.  \n")
  cat("\t --period.count   set the number of periods  .
      the default is 5  \n")
  cat("\t --period.sample.count   set the number of samples in every period . 
      the default is 5 \n")
  cat("\t --features.sd.threshold   set the threshold of filtering SD
      the default is 0.001 \n")
  cat("\t --cluster.hclust.h   set the h value when we call the cutree function
      the default is 0.75 \n")
  cat("\t --pcc.out.amount  set the max number of the PCC between two modules 
      we select to calculate. the default is 50 \n")
  cat("Description:\n")
  cat("\t  if -h/--help is appeared,the other parameters is ignored. 
      \t  if you want have more cores ,you can set it larger value ,
      the program may run faster.
      \t  change features.sd.threshold may have suprise. it's good encough
      to the data of rat's liver.
      \n")
}

divide.files.by.periods <- function(state,file.name){
  matrix.table <- read.table(file.path("sourceData",file.name),
                             header=TRUE,sep="")
  period.name <- ""
  z1 <- c((1-PERIOD.SAMPLE.COUNT):1)
  
  for(i in 1:PERIOD.COUNT) {
    z <- z1+PERIOD.SAMPLE.COUNT*i
    z[1]<-1 #row name
    
    period.name <- paste(state,"_matrix_table_",i,".txt",sep="")
    # the matrix in each state in every period
    write.table(matrix.table[z],file=period.name,
                row.names = FALSE,
                sep="\t")
  }
}

sd.test <- function(file.name,features.sd.threshold=0.001){
  case.period.matrix.table <- read.table(paste("case_",file.name,".txt",sep=""),
                                         header=TRUE,sep="")  
  control.period.matrix.table <- read.table(paste("control_",file.name,".txt",sep=""),
                                            header=TRUE,sep="")  
  z <- c(2:(PERIOD.SAMPLE.COUNT+1))
  
  case.sd <- apply(case.period.matrix.table[,z],1,sd) 
  control.sd <- apply(control.period.matrix.table[,z],1,sd)
  
  no.zero.index <- which((case.sd != 0) & (control.sd != 0))
  
  gene.sd <- case.sd[no.zero.index]/control.sd[no.zero.index]
  gene.sd.log <- log(gene.sd)
  gene.sd.log.p <- unlist(lapply(gene.sd.log,pnorm,mean=mean(gene.sd.log),sd=sd(gene.sd.log)))
  high.sd.index <- which((gene.sd.log.p <= features.sd.threshold) | (gene.sd.log.p >= (1-features.sd.threshold))) 
  source.high.sd.index <- no.zero.index[high.sd.index]
  #li's method
  #   sd.log.threshold <- pnorm(features.sd.threshold/2,mean=mean(gene.sd.log),sd=sd(gene.sd.log))
  #   high.sd.index <- which(abs(gene.sd.log) >= sd.log.threshold)
  
  # the sd of genes 
  write.table(gene.sd,
              paste(file.name,"_sd.txt",sep=""),
              row.names=FALSE,
              sep="\t")
  # the sd of genes which has a big value
  write.table(gene.sd[high.sd.index],
              paste(file.name,"_high_sd.txt",sep=""),
              row.names=FALSE,
              sep="\t")
  # the sd of case data which has a big value
  write.table(case.sd[source.high.sd.index],
              paste("case_",file.name,"_high_sd.txt",sep=""),
              row.names=FALSE,
              sep="\t")
  # the sd of control data which has a big value
  write.table(control.sd[source.high.sd.index],
              paste("control_",file.name,"_high_sd.txt",sep=""),
              row.names=FALSE,
              sep="\t")
  # the case data whose sd has a big value
  write.table(case.period.matrix.table[source.high.sd.index,],
              paste("case_",file.name,"_with_high_sd.txt",sep=""),
              row.names=FALSE,
              sep="\t")
  # the  control data whose sd has a big value
  write.table(control.period.matrix.table[source.high.sd.index,],
              paste("control_",file.name,"_with_high_sd.txt",sep=""),
              row.names=FALSE,
              sep="\t")
}

sd.test.with.one.state <- function(file.name,features.sd.threshold=0.001){
  case.period.matrix.table <- read.table(paste("case_",file.name,".txt",sep=""),
                                         header=TRUE,sep="")  
  z <- c(2:(PERIOD.SAMPLE.COUNT+1))
  
  case.sd <- apply(case.period.matrix.table[,z],1,sd) 
  
  no.zero.index <- which(case.sd != 0)
  gene.sd <- case.sd
  gene.sd.log <- log(gene.sd)
  gene.sd.log.p <- unlist(lapply(gene.sd.log,pnorm,mean=mean(gene.sd.log),sd=sd(gene.sd.log)))
  high.sd.index <- which((gene.sd.log.p <= features.sd.threshold) | (gene.sd.log.p >= (1-features.sd.threshold))) 
  source.high.sd.index <- no.zero.index[high.sd.index]
  #li's method
  #   sd.log.threshold <- pnorm(features.sd.threshold/2,mean=mean(gene.sd.log),sd=sd(gene.sd.log))
  #   high.sd.index <- which(abs(gene.sd.log) >= sd.log.threshold)
  
  # the sd of genes 
  write.table(gene.sd,
              paste(file.name,"_sd.txt",sep=""),
              row.names=FALSE,
              sep="\t")
  # the sd of genes which has a big value
  write.table(gene.sd[high.sd.index],
              paste(file.name,"_high_sd.txt",sep=""),
              row.names=FALSE,
              sep="\t")
  # the sd of case data which has a big value
  write.table(case.sd[source.high.sd.index],
              paste("case_",file.name,"_high_sd.txt",sep=""),
              row.names=FALSE,
              sep="\t")
  # the case data whose sd has a big value
  write.table(case.period.matrix.table[source.high.sd.index,],
              paste("case_",file.name,"_with_high_sd.txt",sep=""),
              row.names=FALSE,
              sep="\t")
}

calc.pcc <- function(state,period){
  filter.table <- read.table(paste(state,"_matrix_table_",period,"_with_high_sd.txt",sep=""),
                             header=TRUE,sep="")
  geneIds <- filter.table[,1] #as the row names and column names of matrix
  filter.table <- filter.table[,c(2:(PERIOD.SAMPLE.COUNT+1))]
  trans.matrix <- t(filter.table) #matrix Transpose
  cor.matrix <- abs(cor(trans.matrix))
  rownames(cor.matrix) <- geneIds
  colnames(cor.matrix) <- geneIds
  cor.matrix
}

#generate DNB 
pcc.test <- function(period){
  #control sample 
  #   control.cor.table <- read.table(paste("control_",period.name,"_cor_matrix.txt",sep=""),
  #                              header=TRUE,sep="")
  control.cor.table <- calc.pcc(STATE[2],period)
  #   names(control.cor.table) <- row.names(control.cor.table)
  genes <- row.names(control.cor.table)
  genes.number <- length(genes)
  genes.index <- 1:genes.number
  #matrix is more lightweight
  #   control.cor.table <- as.matrix(control.cor.table)
  
  #case sample
  #   case.cor.table <- read.table(paste("case_",period.name,"_cor_matrix.txt",sep=""),
  #                              header=TRUE,sep="")
  case.cor.table <- calc.pcc(STATE[1],period)
  #   names(case.cor.table) <- row.names(case.cor.table)
  #   #matrix is more lightweight
  #   case.cor.table <- as.matrix(case.cor.table)
  
  model <- hclust(as.dist(1-case.cor.table))
  cluster <- cutree(model,h = CLUSTER.HCLUST.H)
  
  case.sd <- read.table(paste("case_matrix_table_",period,"_high_sd.txt",sep=""),
                        header=TRUE,
                        sep="")
  control.sd <- read.table(paste("control_matrix_table_",period,"_high_sd.txt",sep=""),
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
    out.index <- ifelse(out.index<nrow(pcc.out),out.index,nrow(pcc.out))
    pcc.out <- pcc.out[1:out.index,]
    pcc.out.mean[cluster.index] <- mean(pcc.out[,2],na.rm=TRUE)/mean(pcc.out[,1],na.rm=TRUE)   
  }
  ci <- pcc.in.mean*(df.aggr.by.cluster$sd)/pcc.out.mean
  
  # the final CI value in the period
  ci.max <- max(ci)
  write.table(ci.max,
              paste("matrix_table_",period,"_max_ci.txt",sep=""),
              row.names=FALSE,
              sep="\t",
              col.names=FALSE)
  
  # this is the gene ids in  'DNB' ,every period have a 'DNB' ,
  # but the real DNB is whose CI value is the maxima
  max.model <<- genes[as.integer(unlist(strsplit(as.character(models[which.max(ci)]),",")))]
  #   print(max.model)
  #write the dnbs in current period
  write.table(max.model,
              paste("matrix_table_",period,"_dnb.txt",sep=""),
              row.names=FALSE,
              sep="\t",
              col.names=FALSE,
              quote=FALSE)
}

#generate DNB  for one state
pcc.test.with.one.state <- function(period){
  case.cor.table <- calc.pcc(STATE[1],period)
  genes <- row.names(case.cor.table)
  genes.number <- length(genes)
  genes.index <- 1:genes.number
  
  model <- hclust(as.dist(1-case.cor.table))
  cluster <- cutree(model,h = CLUSTER.HCLUST.H)
  
  case.sd <- read.table(paste("case_matrix_table_",period,"_high_sd.txt",sep=""),
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
              paste("matrix_table_",period,"_max_ci.txt",sep=""),
              row.names=FALSE,
              sep="\t",
              col.names=FALSE)
  
  # this is the gene ids in  'DNB' ,every period have a 'DNB' ,
  # but the real DNB is whose CI value is the maxima
  max.model <<- genes[as.integer(unlist(strsplit(as.character(models[which.max(ci)]),",")))]
  #   print(max.model)
  #write the dnbs in current period
  write.table(max.model,
              paste("matrix_table_",period,"_dnb.txt",sep=""),
              row.names=FALSE,
              sep="\t",
              col.names=FALSE,
              quote=FALSE)
}

#find the maxima values of an array
findMaxima <- function(array){
  which(diff(c(1,sign(diff(array)),-1)) == -2)
}

plot.ci <- function(){
  
  ci <<- numeric()# this is the final CI result of all periods
  periods <-1:PERIOD.COUNT
  for(i in periods){
    
    period.name <- paste("matrix_table_",i,"_max_ci.txt",sep="")
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
  
  if(is.null(CASE.FILE.NAME)){
    stop("you should set --case.file.name")
  }else{
    if(is.null(CONTROL.FILE.NAME)){
      STATE.COUNT <<- 1 #no control data
    }
  }
  
  divide.files.by.periods(STATE[1],CASE.FILE.NAME)
  
  if(STATE.COUNT == 2){
    divide.files.by.periods(STATE[2],CONTROL.FILE.NAME)
    
    for (period in 1:PERIOD.COUNT)  {
      file.name <- paste("matrix_table_",period,sep="")
      sd.test(file.name=file.name,features.sd.threshold=FEATURES.SD.THRESHOLD)
      pcc.test(period)
    }
  }else{# one state
    for (period in 1:PERIOD.COUNT)  {
      file.name <- paste("matrix_table_",period,sep="")
      sd.test.with.one.state(file.name=file.name,features.sd.threshold=FEATURES.SD.THRESHOLD)
      pcc.test.with.one.state(period)
    }
  }
  plot.ci()
}

main <- function(){
  #   setwd(".")
  args <- commandArgs(TRUE)
  print(args)
  if ((length(args) %% 2 != 0) ){
    print.usage()
  }else {
    if(length(args) != 0){
      init(args)
    }
    
    gdm()
  }
}
# main()
system.time(main())
