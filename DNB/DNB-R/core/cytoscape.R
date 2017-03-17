#! /usr/bin/Rscript --no-save
#
#' @author : star qiu
#' @date 2014.8.1
#' 
#' 	

# library(foreach)
# library(doParallel)

BASE.PATH <- "/host/data/"
# BASE.PATH <- "~/prog/apache-tomcat-8.0.17/webapps/DNBGen/WEB-INF/classes/"
PERIOD.COUNT <- 5 
PERIOD.SAMPLE.COUNT <- 5 
# PERIOD.COUNT <- 4 
# PERIOD.SAMPLE.COUNT <- 3 
STATE <- c("case","control") #case is abnormal,control is normal
STATE.COUNT <- 2 #
CORES <- 6

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
         "--cores" = CORES <<- as.integer(value)
  )
}

print.usage <- function(){
  cat("Usage: gdm4Par.R [-h/--help |-p/--base.path directory] \n
      [--period.count number] [--period.sample.count number]  \n
      [cores number]\n")
  cat("Details:\n")
  cat("\t -h/--help   show the usage of gdm4Par.R \n")
  cat("\t -p/--base.path   set the path of gdm4Par.R . the default value is ./ \n")
  cat("\t --period.count   set the number of periods  .
      the default is 5  \n")
  cat("\t --period.sample.count   set the number of samples in every period . 
      the default is 5 \n")
  cat("\t --cores  set the number of cores we use for parallel program 
      the default is 6 \n")
  cat("Description:\n")
  cat("\t  if -h/--help is appeared,the other parameters is ignored. 
      \t  if you want have more cores ,you can set it larger value ,
      the program may run faster.
      \t  change features.sd.threshold may have suprise. it's good encough
      to the data of rat's liver.
      \n")
}

calc.pcc <- function(state,period){
  filter.table <- read.table(paste(BASE.PATH,state,"_matrix_table_",period,"_with_high_sd.txt",sep=""),
                             header=TRUE,sep="")
  geneIds <- filter.table[,1] #as the row names and column names of matrix
  filter.table <- filter.table[,c(2:(PERIOD.SAMPLE.COUNT+1))]
  trans.matrix <- t(filter.table) #matrix Transpose
  cor.matrix <- abs(cor(trans.matrix))
  rownames(cor.matrix) <- geneIds
  colnames(cor.matrix) <- geneIds
  cor.matrix
}

cor.matrix.profile <- function(period){
  case.cor.matrix <- calc.pcc("case",period)
  control.cor.matrix <- calc.pcc("control",period)
  cor.matrix <- case.cor.matrix/control.cor.matrix
  rm(case.cor.matrix)
  rm(control.cor.matrix)
  cor.vector.log <- log(as.vector(cor.matrix[lower.tri(cor.matrix)]))
  rm(cor.matrix)
  hist(cor.vector.log)
}

gen.gdm.csv.bk <- function(period){
  case.cor.matrix <- calc.pcc("case",period)
  control.cor.matrix <- calc.pcc("control",period)
  cor.matrix <- case.cor.matrix/control.cor.matrix
  rm(case.cor.matrix)
  rm(control.cor.matrix)
  
  genes <- rownames(cor.matrix)
  
  # sum(cor.matrix>1)-10729
  # hist(as.vector(cor.matrix))
  total.row <- nrow(cor.matrix)
  title <- c("source","target","symbol","value")
  
  save.file.name <- paste(BASE.PATH,"gdm_",period,".csv",sep="")
  if (file.exists(save.file.name)){
    file.remove(save.file.name)
  }
  write.table(t(title),save.file.name,
              append=TRUE,quote=FALSE,sep=",",
              row.names =FALSE,col.names=FALSE)
  
  for( i in 1:(total.row-1)){
    
    element.index <- (i+1):total.row
    element.num <- total.row - i
    
    mysource <- genes[i]
    mytarget <- genes[element.index]
    value <- cor.matrix[i,element.index]
    symbol <- paste("abcd",i,element.index,sep="")
    
    cyto.csv <- cbind(mysource,mytarget,symbol,value)
    
    write.table(cyto.csv,save.file.name,
                append=TRUE,quote=FALSE,sep=",",
                row.names =FALSE,col.names=FALSE)
  }
}

generate.high.sd.genes <- function (period,genes) {
  all.genes <- read.table(paste("matrix_table_",period,"_genes.txt",sep="")
                          ,header= TRUE)[,1]
  all.sds <- read.table(paste("matrix_table_",period,"_sd.txt",sep="")
                        ,header= TRUE)[,1]
  # avoid regarding as factor
  all.genes <- as.character(all.genes)
  
  high.sd.genes.len <- length(genes)
  high.sd.genes.index <- numeric(length=high.sd.genes.len)
  for(i in 1:high.sd.genes.len){
    high.sd.genes.index[i] <- which(genes[i] == all.genes)
  }

  high.sd.genes.and.sd <- cbind(all.genes[high.sd.genes.index]
                                ,all.sds[high.sd.genes.index])
  write.table(high.sd.genes.and.sd,
              paste("matrix_table_",period,"_high_sd_genes.txt",sep=""),
              quote=FALSE,sep=",",
              row.names =FALSE,col.names=FALSE)
}

gen.gdm.csv <- function(period){
  case.cor.matrix <- calc.pcc(STATE[1],period)
  control.cor.matrix <- calc.pcc(STATE[2],period)
  cor.matrix <- case.cor.matrix/control.cor.matrix
  rm(case.cor.matrix)
  rm(control.cor.matrix)
  genes <- rownames(cor.matrix)
  
  generate.high.sd.genes(period,genes)
  
  # sum(cor.matrix>1)-10729
  # hist(as.vector(cor.matrix))

  title <- c("source","target","symbol","value")
  
  save.file.name <- paste(BASE.PATH,"gdm_",period,".csv",sep="")
  if (file.exists(save.file.name)){
    file.remove(save.file.name)
  }
  write.table(t(title),save.file.name,
              append=TRUE,quote=FALSE,sep=",",
              row.names =FALSE,col.names=FALSE)
  
  
#   high.sd.genes <- read.table(paste("matrix_table_",period,"_genes.txt",sep="")
#                               ,header= TRUE)[,1]
#   high.sd.genes.index <- which(genes %in% high.sd.genes)
#   genes <- genes[high.sd.genes.index]
#   cor.matrix <- cor.matrix[high.sd.genes.index,high.sd.genes.index]
  total.row <- nrow(cor.matrix)  
  
  dnb <-read.table(paste("matrix_table_",period,"_dnb.txt",sep=""))[,1]

  for( i in 1:(total.row-1)){
    
    element.index <- (i+1):total.row
    #     element.index <- which(log(cor.matrix[i,])>5)
    #     element.index <- element.index[element.index>i]
    value <- cor.matrix[i,element.index]
    #value should not be Inf ,-Inf,0
    element.index <- element.index[which(is.finite(value) & (0 != value))]
    
    mysource <- genes[i]
    mytarget <- genes[element.index]
    
    #ignore the edges of whose souce and target are both not in dnb
#     if(!(mysource %in% dnb)){
#       element.index <- element.index[which(mytarget %in% dnb)]
#       mytarget <- genes[element.index]
#     }
    value <- cor.matrix[i,element.index]
    
    element.num <- length(mytarget)
    
    if (element.num > 0){
        
        symbol <- paste("abcd",i,element.index,sep="")
        
        cyto.csv <- cbind(mysource,mytarget,symbol,value)
        
        write.table(cyto.csv,save.file.name,
                    append=TRUE,quote=FALSE,sep=",",
                    row.names =FALSE,col.names=FALSE)
    }
  }
}

main <- function(){
#   registerDoParallel(cores=CORES) 
  args <- commandArgs(TRUE)
  print(args)
  if ((length(args) %% 2 != 0) ){
    print.usage()
  }else {
    if(length(args) != 0){
      init(args)
    }
    
    setwd(BASE.PATH)
    print(paste("working directory : " , BASE.PATH))
        for (i in 1:PERIOD.COUNT)  {
          gen.gdm.csv(i)
        }
#     foreach (i = 1:PERIOD.COUNT) %dopar% {
#       gen.gdm.csv(i)
#     }
  }
}
# main()
system.time(main())
