# DIR <- "D:\\x\\"
DIR <- "~/x/"

setwd(DIR)

gdmCsv <- read.table("gdm_1.csv",sep=",",header=TRUE)
pccValues <- as.integer(gdmCsv[,4])

pccValues <- pccValues[pccValues != 0]

h1 <-hist(pccValues)

h2 <- hist(pccValues,breaks=c(0,1,16, 41480),freq=TRUE)

sortedPccValues <- sort(pccValues,decreasing = TRUE)
sortedPccValues[1:20]

sd(sortedPccValues)
