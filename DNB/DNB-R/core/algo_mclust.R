getCluster <- function(data,cluster.number=30){
  emobj <- simple.init(data, nclass = cluster.number)
  emobj <- shortemcluster(data, emobj)
  summary(emobj)
  ret <- emcluster(data, emobj, assign.class = TRUE)
#   cluster <- model$label
#   print(cluster)
}