FILE.NAME <- "liver_labeled_data.txt"
PERIOD.COUNT <- 5 # the number of periods
PERIOD.SAMPLE.COUNT <- 5 # the number of samples in every period
# FILE.NAME <- "GSE64538_labeled.txt"
# PERIOD.COUNT <- 4 # the number of periods
# PERIOD.SAMPLE.COUNT <- 3 # the number of samples in every period
STATE <- c("case","control") #case is abnormal,control is normal
STATE.COUNT <- 2 #

#case , control
divide.files.by.state <- function(file.name){
  matrix.table <- read.table(file.path("sourceData",file.name),
                             header=TRUE,sep="")
  #   case.index <- c(1,2:6,12:16,22:26,32:36,42:46)
  #   control.index <- c(1,7:11,17:21,27:31,37:41,47:51)
  
  case.index <- c(1)
  control.index <- c(1)
  case.start <- 2:(PERIOD.SAMPLE.COUNT+1)
  control.start <- (2+PERIOD.SAMPLE.COUNT):(STATE.COUNT*PERIOD.SAMPLE.COUNT+1)
  
  for (i in 1:PERIOD.COUNT){
    offset <- (i-1)*PERIOD.SAMPLE.COUNT*STATE.COUNT
    case.index <- c(case.index,case.start + offset)
    control.index <- c(control.index,control.start + offset)
  }
  # all case data matrix
  write.table(matrix.table[case.index],
              file=file.path("sourceData","case_data.txt"),
              row.names = FALSE,
              sep="\t")
  # all control data matrix
  write.table(matrix.table[control.index],
              file=file.path("sourceData","control_data.txt"),
              row.names = FALSE,
              sep="\t")
}

divide.files.by.state(FILE.NAME)
