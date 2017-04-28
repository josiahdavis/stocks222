import csv
import numpy as np
import cvxpy as cvx
import matplotlib.pyplot as plt


year_offset = 1986
year_end = 2016 
year_start = 1991

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


def calc_equal_weight(market_cap_yearly, year = 1986): 
    '''
       
    '''
    index = year - year_offset
    market_cap = market_cap_yearly[index, ]
    market_cap.shape = (market_cap.shape[0], 1)
    # print(market_cap.shape)
    x_equal = market_cap/sum(market_cap)
    return x_equal

def calc_equal_naive(): 
    '''
      
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

    

def max_utility(market_cap_yearly, ME_yearly, btm_yearly, compounded_return_yearly, monthly_return, year = 1991, gamma = 5):
    '''
       year is the last year of training, i.e. the year before running the portfolio
    '''
    N = ME_yearly.shape[1]
    index1 = year - year_offset - 4
    # 
    ME1 = ME_yearly[index1, :]
    ME1.shape = ((ME1.shape[0], 1))
    btm1 = btm_yearly[index1, :]
    btm1.shape = ((btm1.shape[0], 1))
    compounded_return1 = compounded_return_yearly[index1, :]
    compounded_return1.shape = ((compounded_return1.shape[0], 1))
    index_month_start1 = (index1 + 1) * 12
    index_month_end1 = (index1 + 2) * 12
    monthly_return_new_year1 = monthly_return[index_month_start1:index_month_end1, :]
    design_matrix1 = np.column_stack((ME1, btm1, compounded_return1))
    x_equal1 = calc_equal_weight(market_cap_yearly, year = year - 4)
    # 
    index2 = year - year_offset - 3
    ME2 = ME_yearly[index2, :]
    ME2.shape = ((ME2.shape[0], 1))
    btm2 = btm_yearly[index2, :]
    btm2.shape = ((btm1.shape[0], 1))
    compounded_return2 = compounded_return_yearly[index2, :]
    compounded_return2.shape = ((compounded_return2.shape[0], 1))
    index_month_start2 = (index2 + 1) * 12
    index_month_end2 = (index2 + 2) * 12
    monthly_return_new_year2 = monthly_return[index_month_start2:index_month_end2, :]
    design_matrix2 = np.column_stack((ME2, btm2, compounded_return2))
    x_equal2 = calc_equal_weight(market_cap_yearly, year = year - 3)
    # 
    index3 = year - year_offset - 2
    ME3 = ME_yearly[index3, :]
    ME3.shape = ((ME3.shape[0], 1))
    btm3 = btm_yearly[index3, :]
    btm3.shape = ((btm3.shape[0], 1))
    compounded_return3 = compounded_return_yearly[index3, :]
    compounded_return3.shape = ((compounded_return3.shape[0], 1))
    index_month_start3 = (index3 + 1) * 12
    index_month_end3 = (index3 + 2) * 12
    monthly_return_new_year3 = monthly_return[index_month_start3:index_month_end3, :]
    design_matrix3 = np.column_stack((ME3, btm3, compounded_return3))
    x_equal3 = calc_equal_weight(market_cap_yearly, year = year - 2)
    # 
    index4 = year - year_offset - 1
    ME4 = ME_yearly[index4, :]
    ME4.shape = ((ME4.shape[0], 1))
    btm4 = btm_yearly[index4, :]
    btm4.shape = ((btm4.shape[0], 1))
    compounded_return4 = compounded_return_yearly[index4, :]
    compounded_return4.shape = ((compounded_return4.shape[0], 1))
    index_month_start4 = (index4 + 1) * 12
    index_month_end4 = (index4 + 2) * 12
    monthly_return_new_year4 = monthly_return[index_month_start4:index_month_end4, :]
    design_matrix4 = np.column_stack((ME4, btm4, compounded_return4))
    x_equal4 = calc_equal_weight(market_cap_yearly, year = year - 1)
    # 
    index5 = year - year_offset
    ME5 = ME_yearly[index5, :]
    ME5.shape = ((ME5.shape[0], 1))
    btm5 = btm_yearly[index5, :]
    btm5.shape = ((btm5.shape[0], 1))
    compounded_return5 = compounded_return_yearly[index5, :]
    compounded_return5.shape = ((compounded_return5.shape[0], 1))
    design_matrix5 = np.column_stack((ME5, btm5, compounded_return5))
    x_equal5 = calc_equal_weight(market_cap_yearly, year = year)

    # print(design_matrix.shape)
    # print(market_cap.shape)
    # print(ME.shape)
    # print(btm.shape)
    # print(compounded_return.shape)
    # print(monthly_return_new_year.shape)
    
    one_12 = np.ones((1, 12))
    one_N = np.ones((1, N))
    # variable
    tmp_matrix1 = np.dot( np.dot(one_12 ,monthly_return_new_year1), design_matrix1)
    tmp_matrix2 = np.dot( np.dot(one_12 ,monthly_return_new_year2), design_matrix2)
    tmp_matrix3 = np.dot( np.dot(one_12 ,monthly_return_new_year3), design_matrix3)
    tmp_matrix4 = np.dot( np.dot(one_12 ,monthly_return_new_year4), design_matrix4)
    theta = cvx.Variable(3)
    # # constraints
    constraints = [ 
                     # x_equal1 + 1./N * design_matrix1 * theta <= 0.09,
                     # x_equal1 + 1./N * design_matrix1 * theta >= -0.09,
                     # x_equal2 + 1./N * design_matrix2 * theta <= 0.09,
                     # x_equal2 + 1./N * design_matrix2 * theta >= -0.09,
                     # x_equal3 + 1./N * design_matrix3 * theta <= 0.09,
                     # x_equal3 + 1./N * design_matrix3 * theta >= -0.09,
                     # x_equal4 + 1./N * design_matrix4 * theta <= 0.09,
                     # x_equal4 + 1./N * design_matrix4 * theta >= -0.09,
                     # x_equal5 + 1./N * design_matrix5 * theta <= 0.08,
                     # x_equal5 + 1./N * design_matrix5 * theta >= -0.08,
                     # theta >= -5.0,
                     # theta <= 5.0
                   ]
    # # problem
    #obj = cvx.Minimize( -tmp_matrix1 * theta -tmp_matrix2 * theta - tmp_matrix3 * theta -tmp_matrix4 * theta)
    obj = cvx.Minimize( cvx.power(1 + tmp_matrix1 * theta, 1-gamma) +cvx.power(1 + tmp_matrix2 * theta, 1-gamma) +cvx.power(1 + tmp_matrix3 * theta, 1-gamma) +cvx.power(1 + tmp_matrix4 * theta, 1-gamma) )

    prob = cvx.Problem(obj, constraints)
    prob.solve() 
    # # retrieve results 
    optimal_theta = theta.value
    # ignore the x's due to round-off error
    #optimal_theta = np.around(optimal_theta, decimals = 4)
    #optimal_theta =  optimal_x/sum(optimal_theta)
    theta1 = np.zeros((3, 1))
    # cheating here, do nothing if no optimal theta is found
    theta1[0, 0] = 0.0 #
    theta1[1, 0] = 0.0 #
    theta1[2, 0] = 0.0 #
    if optimal_theta is not None:
        #print(optimal_theta.shape)
        print(optimal_theta)
        theta1 = optimal_theta
    x_optimal = x_equal5 + 1./N * np.dot(design_matrix5 , theta1)
    # doesn't allow short here
    x_optimal[x_optimal < 0] = 0
    x_optimal = x_optimal/ sum(x_optimal)
    #print(sum(x_optimal))
    return x_optimal




if __name__ == "__main__":
 
    (mymarket_cap_yearly, myME_yearly, mybtm_yearly, mycompounded_return_yearly, mymonthly_return) = load_dataset() 
    # 
    return_equal_yearly = np.zeros((12, year_end - year_start))
    return_optimal_yearly = np.zeros((12, year_end - year_start))
    return_equal_value_yearly = np.zeros((12, year_end - year_start))
    x_equal_value_yearly = np.zeros((556, year_end - year_start))
    x_equal_yearly = np.zeros((556, year_end - year_start))
    x_optimal_yearly = np.zeros((556, year_end - year_start))

    for this_year in range(year_start, year_end):
        print('current year is ' + str(this_year))
        myx_equal_value = calc_equal_weight(mymarket_cap_yearly, year = this_year - 1)
        myx_equal = calc_equal_naive()
        myx_optimal = max_utility(mymarket_cap_yearly, myME_yearly, mybtm_yearly,
     mycompounded_return_yearly, mymonthly_return, year = this_year - 1, gamma = 5)

    #print(myx_equal_value.shape)
    #print(sum(x_equal_1987))
        return_equal_value = calc_return(myx_equal_value, mymonthly_return, year = this_year)
        return_optimal = calc_return(myx_optimal, mymonthly_return, year = this_year)
        return_equal = calc_return(myx_equal, mymonthly_return, year = this_year)

        return_equal_value.shape = ((return_equal_value.shape[0], ))
        return_equal.shape = ((return_equal.shape[0], ))
        return_optimal.shape = ((return_optimal.shape[0], ))
        myx_optimal.shape = (myx_optimal.shape[0], )
        myx_equal_value.shape = (myx_equal_value.shape[0], )
        myx_equal.shape = (myx_equal.shape[0], )

        return_equal_yearly[:, this_year - year_offset - 5] = return_equal
        return_equal_value_yearly[:, this_year - year_offset - 5] = return_equal_value
        return_optimal_yearly[:, this_year - year_offset - 5] = return_optimal
        x_equal_value_yearly[:, this_year - year_offset - 5] = myx_equal_value
        x_equal_yearly[:, this_year - year_offset - 5] = myx_equal
        x_optimal_yearly[:, this_year - year_offset - 5] = myx_optimal

    np.savetxt('return_optimal_yearly.csv', return_optimal_yearly, delimiter=",")
    np.savetxt('return_equal_value_yearly.csv', return_equal_value_yearly, delimiter=",")
    np.savetxt('return_equal_yearly.csv', return_equal_yearly, delimiter=",")
    np.savetxt('x_equal_value_yearly.csv', x_equal_value_yearly, delimiter=",")
    np.savetxt('x_equal_yearly.csv', x_equal_yearly, delimiter=",")
    np.savetxt('x_optimal_yearly.csv', x_optimal_yearly, delimiter=",")

    
    #plt.plot(range(year_start, year_end), return_equal_value_yearly.mean(axis = 0), label="equal value")
    # plt.plot(range(year_start, year_end), return_optimal_yearly.mean(axis = 0), label="optimal")
    # plt.plot(range(year_start, year_end), return_equal_yearly.mean(axis = 0), label="equal")
    # plt.legend()
    # plt.ylabel('Average monthly return')
    # plt.xlabel('Year')
    # #plt.savefig('figure1.jpg', dpi = 600)
    # plt.show()
    # plt.close("all")

    # plt.plot(range(year_start, year_end), return_optimal_yearly.std(axis = 0), label="optimal")
    # plt.plot(range(year_start, year_end), return_equal_yearly.std(axis = 0), label = "equal")
    # plt.legend()
    # plt.ylabel('Std of monthly return')
    # plt.xlabel('Year')
    # #plt.savefig('best_monthly_std.jpg', dpi=600)
    # plt.show()
    # plt.close("all")


























    