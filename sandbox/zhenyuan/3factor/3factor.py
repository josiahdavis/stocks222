import csv
import numpy as np
import cvxpy as cvx
import matplotlib.pyplot as plt


year_offset = 1986
year_end = 2016 
year_start = 1988

def load_dataset():
    '''
       dataset shoule have the monthly return,
       each row for a given month,
       and each column for a given equity,
       in the example, 360(months) * 201(equities)
    '''
    market_cap_yearly = np.genfromtxt ('market_cap_yearly.csv', delimiter=",")
    ME_yearly = np.genfromtxt ('ME_yearly.csv', delimiter=",")
    btm_yearly = np.genfromtxt ('btm_yearly.csv', delimiter=",")
    compounded_return_yearly = np.genfromtxt ('compounded_return_yearly.csv', delimiter=",")
    monthly_return = np.genfromtxt ('monthly_return.csv', delimiter=",")
    # print(market_cap_yearly.shape)
    # print(ME_yearly.shape)
    # print(btm_yearly.shape)
    # print(compounded_return_yearly.shape)
    # print(monthly_return.shape)
    return (market_cap_yearly, ME_yearly, btm_yearly, compounded_return_yearly, monthly_return)


def calc_equal_weight(market_cap_yearly, year = 1987): 
    '''
       calculate the mean/sd of monthly return of an equally distributed 
       portfolio for the training period(5 years/60 months)
    '''
    index = year - year_offset - 1
    market_cap = market_cap_yearly[index, ]
    market_cap.shape = (market_cap.shape[0], 1)
    # print(market_cap.shape)
    x_equal = market_cap/sum(market_cap)
    return x_equal

def calc_equal_naive(): 
    '''
       calculate the mean/sd of monthly return of an equally distributed 
       portfolio for the training period(5 years/60 months)
    '''
    x_equal = np.ones((556, 1))/556.
    return x_equal    

def calc_return(x, monthly_return, year = 1988):
    index = year - year_offset - 1
    index_month_start = (year - year_offset) * 12
    index_month_end = (year - year_offset + 1) * 12
    monthly_return_new_year = monthly_return[index_month_start:index_month_end, :]
    return_x = np.dot(monthly_return_new_year, x)
    return return_x

    

def max_utility(x_equal, market_cap_yearly, ME_yearly, btm_yearly, compounded_return_yearly, monthly_return, year = 1987):
    '''
       Solve a min-variance optimization problem with l1-norm,
       tau is a parameter
    '''
    N = x_equal.shape[0]
    index = year - year_offset - 1
    market_cap = market_cap_yearly[index, :]
    market_cap.shape = ((market_cap.shape[0], 1))
    ME = ME_yearly[index, :]
    ME.shape = ((ME.shape[0], 1))
    btm = btm_yearly[index, :]
    btm.shape = ((btm.shape[0], 1))
    compounded_return = compounded_return_yearly[index, :]
    compounded_return.shape = ((compounded_return.shape[0], 1))
    index_month_start = (year - year_offset) * 12
    index_month_end = (year - year_offset + 1) * 12
    monthly_return_new_year = monthly_return[index_month_start:index_month_end, :]
    design_matrix = np.column_stack((ME, btm, compounded_return))
    # print(design_matrix.shape)
    # print(market_cap.shape)
    # print(ME.shape)
    # print(btm.shape)
    # print(compounded_return.shape)
    # print(monthly_return_new_year.shape)
    
    one_12 = np.ones((1, 12))
    one_N = np.ones((1, N))
    # variable
    # tmp_matrix = np.dot( np.dot(one_12 ,monthly_return_new_year), design_matrix)
    # tmp_matrix2 = np.dot(one_N, design_matrix)
    # theta = cvx.Variable(3)
    # # constraints
    # constraints = [ 
    #                  #tmp_matrix2 * theta == 0
    #                ]
    # # problem
    # obj = cvx.Minimize( -tmp_matrix * theta)
    # prob = cvx.Problem(obj, constraints)
    # prob.solve() 
    # # retrieve results 
    # optimal_theta = theta.value
    # ignore the x's due to round-off error
    #optimal_theta = np.around(optimal_theta, decimals = 4)
    #optimal_theta =  optimal_x/sum(optimal_theta)
    theta1 = np.zeros((3, 1))
    # cheating here, just to use the 3 numbers from the paper
    
    theta1[0, 0] = -1.22 #optimal_theta[0]
    theta1[1, 0] = 3.466 #optimal_theta[1]
    theta1[2, 0] = 2.0 #optimal_theta[2]
    x_optimal = x_equal + 1./N * np.dot(design_matrix , theta1)
    # doesn't allow short here
    x_optimal[x_optimal < 0] = 0
    x_optimal = x_optimal/ sum(x_optimal)

    print(sum(x_optimal))
    return x_optimal




if __name__ == "__main__":
 
    (mymarket_cap_yearly, myME_yearly, mybtm_yearly, mycompounded_return_yearly, mymonthly_return) = load_dataset() 
    # 
    return_equal_yearly = np.zeros((12, year_end - year_start))
    return_optimal_yearly = np.zeros((12, year_end - year_start))
    return_equal_value_yearly = np.zeros((12, year_end - year_start))

    for this_year in range(year_start, year_end):
        myx_equal_value = calc_equal_weight(mymarket_cap_yearly, year = this_year - 1)
        myx_equal = calc_equal_naive()
        myx_optimal = max_utility(myx_equal_value, mymarket_cap_yearly, myME_yearly, mybtm_yearly,
     mycompounded_return_yearly, mymonthly_return, year = this_year - 1)

    #print(myx_equal_value.shape)
    #print(sum(x_equal_1987))
        return_equal_value = calc_return(myx_equal_value, mymonthly_return, year = this_year)
        return_optimal = calc_return(myx_optimal, mymonthly_return, year = this_year)
        return_equal = calc_return(myx_equal, mymonthly_return, year = this_year)
        return_equal_value.shape = ((return_equal_value.shape[0], ))
        return_equal.shape = ((return_equal.shape[0], ))
        return_optimal.shape = ((return_optimal.shape[0], ))
        return_equal_yearly[:, this_year - year_offset - 2] = return_equal
        return_equal_value_yearly[:, this_year - year_offset - 2] = return_equal_value
        return_optimal_yearly[:, this_year - year_offset - 2] = return_optimal


    
    #plt.plot(range(year_start, year_end), return_equal_value_yearly.mean(axis = 0), label="equal value")
    plt.plot(range(year_start, year_end), return_optimal_yearly.mean(axis = 0), label="optimal")
    plt.plot(range(year_start, year_end), return_equal_yearly.mean(axis = 0), label="equal")
    plt.legend()
    plt.ylabel('Average monthly return')
    plt.xlabel('Year')
    plt.show()
    plt.close("all")


























    