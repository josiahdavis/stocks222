import csv
import numpy as np
import cvxpy as cvx
import matplotlib.pyplot as plt
import random as rd

training_years = 5 # number of years used to estimate the expected return and covariance matrix
test_years = 1 # number of years to keep the portfolio run
year_start = 1996 # the first year to run the portfolio, 1991 because the data starts from 19860101
year_offset = 1991
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
    training_start = 12 * (Year - year_offset)
    training_end = training_years * 12 + 12 * (Year - year_offset)
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

    # recover all the data
    x_optimal_year = np.genfromtxt ('x_optimal_year.csv', delimiter=",")
    monthly_return_year = np.genfromtxt ('monthly_return_year.csv', delimiter=",")
    monthly_return_equal_year = np.genfromtxt ('monthly_return_equal_year.csv', delimiter=",")
    tau_optimal_year = np.genfromtxt ('tau_optimal_year.csv', delimiter=",")
    num_assets = np.genfromtxt ('num_assets.csv', delimiter=",")

    # plot the "best return" vs the return of the equally distributed portfolio
    plt.plot(range(year_start, year_end), monthly_return_year.mean(axis = 0), label="Best sparse model")
    plt.plot(range(year_start, year_end), monthly_return_equal_year.mean(axis = 0), label = "Equally distributed")
    #print monthly_return_year.mean(axis = 0) - monthly_return_equal_year.mean(axis = 0)
    plt.legend()
    plt.ylabel('Mean of monthly return')
    plt.xlabel('Year')
    plt.savefig('best_monthly_return.jpg', dpi=600)
    plt.show()
    plt.close("all")

    # plot the "best return" vs the return of the equally distributed portfolio
    plt.plot(range(year_start, year_end), monthly_return_year.std(axis = 0), label="Best sparse model")
    plt.plot(range(year_start, year_end), monthly_return_equal_year.std(axis = 0), label = "Equally distributed")
    print monthly_return_year.std(axis = 0) - monthly_return_equal_year.std(axis = 0)
    plt.legend()
    plt.ylabel('Std of monthly return')
    plt.xlabel('Year')
    plt.savefig('best_monthly_std.jpg', dpi=600)
    plt.show()
    plt.close("all")
    
    # plot the "best return" vs the return of the equally distributed portfolio
    plt.bar(range(year_start, year_end), num_assets, label="Best sparse model")
    plt.legend()
    plt.ylabel('Number of assets')
    plt.xlabel('Year')
    plt.savefig('best_monthly_num_asset.jpg', dpi=600)
    plt.show()
    plt.close("all")

    # 
    # rd.seed(0)
    # num_samples = 1000
    # sample_mean_std = np.zeros((2,num_samples, N_years))
    # for year in range(year_start, year_start+1):
    #     print ('current year is ' + str(year))
    #     # size_portfolio = int(num_assets[year - year_start])
    #     (mytraining_data, mytest_data, myr_hat, mysigma) = preprocessing(mydata, year)
    #     (myequal_weight_mean, myequal_weight_sd) = calc_equal_weight(mytraining_data)

    #     for k in range(num_samples):
    #         sample_weights = np.zeros((1, N_equity))
    #         for i in range(N_equity):
    #             tmp = rd.uniform(0,1)
    #             sample_weights[0,i] = tmp
    #         sample_weights = sample_weights/np.sum(sample_weights)
    #         sample_x = np.zeros(( N_equity, 1))
    #         for j in range(N_equity):
    #             sample_x[j, 0] = sample_weights[0,j]
    #         sample_return = np.dot(mytraining_data, sample_x)
    #         sampled_mean = np.mean(sample_return)
    #         sampled_std = np.std(sample_return)
    #         sample_mean_std[0, k, year - year_start] = sampled_mean
    #         sample_mean_std[1, k, year - year_start] = sampled_std
    #     # plot a scatter plot
    #     plt.scatter(sample_mean_std[0, :, year - year_start], sample_mean_std[1, :, year - year_start], label="Best sparse model")
    #     #plt.legend
    #     plt.ylabel('Mean of monthly return')
    #     plt.xlabel('sd of monthly return')
    #     #plt.savefig('best_monthly_return.jpg')
    #     plt.show()
    #     plt.close("all")

        # print sample_weights
        # print np.sum(sample_weights)

    #     for i in range(N_tau):
    #         (myoptimal_value, myoptimal_x) = minimize_var(mytraining_data, mytest_data, myr_hat
    #         , mysigma, taus[i], myequal_weight_mean)
    #         myoptimal_x.shape = (myoptimal_x.shape[0],)
    #         x_optimal_year_tau[:,i ,year - year_start] = myoptimal_x
    #     # uncomment the below lines to output the full results for each year    
    #     filename = 'minimize_variance_' + str(year) + '.csv'
    #     np.savetxt(filename, x_optimal_year_tau[:,:, year - year_start], delimiter=",")
    # # choose the best tau for each year    
    #     tau_optimal_index = 0
    #     sr_optimal = -9999
    #     for i in range(N_tau):
    #         tmp = x_optimal_year_tau[:,i ,year - year_start]
    #         tmp2 = tmp[tmp >= 0]
    #         if (tmp2.shape[0] == tmp.shape[0]):   # no short(all elements >= 0) 
    #             tmp_return = np.dot(mytraining_data, tmp)
    #             tmp_return_mean = np.mean(tmp_return)
    #             tmp_return_sd = np.std(tmp_return)
    #             sr = tmp_return_mean/max(tmp_return_sd, 1e-16)
    #             if sr > sr_optimal:
    #                 tau_optimal_index = i
    #                 sr_optimal = sr
    #     x_optimal_year[:, year - year_start] = x_optimal_year_tau[:,tau_optimal_index ,year - year_start]
    #     x_optim = x_optimal_year[:, year - year_start]
    #     x_optim = x_optim[x_optim > 0]
    #     num_assets[0,year - year_start] = x_optim.shape[0]
    #     tau_optimal_year[0,year - year_start] = taus[tau_optimal_index]
    #     monthly_return_year[:, year - year_start] = np.dot(mytest_data, x_optimal_year[:, year - year_start])
    #     monthly_return_equal_year[:, year - year_start] = mytest_data.mean(axis = 1)
    # np.savetxt('num_assets', num_assets, delimiter=",")
    # np.savetxt('x_optimal_year.csv', x_optimal_year, delimiter=",")
    # np.savetxt('monthly_return_year.csv', monthly_return_year, delimiter=",")
    # np.savetxt('tau_optimal_year.csv', tau_optimal_year, delimiter=",")
    # np.savetxt('monthly_return_equal_year.csv', monthly_return_equal_year, delimiter=",")

   








        