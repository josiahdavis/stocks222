import csv
import numpy as np
import cvxpy as cvx
import matplotlib.pyplot as plt
import random as rd
import math

training_years = 5 # number of years used to estimate the expected return and covariance matrix
test_years = 1 # number of years to keep the portfolio run
year_start = 1991 # the first year to run the portfolio, 1991 because the data starts from 19860101
year_offset = 1991
year_end = 2016 # the last year to run the portfolio, not inclusive


if __name__ == "__main__":

    # recover all the data
    x_optimal_year = np.genfromtxt ('x_optimal_year.csv', delimiter=",")
    monthly_return_year = np.genfromtxt ('monthly_return_year.csv', delimiter=",")
    monthly_return_equal_year = np.genfromtxt ('monthly_return_equal_year.csv', delimiter=",")
    tau_optimal_year = np.genfromtxt ('tau_optimal_year.csv', delimiter=",")
    num_assets = np.genfromtxt ('num_assets.csv', delimiter=",")

    # try to claculate the cumulative return from 1991 to 2015
    gain_log_optimal = monthly_return_year + np.ones((monthly_return_year.shape[0], monthly_return_year.shape[1]))
    gain_log_equal = monthly_return_equal_year + np.ones((monthly_return_equal_year.shape[0], monthly_return_equal_year.shape[1]))
    f = np.vectorize(math.log)
    g = np.vectorize(math.exp)
    gain_log_optimal = f(gain_log_optimal)
    gain_log_equal = f(gain_log_equal)
    yearly_gain_optimal = g(gain_log_optimal.sum(axis = 0))
    yearly_gain_equal = g(gain_log_equal.sum(axis = 0))
    # compute compounded return for each year
    h = np.vectorize(math.pow)
    compounded_return_optimal = h(yearly_gain_optimal, 1./12) - 1.
    compounded_return_equal = h(yearly_gain_equal, 1./12) - 1.
    #print(compounded_return_optimal)
    #print(compounded_return_equal)

    # try to claculate the cumulative return from 1991 to 2015, assuming a 3% dividend yearly
    # gain_log_optimal = monthly_return_year + np.ones((monthly_return_year.shape[0], monthly_return_year.shape[1]))
    # gain_log_equal = monthly_return_equal_year + np.ones((monthly_return_equal_year.shape[0], monthly_return_equal_year.shape[1]))
    # f = np.vectorize(math.log)
    # g = np.vectorize(math.exp)
    # gain_log_optimal = f(gain_log_optimal)
    # gain_log_equal = f(gain_log_equal)
    # yearly_gain_optimal = g(gain_log_optimal.sum(axis = 0)) - 0.03
    # yearly_gain_equal = g(gain_log_equal.sum(axis = 0)) - 0.03
    #print(compounded_return_optimal)
    #print(compounded_return_equal)



    #print(yearly_gain_optimal)
    #print(yearly_gain_equal)
    yearly_gain_optimal_log = f(yearly_gain_optimal)
    yearly_gain_equal_log = f(yearly_gain_equal)
    net_value_optimal = g(np.cumsum(yearly_gain_optimal_log))
    net_value_equal = g(np.cumsum(yearly_gain_equal_log))
    print(net_value_equal)
    print(net_value_optimal)
    print(net_value_equal.shape)
    print(net_value_optimal.shape)
    net_value_optimal = np.append([1], net_value_optimal)
    net_value_equal = np.append([1], net_value_equal)
    # plot the cumulative value 
    plt.plot(range(year_start - 1, year_end), net_value_optimal, label="Best sparse model")
    plt.plot(range(year_start - 1, year_end), net_value_equal, label = "Equally distributed")
    #print monthly_return_year.mean(axis = 0) - monthly_return_equal_year.mean(axis = 0)
    plt.legend()
    plt.ylabel('Cumulative value')
    plt.xlabel('Year')
    plt.xlim((1990, 2015))
    plt.ylim((0, 55))
    plt.savefig('mean_variance_cumulative.jpg', dpi=600)
    plt.show()
    plt.close("all")
    
    # plot the "best return" vs the return of the equally distributed portfolio
    plt.plot(range(year_start, year_end), monthly_return_year.mean(axis = 0)/monthly_return_year.std(axis = 0), label="Best sparse model")
    plt.plot(range(year_start, year_end), monthly_return_equal_year.mean(axis = 0)/monthly_return_equal_year.std(axis = 0), label = "Equally distributed")
    #print monthly_return_year.mean(axis = 0) - monthly_return_equal_year.mean(axis = 0)
    plt.legend()
    temp = monthly_return_year.mean(axis = 0)/monthly_return_year.std(axis = 0) - monthly_return_equal_year.mean(axis = 0)/monthly_return_equal_year.std(axis = 0)
    temp = temp[temp > 0] #13
    print('temp_Sharpe_ratio ' + str(len(temp)))
    plt.ylabel('Sharpe ratio in a year')
    plt.xlabel('Year')
    plt.xlim((1991, 2015))
    plt.xticks([1991, 1995, 2000, 2005, 2010, 2015])
    plt.savefig('mean_variance_sr.jpg', dpi=600)
    plt.show()
    plt.close("all")


    # plot the "best return" vs the return of the equally distributed portfolio
    plt.plot(range(year_start, year_end), compounded_return_optimal, label="Best sparse model")
    plt.plot(range(year_start, year_end), compounded_return_equal, label = "Equally distributed")
    #print monthly_return_year.mean(axis = 0) - monthly_return_equal_year.mean(axis = 0)
    plt.legend()
    plt.ylabel('Compounded monthly return in a year')
    plt.xlabel('Year')
    plt.xlim((1991, 2015))
    plt.xticks([1991, 1995, 2000, 2005, 2010, 2015])
    #plt.ylim((0, 50))
    plt.savefig('mean_variance_c_return.jpg', dpi=600)
    plt.show()
    plt.close("all")

    # plot the "best return" vs the return of the equally distributed portfolio
    plt.plot(range(year_start, year_end), monthly_return_year.mean(axis = 0), label="Best sparse model")
    plt.plot(range(year_start, year_end), monthly_return_equal_year.mean(axis = 0), label = "Equally distributed")
    #print monthly_return_year.mean(axis = 0) - monthly_return_equal_year.mean(axis = 0)
    temp = monthly_return_year.mean(axis = 0) - monthly_return_equal_year.mean(axis = 0)
    temp = temp[temp > 0] #13
    print('temp_monthly_Return ' + str(len(temp)))
    plt.legend()
    plt.ylabel('Average of monthly return in a year')
    plt.xlabel('Year')
    plt.xlim((1991, 2015))
    plt.xticks([1991, 1995, 2000, 2005, 2010, 2015])
    plt.savefig('mean_variance_monthly_return.jpg', dpi=600)
    plt.show()
    plt.close("all")

    # plot the "best return" vs the return of the equally distributed portfolio
    plt.plot(range(year_start, year_end), monthly_return_year.std(axis = 0), label="Best sparse model")
    plt.plot(range(year_start, year_end), monthly_return_equal_year.std(axis = 0), label = "Equally distributed")
    #print (monthly_return_year.std(axis = 0) - monthly_return_equal_year.std(axis = 0))
    plt.legend()
    plt.ylabel('Std of monthly return')
    plt.xlabel('Year')
    plt.xlim((1991, 2015))
    plt.xticks([1991, 1995, 2000, 2005, 2010, 2015])
    plt.ylim((0, 0.09))
    plt.savefig('mean_variance_monthly_std.jpg', dpi=600)
    plt.show()
    plt.close("all")
    
    # plot the "best return" vs the return of the equally distributed portfolio
    plt.bar(range(year_start, year_end), num_assets, label="Best sparse model")
    plt.legend()
    plt.ylabel('Number of assets')
    plt.xlabel('Year')
    plt.xlim((1991, 2015))
    plt.xticks([1991, 1995, 2000, 2005, 2010, 2015])
    plt.savefig('mean_variance_monthly_num_asset.jpg', dpi=600)
    plt.show()
    plt.close("all")

   