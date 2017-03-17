# DIR <- "D:\\x\\"
DIR <- "~/x/"

setwd(DIR)

gdmCsv <- read.table("gdm_1.csv",sep=",",header=TRUE)
pccValues <- as.integer(as.double(gdmCsv[,4])*10)

pccValues <- pccValues[pccValues >= 10]

h1 <-hist(pccValues)

h2 <- hist(pccValues,breaks=c(0,10, 11, 12, 13, 14, 15, 16, 18, 20, 23, 28, 36, 49, 78, 167, 41480),freq=TRUE)

sortedPccValues <- sort(pccValues,decreasing = TRUE)
sortedPccValues[1:20]

sd(sortedPccValues)