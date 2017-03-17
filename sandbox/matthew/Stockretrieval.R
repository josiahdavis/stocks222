library(quantmod)
#Use stockSymbols to get the name of the stocks on the NYSE.
symbols=stockSymbols()
symb<-symbols[symbols[,8]=="NYSE",][,1]
stocklist=list()
usedsymb=NULL
j=1
for (i in 1:length(symb)) {
  #We have to test each symbol to make sure we can download it.
  tes=try(getSymbols.yahoo(Symbols=symb[i], env=.GlobalEnv, from="1980-01-01"))
  if(!inherits(tes, "try-error")) {
    #getSymbols will download the data for each stock back to 1980.
    getSymbols.yahoo(Symbols=symb[i], env=.GlobalEnv, from="1980-01-01")
    usedsymb=c(usedsymb, symb[i])
    stocklist[[j]]=get(symb[i])
    j=j+1
  }
}
names(stocklist) <- usedsymb
stocklist[[1]]
#Save the data to an .RData file so we don't have to redownload the data to get it again.
save(stocklist, file='stocks.RData')

#use load('stocks.RData') to get get the data back if needed.
usymb=names(stocklist)
#MRet wil hold the monthly returns for each stock.
MRet=NULL
for (i in 1:length(usymb)){
  MRet=cbind(MRet, monthlyReturn(stocklist[[i]]))
}

colnames(MRet) <- usymb
#MR90 will hold the returns from 1986 to 2016
MR86 = MRet[as.character(1986:2016),which(!is.na(MRet['1986-01']))]

#In general, it is not certain that this procedure will always remove the NA values as desired.
#This means that if different returns or dates are needed, careful analysis is needed to remove the NAs.

#To check that it worked as intended, check to see that it has the number of motnhly returns expected
#Also check that it has one return for each month, at the end of the month.
#Also check that there are no NAs left.

#First we must remove the rows that all NAs.
allnarows=NULL
for (j in 1:dim(MR86)[1]) {
  allnarows[j]=all(is.na(MR86[j,]))
}
MR862 = MR86[-which(allnarows),]

#Remove all rows for which the our first stock has missing values.
MR863=MR862[-which(is.na(MR862[,1])),]

#Remove any columns that have NA values remaining.
MR864 = MR863[,-which(is.na(colMeans(MR863)))]

#Write to a csv file for future use.
write.csv(MR864, file="monthlyreturnsNYSE1986.csv")
