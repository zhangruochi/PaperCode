
index <- c(1,
           14,20,26,2,6,10, #0 d
           18,24,30,4,8,12, #4 d
           19,25,31,5,9,13, #7 d
           16,22,28,3,7,11 #28 d
           )

sourceMatrix <- read.table(file.path("sourceData","GSE64538_gene_count_matrix.txt"),
                           sep="\t",header=TRUE) 
destinationMatrix <- sourceMatrix[,index]

write.table(destinationMatrix,file.path("sourceData","GSE64538_labeled.txt"),
            row.names=FALSE,sep="\t",quote=FALSE)