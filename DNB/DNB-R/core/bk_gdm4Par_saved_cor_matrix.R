library(plyr)
library(foreach)
library(doParallel)

# BASE.PATH <- "/host/data/"
BASE.PATH <- "~/gdm/"
FILE.NAME <- "liver_labeled_data.txt"

PERIOD.COUNT <- 5 #we have 5 periods:4wk,8wk,12wk,16wk,20wk
PERIOD.SAMPLE.SEP <- 10 #each period has 10 samples
PERIOD.SAMPLE.COUNT <- 5 # divide into GK and WKY, each have 5 samples 
STATE <- c("gk","wt") #gk is case,wt is control
FEATURES.SD.THRESHOLD <- 100
CLUSTER.HCLUST.H <- 0.75
PCC.OUT.AMOUNT <- 50
CORES <- 6

BASE.PATH <- "~/gdm/"
FILE.NAME <- "liver_labeled_data.txt"

PERIOD.COUNT <- 5 #we have 5 periods:4wk,8wk,12wk,16wk,20wk
PERIOD.SAMPLE.SEP <- 10 #each period has 10 samples
PERIOD.SAMPLE.COUNT <- 5 # divide into GK and WKY, each have 5 samples 
STATE <- c("gk","wt") #gk is case,wt is control
FEATURES.SD.THRESHOLD <- 100
CLUSTER.HCLUST.H <- 0.75
PCC.OUT.AMOUNT <- 50
CORES <- 6

registerDoParallel(cores=CORES)

#GK , WT
divide.files.by.state <- function(file.name){
  matrix.table <- read.table(paste(BASE.PATH,file.name,sep=""),
                             header=TRUE,sep="")
  gk.index <- c(1,2:6,12:16,22:26,32:36,42:46)
  wt.index <- c(1,7:11,17:21,27:31,37:41,47:51)
  write.table(matrix.table[gk.index],file=paste(BASE.PATH,"gk_data.txt",sep=""),
              row.names = FALSE,
              sep="\t")
  write.table(matrix.table[wt.index],file=paste(BASE.PATH,"wt_data.txt",sep=""),
              row.names = FALSE,
              sep="\t")
}

#4wk,8wk,12wk,16wk,20wk
divide.files.by.periods <- function(state,file.name){
  matrix.table <- read.table(paste(BASE.PATH,state,file.name,sep=""),
                             header=TRUE,sep="")
  period.name <- ""
  z <- c((1-PERIOD.SAMPLE.COUNT):1)  
  
  foreach(i = 1:PERIOD.COUNT) %dopar% {
    z <- z+PERIOD.SAMPLE.COUNT*i
    z[1]<-1
    
    #4wk,8wk,12wk,16wk,20wk
    period.name <- paste(state,"_matrix_table_",i*4,"wk.txt",sep="")
    write.table(matrix.table[z],file=paste(BASE.PATH,period.name,sep=""),
                row.names = FALSE,
                sep="\t")
  }
}

z.test<-function(x,n,sigma,alpha){
  mean<-mean(x)
  ans<-c(
    mean-sigma*qnorm(1-alpha/2,mean=0,sd=1,lower.tail=TRUE)/sqrt(n),
    mean+sigma*qnorm(1-alpha/2,mean=0,sd=1,lower.tail=TRUE)/sqrt(n))
  ans
}

sd.test <- function(file.name,features.sd.threshold=0.05){
  gk.period.matrix.table <- read.table(paste(BASE.PATH,"gk_",file.name,".txt",sep=""),
                                       header=TRUE,sep="")  
  wt.period.matrix.table <- read.table(paste(BASE.PATH,"wt_",file.name,".txt",sep=""),
                                       header=TRUE,sep="")  
  z <- c(2:(PERIOD.SAMPLE.COUNT+1))
  
  gk.sd <- apply(gk.period.matrix.table[z],1,sd) 
  wt.sd <- apply(wt.period.matrix.table[z],1,sd)
  
  gene.sd <- gk.sd/wt.sd
  gene.sd.log <- log(gene.sd)
  gene.sd.log.p <- unlist(lapply(gene.sd.log,pnorm,mean=mean(gene.sd.log),sd=sd(gene.sd.log)))
  high.sd.index <- which((gene.sd.log.p <= features.sd.threshold) | (gene.sd.log.p >= (1-features.sd.threshold)))
  #   gene.length <- length(gene.sd)
  #   gene.selet.sep <- gene.length * features.sd.threshold
  #   
  #   #   high.sd.index <- 1:gene.length 
  #   high.sd.index <- order(gene.sd)
  #   high.sd.index <- high.sd.index[c(1:gene.selet.sep,(gene.length-gene.selet.sep+1):gene.length)]
  #   high.sd.index <- which(gene.sd >= FEATURES.SD.THRESHOLD)
  
  write.table(gene.sd,
              paste(BASE.PATH,file.name,"_sd.txt",sep=""),
              row.names=FALSE,
              sep="\t")
  write.table(gene.sd[high.sd.index],
              paste(BASE.PATH,file.name,"_high_sd.txt",sep=""),
              row.names=FALSE,
              sep="\t")
  
  write.table(gk.sd[high.sd.index],
              paste(BASE.PATH,"gk_",file.name,"_high_sd.txt",sep=""),
              row.names=FALSE,
              sep="\t")
  write.table(wt.sd[high.sd.index],
              paste(BASE.PATH,"wt_",file.name,"_high_sd.txt",sep=""),
              row.names=FALSE,
              sep="\t")
  
  write.table(gk.period.matrix.table[high.sd.index,],
              paste(BASE.PATH,"gk_",file.name,"_with_high_sd.txt",sep=""),
              row.names=FALSE,
              sep="\t")
  write.table(wt.period.matrix.table[high.sd.index,],
              paste(BASE.PATH,"wt_",file.name,"_with_high_sd.txt",sep=""),
              row.names=FALSE,
              sep="\t")
}

calc.pcc <- function(state,file.name){
  filtered.table <- read.table(paste(BASE.PATH,state,"_",file.name,"_with_high_sd.txt",sep=""),
                               header=TRUE,sep="")
  geneIds <- filtered.table[,1] #as the row names and column names of matrix
  filtered.table <- filtered.table[,c(2:(PERIOD.SAMPLE.COUNT+1))]
  trans.matrix <- t(filtered.table) #matrix Transpose
  cor.matrix <- abs(cor(trans.matrix))
  rownames(cor.matrix) <- geneIds
  colnames(cor.matrix) <- geneIds
  write.table(cor.matrix,
              paste(BASE.PATH,state,"_",file.name,"_cor_matrix.txt",sep=""),
              row.names=TRUE,
              sep="\t")
}

pcc.test <- function(period.name){
  #control sample 
  wt.cor.table <- read.table(paste(BASE.PATH,"wt_",period.name,"_cor_matrix.txt",sep=""),
                             header=TRUE,sep="")
  names(wt.cor.table) <- row.names(wt.cor.table)
  genes <- row.names(wt.cor.table)
  genes.number <- length(genes)
  genes.index <- 1:genes.number
  #matrix is more lightweight
  wt.cor.table <- as.matrix(wt.cor.table)
  
  #case sample
  gk.cor.table <- read.table(paste(BASE.PATH,"gk_",period.name,"_cor_matrix.txt",sep=""),
                             header=TRUE,sep="")
  names(gk.cor.table) <- row.names(gk.cor.table)
  #matrix is more lightweight
  gk.cor.table <- as.matrix(gk.cor.table)
  
  model <- hclust(as.dist(1-gk.cor.table))
  cluster <- cutree(model,h = CLUSTER.HCLUST.H)
  
  gk.sd <- read.table(paste(BASE.PATH,"gk_",period.name,"_high_sd.txt",sep=""),
                      header=TRUE,
                      sep="")
  wt.sd <- read.table(paste(BASE.PATH,"wt_",period.name,"_high_sd.txt",sep=""),
                      header=TRUE,
                      sep="")
  
  df.with.cluster.genes.sds <- cbind(cluster,genes.index,gk.sd,wt.sd)
  colnames(df.with.cluster.genes.sds) <-c("cluster","genes.index","gk.sd","wt.sd")
  df.aggr.by.cluster <- ddply(df.with.cluster.genes.sds,.(cluster),summarize,
                              models = paste(genes.index,collapse=","),
                              sd = mean(gk.sd)/mean(wt.sd))
  colnames(df.aggr.by.cluster) <-c("cluster","models","sd")
  
  cluster.aggr <- df.aggr.by.cluster$cluster
  models <- df.aggr.by.cluster$models
  cluster.number <- length(cluster.aggr)
  
  
  #make sure wt.cor.table is upper.tri
  diag(wt.cor.table) <- NA
  diag(gk.cor.table) <- NA
  
  pcc.in.mean <- numeric()
  pcc.out.mean <- numeric()
  
  for(cluster.index in 1:cluster.number){
    cur.model <- as.integer(unlist(strsplit(as.character(models[cluster.index]),",")))
    model.size <- length(cur.model)
    wt.pcc.in <- as.vector(wt.cor.table[cur.model,cur.model])
    gk.pcc.in <- as.vector(gk.cor.table[cur.model,cur.model])
    
    wt.pcc.out <- as.vector(wt.cor.table[-cur.model,cur.model])
    gk.pcc.out <- as.vector(gk.cor.table[-cur.model,cur.model])
    
    pcc.in.mean[cluster.index] <- (sum(gk.pcc.in,na.rm=TRUE)-model.size)/(sum(wt.pcc.in,na.rm=TRUE)-model.size)
    
    pcc.out <- cbind(wt.pcc.out,gk.pcc.out)
    pcc.out <- pcc.out[order(-pcc.out[,1]),]
    pcc.out <- pcc.out[1:(PCC.OUT.AMOUNT*model.size),]
    pcc.out.mean[cluster.index] <- mean(pcc.out[,2],na.rm=TRUE)/mean(pcc.out[,1],na.rm=TRUE)   
  }
  ci <- pcc.in.mean*(df.aggr.by.cluster$sd)/pcc.out.mean
  
  ci.max <- max(ci)
  write.table(ci.max,
              paste(BASE.PATH,period.name,"_max_ci.txt",sep=""),
              row.names=FALSE,
              sep="\t",
              col.names=FALSE)
  
  max.model <- genes[as.integer(unlist(strsplit(as.character(models[which.max(ci)]),",")))]
  write.table(max.model,
              paste(BASE.PATH,period.name,"_dnb.txt",sep=""),
              row.names=FALSE,
              sep="\t",
              col.names=FALSE)
  
}

plot.ci <- function(){
  ci <- numeric()
  periods <-1:PERIOD.COUNT
  for(i in periods){
    #4wk,8wk,12wk,16wk,20wk
    period.name <- paste("matrix_table_",i*4,"wk_max_ci.txt",sep="")
    ci[i] <- read.table(paste(BASE.PATH,period.name,sep=""))
  }
  print("ci=")
  print(ci)
  setwd(BASE.PATH)
  png("ci.png")
  plot(periods,unlist(ci),
       xlab="period (*4 wk)",
       ylab="ci",
       main="ci growth",
       type="b")
  dev.off()
}

compare.to.example <- function(){
  example.dnb.t1 <-read.table(paste(BASE.PATH,"liver_DNB_t1.txt",sep=""))[,1]
  example.dnb.t4 <-read.table(paste(BASE.PATH,"liver_DNB_t4.txt",sep=""))[,1]
  dnb.4wk <-read.table(paste(BASE.PATH,"matrix_table_4wk_dnb.txt",sep=""))[,1]
  dnb.16wk <-read.table(paste(BASE.PATH,"matrix_table_16wk_dnb.txt",sep=""))[,1]
  
  #find common features
  common.features.t1 <- intersect(example.dnb.t1,dnb.4wk)
  write.table(common.features.t1,paste(BASE.PATH,"common_4wk_dnb.txt",sep=""),sep="\n",
              col.names=FALSE,row.names=FALSE)
  common.features.t4 <- intersect(example.dnb.t4,dnb.16wk)
  write.table(common.features.t4,paste(BASE.PATH,"common_16wk_dnb.txt",sep=""),sep="\n",
              col.names=FALSE,row.names=FALSE)
}

main <- function(){
  
  divide.files.by.state(FILE.NAME)
  foreach(state = STATE) %dopar% {
    divide.files.by.periods(state,"_data.txt")
  }
  
  for(i in 1:PERIOD.COUNT)  {   
    #4wk,8wk,12wk,16wk,20wk
    file.name <- paste("matrix_table_",i*4,"wk",sep="")
    sd.test(file.name=file.name,features.sd.threshold=FEATURES.SD.THRESHOLD)
    foreach(state = STATE) %dopar% {
      calc.pcc(state,file.name)
    }
    pcc.test(file.name)
  }
}
# divide.files.by.state(FILE.NAME)
# foreach(state = STATE) %dopar% {
#   divide.files.by.periods(state,"_data.txt")
# }

foreach (period = 1:PERIOD.COUNT) %dopar% {
# for(i in 1:PERIOD.COUNT)  {   
  #4wk,8wk,12wk,16wk,20wk
  file.name <- paste("matrix_table_",period*4,"wk",sep="")
  sd.test(file.name=file.name,features.sd.threshold=FEATURES.SD.THRESHOLD)
  foreach(state = STATE) %dopar% {
    calc.pcc(state,file.name)
  }
  #   pcc.test(file.name)
}
# plot.ci()
# compare.to.example()
# system.time(main())