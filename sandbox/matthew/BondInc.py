import numpy as np
import pandas as pd
import cvxpy as cvx
import pandas_datareader.data as web
import datetime

#For initial Bond Data, we'll use 10 year Yields from data FRED(Federal Reserve Economic Data (St. Louis)).
start = datetime.datetime(1991, 1, 1)
end = datetime.datetime(2016, 12, 31)
Bond10 = web.DataReader("GS10", "fred", start, end)

#Get the monthly returns from our csv
mon=pd.read_csv('monthlyreturnsNYSE1986.csv')

mon.drop(mon.columns[[0]], axis=1, inplace=True)

#rhat are the yearly returns, obtained from our monthly returns.
#Probably shouldn't be called rhat, as it isn't expected returns.
rhat = (mon.ix[0:11,:]+1).apply(np.prod, axis=0)

for i in range(1, 31):
	test=(mon.ix[i*12:i*12+11,:]+1).apply(np.prod, axis=0)
	rhat=np.vstack([rhat, test])

#returns for equally weighting each stock starting in 1995 to 2016
np.mean(np.cumprod(rhat[5:27],axis=0), axis=1)
	
#rhat1: Our expected yearly returns
rhat1=np.power(np.prod(rhat[:5,:], axis=0),1./5)
#sigma: initial covariance matrix
sigma=np.cov(mon.ix[:59,:], rowvar=False)
#The number of stocks.
N=rhat1.shape[0]
#sigma1 the covariance matrix with 0's added to represent how the bonds have zero volatility.
#I expect this isn't the best (or even appropriate) way to handle bonds, but am not certain of a better method.
sigma1=np.vstack((sigma, np.zeros((1,N))))

sigma1=np.hstack((sigma1, np.zeros((N+1,1))))

Bondret = float(Bond10['1991'].iloc[0])/100
#rhat2 expected returns with bond yield.
rhat2 = np.hstack((rhat1, Bondret+1))
#goal, The minimum returns we're aiming for.
#arbitrarily picked, should use something else. 
goal = np.power(np.prod(np.mean(rhat[0:4], axis=1)),1./5)
#Percentage of our money we'l invest in bonds.
#This is specified as if it isn't, we'll get at least 40% in the bonds, and likely more, depending on the yield on stocks.
Bondam = .2
BondInc = .2

#tau constraint value
#tau chosen somewhat arbitrarily.  We want a large value to prevent shorting, but my initial analysis shows no significant difference for minute changes.
tau=.7
#Below is the optimization problem.
x=cvx.Variable(N+1)
constraints = [np.ones((1, N+1)) * x == 1,
				np.transpose(rhat2) * x >= .95,
				x[N] == Bondam]
obj = cvx.Minimize( cvx.quad_form(x, sigma1) + tau * cvx.norm(x, 1))
prob = cvx.Problem(obj, constraints)
prob.solve()
#Round to eliminate extremely small values to get sparsity.
something=np.around(x.value, 4)
xnew = rhat[5][:,np.newaxis] * something[0:N]
#portret are the returns our portfolio will give us.
portret =  [np.sum(xnew)+Bondam*(float(Bond10['1991'].iloc[0])/100+1)]
#xnew holds our is our investment in stocks at the end of the year.
Bondcheck = np.array(float(Bond10['1991'].iloc[0])/100)
xnew = np.append(xnew, Bondam)

#Now we use a for loop to get our portfolio returns through 2016.
for year in range(1992, 2017):
	i = year - 1991
	rhatc = np.power(np.prod(rhat[i:i+5,:], axis=0),1./5)
	sigmac = np.cov(mon.ix[12*i:12*(i+5)-1,:], rowvar=False)
	sigmad=np.vstack((sigmac, np.zeros((1,N))))
	sigmad=np.hstack((sigmad, np.zeros((N+1,1))))
	#year -i$10 will change the bond we use every 10 years.
	Bondretold = Bondret
	Bondret = float(Bond10[str(year - i%10)].iloc[0])/100
	Bondcheck = np.append(Bondcheck, Bondret)
	rhatd = np.hstack((rhatc, Bondret+1))
	goal = np.power(np.prod(np.mean(rhat[i:(i+5)], axis=1)), 1./5)
	#This optimization problem differs in that we're merely adjusting the number of stocks we get.
	#Initial analysis shows that each change is sparse; needs to be checked thoroughly.
	u = cvx.Variable(N+1)
	xn = u + xnew
	#We can't compound US bond coupons, so we'll instead reinvest them in our stocks.
	if i%10 == 0:
		constraintsb = [np.ones((1, N+1)) * u == Bondam * Bondretold,
						xn[N] == Bondam + BondInc,
						np.transpose(rhatd) * xn >= .95 * portret[i-1]]
	else:
		constraintsb = [np.ones((1, N+1)) * u == Bondam * Bondretold,
						xn[N] == Bondam,
						np.transpose(rhatd) * xn >= .95 * portret[i-1]]
	objb = cvx.Minimize( cvx.quad_form(xn, sigmad) + tau * cvx.norm(xn, 1))
	probc = cvx.Problem(objb, constraintsb)
	probc.solve()
	if i%10 == 0:
		Bondam = Bondam + BondInc
	something = np.around(xn.value, 4)
	xnew = rhat[i+5][:,np.newaxis] * something[0:N]
	portret = np.hstack((portret, np.sum(xnew)+Bondam*(1+Bondret)))
	xnew = np.append(xnew, Bondam)
