getCluster <- function(data,cluster.number=30){
  model <- kmeans(data,cluster.number)
  cluster <- model$cluster
}