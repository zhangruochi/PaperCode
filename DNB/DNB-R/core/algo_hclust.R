getCluster <- function(data,cluster.number=30){
  # print("using hclust to cluster")
  dist.data <- calc.pcc.with.filter.table(data) #calc.pcc.with.trans.matrix is in gdm4Par.R
  model <- hclust(as.dist(1-dist.data))
  cluster <- cutree(model,k = cluster.number)
}