# Working
library(MASS)
library(glmnet);#lasso
library(kernlab);#svm
library(rpart);#dtree
library(e1071);#bayes
library(pamr);#pam
library(class); ##K-NN
library(minerva);#mine
library(FSelector);#best.first
library(RRF);
library(genefilter);
library(caret); # createFolds()

### Definitions of all the functions
#! k-Fold Cross Validation
efKFCV <- function(xx,yy,nfold,method)
{
  num_tp=num_fp=num_fn=num_tn=0
  index=NULL
  predy=NULL
  id=createFolds(yy, k = nfold, list = TRUE, returnTrain = T)
  rawdata=cbind(xx,yy)
  n=nrow(rawdata)
  p=ncol(rawdata)
  
  tPrediction <- rep(-1, nrow(rawdata));
  
  for (i in 1:nfold){
    # print(paste("Fold",i,sep=' '))
    index=id[[i]]
    y_train=rawdata[index,p]
    y_test=rawdata[-index,p]
    x_train=matrix(rawdata[index,-p],nrow=length(index))
    x_test=matrix(rawdata[-index,-p],nrow=(n-length(index)))
    
    predy <- efClassifier(x_train,y_train,x_test,method)
    
    num_tp[i]=sum(y_test==1 & predy==1)
    num_fn[i]=sum(y_test==1 & predy==0)
    num_fp[i]=sum(y_test==0 & predy==1)
    num_tn[i]=sum(y_test==0 & predy==0)
    
    tPrediction[-index] <- predy;
  }
  se=sum(num_tp)/sum(yy==1)
  sp=sum(num_tn)/sum(yy==0)
  acc=sum(num_tp+num_tn)/length(yy)
  avc=(se+sp)/2
  mcc=(sum(num_tp)*sum(num_tn)-sum(num_fp)* sum(num_fn))/
    (sqrt((sum(num_tp)+sum(num_fp))*(sum(num_tp)+sum(num_fn))*(sum(num_tn)+sum(num_fp))*(sum(num_tn)+sum(num_fn))))
  out=round(cbind(se,sp,acc,avc,mcc),3)
  return(list(out=out, prediction=tPrediction))
}
#! Standard IO of all the investigated classifiers
efClassifier <- function(x_train,y_train,x_test,method)
{
  if (method=="SVM"){
    fit=ksvm(x_train,y_train,type="C-svc",kernel="rbfdot")
    predy=predict(fit,x_test)
  } else { 
    if (method=="NBayes"){
      colnames(x_train)=NULL
      colnames(x_test)=NULL
      data_train=data.frame(ex=x_train,ey=as.factor(y_train))
      data_test=with(data_train,data.frame(ex=x_test))
      fit <- naiveBayes(ey~.,data=data_train)
      predy=predict(fit, data_test, type="class")
    } else {
      if (method=="DTree"){
        colnames(x_train)=NULL
        colnames(x_test)=NULL
        data_train=data.frame(ex=x_train,ey=as.factor(y_train))
        data_test=with(data_train,data.frame(ex=x_test))
        fit <- rpart(ey~.,data=data_train)
        predy=predict(fit, data_test, type="class")
      }# else {
      #if (method=="Lasso"){
      # cv.fit <- cv.glmnet(x_train, y_train, family = "binomial")
      # fit <- glmnet(x_train, y_train, family = "binomial")
      #pfit = predict(fit,x_test,s = cv.fit$lambda.min,type="response")
      #predy<-ifelse(pfit>0.5,1,0)
      #} 
      else { 
        if (method=="KNN"){
          predy<-knn1(x_train,x_test,y_train)
        }
      }    
      #}
    }
  }
  return (predy)
}

efBinaryPerformance <- function(tClass, tPrediction)
{
  tTP <- sum(tClass==1 & tPrediction==1 );
  tFN <- sum(tClass==1 & tPrediction==0 );
  tFP <- sum(tClass==0 & tPrediction==1 );
  tTN <- sum(tClass==0 & tPrediction==0 );
  tSn <- tTP/(tTP+tFN);
  tSp <- tTN/(tTN+tFP);
  tAcc <- (tTP+tTN)/(tTP+tFN+tTN+tFP);
  tAvc <- (tSn+tSp)/2;
  tMCC <- (tTP*tTN-tFP*tFN)/sqrt((tTP+tFP)*(tTP+tFN)*(tTN+tFP)*(tTN+tFN));
  return(round(cbind(tSn, tSp, tAcc, tAvc, tMCC), 3));
}

efPerformanceMatrix <- function( kMatrix )
{
  tresultMatrix <- matrix(nrow=0,ncol=5);
  tdataRowNames <- c();
  tdataColNames <- c("Sn", "Sp", "Acc", "Avc", "MCC");
  
  # SVM
  egResult <- efKFCV(t(kMatrix), egClassLabel, 3, "SVM");
  etMeasurements <- egResult$out;
  tresultMatrix <- rbind(tresultMatrix, etMeasurements[1,]);
  tdataRowNames <- c(tdataRowNames, "SVM");
  
  # NBayes
  egResult <- efKFCV(t(kMatrix), egClassLabel, 3, "NBayes");
  etMeasurements <- egResult$out;
  tresultMatrix <- rbind(tresultMatrix, etMeasurements[1,]);
  tdataRowNames <- c(tdataRowNames, "NBayes");
  
  # DTree
  egResult <- efKFCV(t(kMatrix), egClassLabel, 3, "DTree");
  etMeasurements <- egResult$out;
  tresultMatrix <- rbind(tresultMatrix, etMeasurements[1,]);
  tdataRowNames <- c(tdataRowNames, "DTree");
  
  # Lasso
  # egResult <- efKFCV(t(kMatrix), egClassLabel, 3, "Lasso");
  #etMeasurements <- egResult$out;
  #tresultMatrix <- rbind(tresultMatrix, etMeasurements[1,]);
  #tdataRowNames <- c(tdataRowNames, "Lasso");
  
  # KNN
  egResult <- efKFCV(t(kMatrix), egClassLabel, 3, "KNN");
  etMeasurements <- egResult$out;
  tresultMatrix <- rbind(tresultMatrix, etMeasurements[1,]);
  tdataRowNames <- c(tdataRowNames, "KNN");
  
  rownames(tresultMatrix) <- tdataRowNames;
  colnames(tresultMatrix) <- tdataColNames;
  
  return ( tresultMatrix );
}

efClassToInt<-function(classes)
{
  levelsClass <- sort(levels(as.factor(classes)));
  #for(i in levelsClass)
  for(i in levelsClass)
  {
    classes<-replace(classes,classes==i,match(i,levelsClass)-1);
    #classes <- replace(classes, classes==levelsClass[i], i-1);
  }
  classes <- (as.numeric(classes));
  return (classes);
}

color.map <- function(tempClass)
{
  if( tempClass=='P' )
    'red'
  else
    'blue';
}




plotfunction<-function(sta,nums){
  set.seed(0);
  egStart <- sta;
  egTopK<-nums;
  vectorMCC <- c();
  nameMCC   <- c();
  for( i in 1:egTopK )
  {
    indexTopRank <- which ( (egRank>=egStart) & (egRank<=(egStart+i-1)) );
    if( length(indexTopRank)==1 )
    {
      indexTopRank <- indexTopRank[c(1,1)];
    }
    tResultMatrix <- efPerformanceMatrix( egSmallMatrix[indexTopRank,]);
    # SVM, Acc
    vectorMCC[i] <- max(tResultMatrix[, 3]);
    nameMCC[i]   <- egStart+i-1;
  }
  names(vectorMCC) <- nameMCC;
  egTitle <- paste("RIFS: ", egStart, "-", egStart+egTopK-1, sep="");
  plot(nameMCC, vectorMCC, type="b", ylim=c(0, 1), main=egTitle, ylab="Max Acc");
  
}




dowork1 <- function(start,egTopK1)
{
  
  MaxAcc<-0;
  MaxPoint<-0;
  NumbefMaxAcc<-0;
  set.seed(0);
  egStart <- start;
  egTopK<-egTopK1;
  vectorMCC <- c();
  nameMCC   <- c();
  
  
  
  for( i in 1:egTopK )
  {
    indexTopRank <- which ( (egRank>=egStart) & (egRank<=(egStart+i-1)) );
    if( length(indexTopRank)==1 ){
      indexTopRank <- indexTopRank[c(1,1)];
    }
    tResultMatrix <- efPerformanceMatrix( egSmallMatrix[indexTopRank,]);
    # SVM, Acc
    vectorMCC[i] <- max(tResultMatrix[, 3]);
    if(vectorMCC[i]>MaxAcc){
      MaxAcc<-vectorMCC[i];
      MaxPoint<-egStart;
      NumbefMaxAcc<-i;
    }
    # MaxAcc;
    nameMCC[i]   <- egStart+i-1;
  }
  names(vectorMCC) <- nameMCC;
  egTitle <- paste("RIFS: ", egStart, "-", egStart+egTopK-1, sep="");
  
  plot(nameMCC, vectorMCC, type="b", ylim=c(0, 1), main=egTitle, ylab="Max Acc");
  
  # plot(nameMCC, vectorMCC, type="b", ylim=c(0, 1), main=egTitle, ylab="SVM Acc");
  
  # avervectorMcc<-mean(vectorMCC);
  return (c(MaxAcc,MaxPoint,NumbefMaxAcc));
}







dowork <- function(start,egTopK1){
  MaxAcc<-0;
  MaxPoint<-0;
  NumbefMaxAcc<-0;
  set.seed(0);
  vectorMCC <- c();
  nameMCC   <- c();
  egStart <- start;
  egTopK<-egTopK1;
  Maxresult<-c(0,0,0,0);
  
  
  for( i in 1:egTopK )
  {
    indexTopRank <- which ( (egRank>=egStart) & (egRank<=(egStart+i-1)) );
    if( length(indexTopRank)==1 ){
      indexTopRank <- indexTopRank[c(1,1)];
    }
    tResultMatrix <- efPerformanceMatrix( egSmallMatrix[indexTopRank,]);
    # SVM, Acc
    vectorMCC[i] <- max(tResultMatrix[, 3]);
    if(vectorMCC[i]>MaxAcc){
      MaxAcc<-vectorMCC[i];
      MaxPoint<-egStart;
      NumbefMaxAcc<-i;
    }
  }
  
  Maxresult[1]<-MaxAcc;
  Maxresult[2]<-MaxPoint;
  Maxresult[3]<-NumbefMaxAcc;
  
  
  
  
  
  if((Maxresult[3] < 3)&(Maxresult[2]!=1)) {
    count <- round(egTopK/2); 
    countdown <- 0;
    n<-1;
    k<-0;
    Maxresult1<-c(0,0,0);
      while((countdown <= count)&((Maxresult[2]-n)>=1)){
        set.seed(0);
        for(i in 1:(n+egTopK)){
          indexTopRank <- which ( (egRank>=Maxresult[2]-n) & (egRank<=Maxresult[2]-n+i-1) );
          if( length(indexTopRank)==1 ){
            indexTopRank <- indexTopRank[c(1,1)];
          }
          tResultMatrix <- efPerformanceMatrix( egSmallMatrix[indexTopRank,]);
          tempmax <- max(tResultMatrix[, 3]);
          if(tempmax>Maxresult1[1])
          {
            Maxresult1[1]<-tempmax;
            
            Maxresult1[3]<-i;
          }
          
        }
        
        
        if(Maxresult1[1]<=Maxresult[1]){
          countdown<-countdown+1;
        }else{
          Maxresult[1]<-Maxresult1[1];
          k<-n;
          Maxresult[3]<-Maxresult1[3];
          
        }
        
        n<-n+1;
      }
      Maxresult[2]<- Maxresult[2]-k;
    }
  
  
  #继续向后寻找最大MACC
  if(Maxresult[3]>=3){
    i<-1;
    count <- round(egTopK/2); 
    countdown <- 0;
    k<-0;
    while((countdown <= count)&((Maxresult[2]+egTopK+i)<=egNumSmall)){
      
      indexTopRank <- which ( (egRank>=Maxresult[2]) & (egRank<=Maxresult[2]+egTopK-1+i) );
      tResultMatrix <- efPerformanceMatrix( egSmallMatrix[indexTopRank,]);
      tempmax <- max(tResultMatrix[, 3]);
      if(Maxresult[1]<tempmax){
        k<-i;
        Maxresult[1]<-tempmax;
      }else{
        countdown<-countdown+1;
      }
      i<-i+1;
      
      
    }
    if(k!=0){
      Maxresult[3]<-egTopK+k;
    }
    
  }
  
  endnumber<-0;
  if(Maxresult[2]<egStart){
    endnumber<-egStart-Maxresult[2]+egTopK;
    
  }else if((Maxresult[3]>egTopK)&(Maxresult[2]=egStart)){
    endnumber<-Maxresult[3];
    
  }else{
    endnumber<-egTopK;
    
  }
  for( i in 1:endnumber)
  {
    nameMCC[i]   <- Maxresult[2]+i-1;
  }
  Maxresult[4]<-endnumber;
  #plo1<-as.numeric(Maxresult[2]);
  #plo2<-as.numeric(Maxresult[4]);
  #plotfunction(plo1,plo2);
  return (c(Maxresult[1],Maxresult[2],Maxresult[3],Maxresult[4]));
}

finalfunction<-function(numrd,Numnamemcc)
{
  numRd1<-numrd;
  Numnamemcc1<-Numnamemcc;
  
  Maxresult <- c(0,0,0);
  
  top20 <- c(1:20);
  for (h in top20)
  {
    temp <- dowork(h,Numnamemcc1);
    if(temp[1]>Maxresult[1])
    {
      Maxresult[1]<-temp[1];
      Maxresult[2]<-temp[2];
      Maxresult[3]<-temp[3];
      Maxresult[4]<-temp[4];
    }
  }
  
  if(Maxresult[1]<1){
    rd <- round(runif(numRd1,1,egNumSmall-Numnamemcc1));
    result <- matrix(nrow=numRd1,ncol=2);
    for (h in rd)
    {
      temp <- dowork(h,Numnamemcc1);
      if(temp[1]>Maxresult[1])
      {
        Maxresult[1]<-temp[1];
        Maxresult[2]<-temp[2];
        Maxresult[3]<-temp[3];
        Maxresult[4]<-temp[4];
      }
    }
  }
  ###########################################################
  
  
  indexTopRank <- which ( (egRank>=Maxresult[2]) & (egRank<=Maxresult[2]+Maxresult[3]-1) );
  finalmatrix <- row.names(egSmallMatrix[indexTopRank,]);
  return(c(Maxresult[1:4],finalmatrix[1:length(finalmatrix)]));
}


### End of function definition

#datasetsname <- c("1CNS.csv","1Colon.csv","1ALL4.csv","1ALL3.csv","1ALL2.csv","1ALL1.csv","1DLBCL.csv","1Gastric.csv","1Gastric1.csv","1Gastric2.csv","1Leukaemia.csv","1Lymphoma.csv","1Myeloma.csv","1Prostate.csv","1Stroke.csv","1t1d.csv");
#classesnames <- c("CNSclass.csv","Colonclass.csv","ALL4class.csv","ALL3class.csv","ALL2class.csv","ALL1class.csv","DLBCLclass.csv","Gastricclass.csv","Gastric1class.csv","Gastric2class.csv","Leukaemiaclass.csv","Lymphomaclass.csv","Myelomaclass.csv","Prostateclass.csv","Strokeclass.csv","t1dclass.csv");
#outfilename <- c("CNS_out.csv","Colon_out.csv","ALL4_out.csv","ALL3_out.csv","ALL2_out.csv","ALL1_out.csv","DLBCL_out.csv","Gastric_out.csv","Gastric1_out.csv","Gastric2_out.csv","Leukaemia_out.csv","Lymphoma_out.csv","Myeloma_out.csv","Prostate_out.csv","Stroke_out.csv","t1d_out.csv");
datasetsname <- c("1Adenoma.csv");
classesnames <- c("Adenomaclass.csv");
outfilename <- c("Adenoma_out.csv");





for(counter in 1:16){ 
  # Initialization: loading the dataset
  egMatrix <- read.csv(datasetsname[counter], header=TRUE, sep=",", row.names=1);
  egClass <- read.csv(classesnames[counter], header=TRUE, sep=",", row.names=1);
  indexP <- which(egClass$Class == "P");
  indexN <- which(egClass$Class == "N");
  egClassLabel <- efClassToInt(as.numeric(egClass$Class));
  
  egNumSmall <- nrow(egMatrix);
  
  egSmallMatrix <- egMatrix[1:egNumSmall,];
  dataRowNames <- row.names(egSmallMatrix);
  resultMatrix <- matrix(nrow=nrow(egSmallMatrix),ncol=0);
  #dataColNames <- c("#Feature");
  dataColNames <- c();
  
  # Two sample t-test
  #! N vs P
  #dataTest <- apply(egSmallMatrix, 1, function(x) t.test(x ~ egClass$Class));
  
  dataTest <- apply(egSmallMatrix, 1, function(x) t.test(x ~ egClass$Class[c(indexP, indexN)]));
  # retrieved values: t and P-value
  dataFTest <- lapply( dataTest, function(x) c(as.numeric(x[1]), as.numeric(x[3])) );
  dataFTest <- unlist(dataFTest);
  dim(dataFTest) <- c(2, egNumSmall);
  dataFTest <- t(dataFTest);
  
  resultMatrix <- cbind(resultMatrix, dataFTest);
  dataColNames <- cbind(dataColNames, "Ttest t", "Ttest Pvalue");
  colorCol <- unlist(lapply(egClass$Class, color.map));
  
  #egTopK <- 5;
  egRank <- rank(resultMatrix[,2]);
  
  par(mfrow=c(2,2));
  
  
  finalmatrix <- finalfunction(4000,5);
  m1 <- finalmatrix[1:3];
  m2 <- finalmatrix[5:length(finalmatrix)];
  m3 <- finalmatrix[4];
  
  plo1<-as.numeric(m1[2]);
  plo2<-as.numeric(m3);
  plotfunction(plo1,plo2);
  write.table(c(m1,m2),file=outfilename[counter],sep = ",");
}
