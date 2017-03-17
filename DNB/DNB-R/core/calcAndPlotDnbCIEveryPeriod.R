# give a module gene ids ,calc its ci value

# BASE.PATH <- "/host/data/"
BASE.PATH <- "~/gdm/"
FILE.NAME <- "liver_labeled_data.txt"

PERIOD.COUNT <- 5 #we have 5 periods:4wk,8wk,12wk,16wk,20wk
PERIOD.SAMPLE.SEP <- 10 #each period has 10 samples
PERIOD.SAMPLE.COUNT <- 5 # divide into GK and WKY, each have 5 samples 
STATE <- c("gk","wt") #gk is case,wt is control

calc.pcc <- function(state,period){
  whole.table <- read.table(paste(BASE.PATH,state,"_matrix_table_",period*4,"wk.txt",sep=""),
                            header=TRUE,sep="")
  #   geneIds <- whole.table[,1] #as the row names and column names of matrix
  whole.table <- whole.table[,c(2:(PERIOD.SAMPLE.COUNT+1))]
  trans.matrix <- t(whole.table) #matrix Transpose
  cor.matrix <- abs(cor(trans.matrix))
  #   rownames(cor.matrix) <- geneIds
  #   colnames(cor.matrix) <- geneIds
  #   cor.matrix
}

calc.ci.spec.period.dnb.and.spec.period <- function(dnb.index,dnb.period,period){
  gk.data <- read.table(paste(BASE.PATH,"gk_matrix_table_",period*4,"wk.txt",sep=""),
                        header=TRUE,sep="")
  wt.data <- read.table(paste(BASE.PATH,"wt_matrix_table_",period*4,"wk.txt",sep=""),
                        header=TRUE,sep="")
  gk.data.dnb <- gk.data[dnb.index,-1]
  wt.data.dnb <- wt.data[dnb.index,-1]
  
  gk.sd <- apply(gk.data.dnb,1,sd)
  wt.sd <- apply(wt.data.dnb,1,sd)
  sd.mean <- mean(gk.sd,na.rm=TRUE) / mean(wt.sd,na.rm=TRUE)
  
  #control sample 
  wt.cor.table <- calc.pcc("wt",period)
  wt.cor.table <- as.matrix(wt.cor.table)
  #case sample
  gk.cor.table <- calc.pcc("gk",period)
  gk.cor.table <- as.matrix(gk.cor.table)
  
  model.size <- length(dnb.index)
  wt.pcc.in <- as.vector(wt.cor.table[dnb.index,dnb.index])
  gk.pcc.in <- as.vector(gk.cor.table[dnb.index,dnb.index])
  
  wt.pcc.out <- as.vector(wt.cor.table[-dnb.index,dnb.index])
  gk.pcc.out <- as.vector(gk.cor.table[-dnb.index,dnb.index])
  
  pcc.in.mean <- (sum(gk.pcc.in,na.rm=TRUE)-model.size)/(sum(wt.pcc.in,na.rm=TRUE)-model.size)
  
  pcc.out <- cbind(wt.pcc.out,gk.pcc.out)
  pcc.out <- pcc.out[order(-pcc.out[,1]),]
  pcc.out <- pcc.out[1:(PCC.OUT.AMOUNT*model.size),]
  pcc.out.mean <- mean(pcc.out[,2],na.rm=TRUE)/mean(pcc.out[,1],na.rm=TRUE)   
  
  ci.max <- pcc.in.mean*sd.mean/pcc.out.mean
  write.table(ci.max,
              paste(BASE.PATH,author,"_",dnb.period*4,"wk_max_ci_",period,".txt",sep=""),
              row.names=FALSE,
              sep="\t",
              col.names=FALSE)
}

calc.ci <- function (author,period,module.file.name) {
  module.gene.ids <- read.table(paste(BASE.PATH,module.file.name,".txt",sep=""),
                                sep="")[,1]
  module.gene.ids <- as.character(module.gene.ids)
  
  gk.data <- read.table(paste(BASE.PATH,"gk_matrix_table_",period*4,"wk.txt",sep=""),
                        header=TRUE,sep="")
  #   wt.data <- read.table(paste(BASE.PATH,"wt_matrix_table_",period*4,"wk.txt",sep=""),
  #                         header=TRUE,sep="")
  dnb.index <- which(as.character(gk.data[,1]) %in% module.gene.ids)
  
  for(p in 1:PERIOD.COUNT){
    calc.ci.spec.period.dnb.and.spec.period(dnb.index,period,p)
  }
  
}



plot.ci <- function(author,period){
  ci <<- numeric()
  periods <-1:PERIOD.COUNT
  for(i in periods){
    #4wk,8wk,12wk,16wk,20wk
    period.name <- paste("qiu_",i*4,"wk_max_ci_",period,".txt",sep="")
    ci[i] <<- read.table(paste(BASE.PATH,period.name,sep=""))
  }
  names(ci) <<- c("4wk","8wk","12wk","16wk","20wk")
  print("ci table:")
  print(as.table(unlist(ci)))
  write.table(ci,
              paste(BASE.PATH,author,"_all_ci_",period,".txt",sep=""),
              row.names=FALSE,
              sep="\t",
              col.names=FALSE)
  setwd(BASE.PATH)
  png(paste(author,"_ci_",period,".png",sep=""))
  plot(periods,unlist(ci),
       xlab="period (*4 wk)",
       ylab="ci",
       main="ci growth",
       type="b")
  dev.off()
}

# period <- 1
# author <- "qiu"

#calc Doc li's ci
# foreach (period = c(1,4)) %dopar% {
for (period in c(1,4)){
  calc.ci("li",period,paste("liver_DNB_t",period,sep=""))
  plot.ci("li",period)
}

#calc my ci
# foreach (period = 1:PERIOD.COUNT) %dopar%{
# for (period in 1:PERIOD.COUNT) {
#   calc.ci("qiu",period,paste("matrix_table_",period*4,"wk_dnb",sep=""))
#   plot.ci("qiu",period)
# }

