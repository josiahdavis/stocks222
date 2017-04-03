import csv
import numpy as np
import cvxpy as cvx
import matplotlib.pyplot as plt


training_years = 5 # number of years used to estimate the expected return and covariance matrix
test_years = 1 # number of years to keep the portfolio run
year_start = 1991 # the first year to run the portfolio, 1991 because the data starts from 19860101
year_end = 2016 # the last year to run the portfolio, not inclusive


def load_dataset():
    '''
       dataset shoule have the monthly return,
       each row for a given month,
       and each column for a given equity,
       in the example, 360(months) * 201(equities)
    '''
    mydata = np.genfromtxt ('sp500_monthlyreturn_19860101_20160101_nonames.csv', delimiter=",")
    return mydata


def preprocessing(allReturns, Year):
    ''' allReturns is a 360 * 201 matrix of all the returns from 19860101 to 20151231,
        Year is any year we want to keep the portfolio running,
        the previous 5 years is used to estimate the r_hat and Sigma,
        1991 - 2015 is valid as input Year
       
    '''
    training_start = 12 * (Year - year_start)
    training_end = training_years * 12 + 12 * (Year - year_start)
    test_start = training_end 
    test_end = training_end + test_years * 12
    training_data = allReturns[training_start:training_end,:]
    test_data = allReturns[test_start:test_end,:]
    r_hat = np.transpose(training_data.mean(axis = 0))
    r_hat.shape = (r_hat.shape[0], 1)  # N * 1
    sigma = np.cov(np.transpose(training_data))
    return (training_data, test_data, r_hat, sigma)

def calc_equal_weight(training_data): 
    '''
       calculate the mean/sd of monthly return of an equally distributed 
       portfolio for the training period(5 years/60 months)
    '''
    N = training_data.shape[1]
    train_equal_return = np.dot(training_data, np.ones((N, 1))/N);
    equal_weight_mean = np.mean(train_equal_return)
    equal_weight_sd = np.std(train_equal_return)
    return (equal_weight_mean, equal_weight_sd)

def minimize_var(training_data, test_data, r_hat, sigma, tau, equal_weight_return):
    '''
       Solve a min-variance optimization problem with l1-norm,
       tau is a parameter
    '''
    N = training_data.shape[1]
    one_N = np.ones((1, N))
    r_hat_T = np.transpose(r_hat)
    # variable
    x = cvx.Variable(N)
    # constraints
    constraints = [one_N * x == 1 ,
                   r_hat_T * x >= equal_weight_return]
    # problem
    obj = cvx.Minimize( cvx.quad_form(x, sigma) + tau * cvx.norm(x, 1))
    prob = cvx.Problem(obj, constraints)
    prob.solve() 
    # retrieve results 
    optimal_value = prob.value
    optimal_x = x.value
    # ignore the x's due to round-off error
    optimal_x = np.around(optimal_x, decimals = 4)
    optimal_x =  optimal_x/sum(optimal_x)
    return (optimal_value, optimal_x)


if __name__ == "__main__":
 
    mydata = load_dataset() 
    taus1 = np.linspace(1.0e-5, 1.0e-4, num = 10)
    taus2 = np.linspace(2.0e-4, 1.0e-3, num = 9)
    taus3 = np.linspace(2.0e-3, 1.0e-2, num = 9)
    taus4 = np.linspace(2.0e-2, 1.0e-1, num = 9)
    taus5 = np.linspace(2.0e-1, 1.0, num = 9)
    taus = np.concatenate((taus1, taus2, taus3, taus4, taus5), axis = 0 )
    N_equity = mydata.shape[1] # 201
    N_tau = taus.shape[0] # 46
    N_years = year_end - year_start #25

    # solve the problem for different years, and different taus
    x_optimal_year_tau = np.zeros((N_equity, N_tau ,N_years)) # all years and all taus
    x_optimal_year = np.zeros((N_equity, N_years)) # each year with best tau
    tau_optimal_year = np.zeros((1, N_years))
    monthly_return_year = np.zeros((12, N_years))
    monthly_return_equal_year = np.zeros((12, N_years))
    num_assets = np.zeros((1, N_years))
    #
    for year in range(year_start, year_end):
        print ('current year is ' + str(year))
        (mytraining_data, mytest_data, myr_hat, mysigma) = preprocessing(mydata, year)
        (myequal_weight_mean, myequal_weight_sd) = calc_equal_weight(mytraining_data)
        for i in range(N_tau):
            (myoptimal_value, myoptimal_x) = minimize_var(mytraining_data, mytest_data, myr_hat
            , mysigma, taus[i], myequal_weight_mean)
            myoptimal_x.shape = (myoptimal_x.shape[0],)
            x_optimal_year_tau[:,i ,year - year_start] = myoptimal_x
        # uncomment the below lines to output the full results for each year    
        filename = 'minimize_variance_' + str(year) + '.csv'
        np.savetxt(filename, x_optimal_year_tau[:,:, year - year_start], delimiter=",")
    # choose the best tau for each year    
        tau_optimal_index = 0
        sr_optimal = -9999
        for i in range(N_tau):
            tmp = x_optimal_year_tau[:,i ,year - year_start]
            tmp2 = tmp[tmp >= 0]
            if (tmp2.shape[0] == tmp.shape[0]):   # no short(all elements >= 0) 
                tmp_return = np.dot(mytraining_data, tmp)
                tmp_return_mean = np.mean(tmp_return)
                tmp_return_sd = np.std(tmp_return)
                sr = tmp_return_mean/max(tmp_return_sd, 1e-16)
                if sr > sr_optimal:
                    tau_optimal_index = i
                    sr_optimal = sr
        x_optimal_year[:, year - year_start] = x_optimal_year_tau[:,tau_optimal_index ,year - year_start]
        x_optim = x_optimal_year[:, year - year_start]
        x_optim = x_optim[x_optim > 0]
        num_assets[0,year - year_start] = x_optim.shape[0]
        tau_optimal_year[0,year - year_start] = taus[tau_optimal_index]
        monthly_return_year[:, year - year_start] = np.dot(mytest_data, x_optimal_year[:, year - year_start])
        monthly_return_equal_year[:, year - year_start] = mytest_data.mean(axis = 1)
    np.savetxt('num_assets.csv', num_assets, delimiter=",")
    np.savetxt('x_optimal_year.csv', x_optimal_year, delimiter=",")
    np.savetxt('monthly_return_year.csv', monthly_return_year, delimiter=",")
    np.savetxt('tau_optimal_year.csv', tau_optimal_year, delimiter=",")
    np.savetxt('monthly_return_equal_year.csv', monthly_return_equal_year, delimiter=",")

   








        