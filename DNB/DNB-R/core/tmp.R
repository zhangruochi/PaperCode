#! /usr/bin/Rscript --no-save
#
#' @author : star qiu
#' @date 2014.8.1
#' 
#' 
library(plyr)
# BASE.PATH <- "/host/data/"
BASE.PATH <- "~/gdm/"
FILE.NAME <- "liver_labeled_data.txt"

# print(BASE.PATH )
# 
# x <- c(1,5,3,1,2,5,3,1)
# 
# hist(x)
# 
# hist(x,breaks=c(0,1,3,5),freq=TRUE)
curFileDir <- dirname(sys.frame(1)$ofile) #get current file directory
# setwd(curFileDir)
# source(file.path(curFileDir,"statPcc.R"))
# 
# result = tryCatch(eval(parse(text="helloKitty('hagls')")),
#                   error = function(e) {print(paste0("12",e));stop(e);},
#                   warning = function(w) print(paste0("23",w)))
data(iris); attach(iris)
iris.km<- kmeans( dist(iris[,1:4]) ,30)
# plot( iris.hc)

h.my <-0.75
# iris.id <- cutree(iris.hc, h = h.my)
# cluster.without.dup <- iris.id[!duplicated(iris.id)]
# cluster.without.dup
necessary <- c('plyr','FisherEM','car')
loadLib <- paste0('library(',necessary,')')
for (lib in loadLib){
  eval(parse(lib))
}

plotcluster(dist(iris[,1:4]) , iris.km$cluster) # 生成聚类图
