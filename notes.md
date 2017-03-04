**Thursday, 3/2**

* Ideas
  * **Dashboard:** displaying the output of various optimization scenarios with some input user control:
    * e.g., User can decide whether they want to optimize on VaR vs., Sharpe Ratio vs. Mean-Variance.
    * e.g., User can choose long-only or allowing shorts, a leverage range, or a number of securities to max out at
    * e.g., User can manually adjust weights
  * **Old vs. New:** Compare traditional portfolio optimization techniques such as Mean-Variance with technique that rely on Machine Learning
    * Could use modern machine learning techniques (E.g., CART, Random Forest, Boosted Trees, Neural Networks) to incorporate features from a variety of sources
    * Metadata from the company (e.g., P/E ratio relative to the industry), sentiment from social media, industry sector data 
* What do we want to work on next week?
  * **Matthew:** Additional sources of data. Getting up to speed on Python.
  * **Josiah:** Factor covariance modeling, data visualizations for comparing portfolios
  * **Zhenyuan:** Value-at-risk optimization
  * **All:** Any good articles on using machine learning within portfolio optimization. Continue learning about (convex) optimization. 



**Thursday, 2/9**

1. What do we want get out of this project? 
   1. Consensus: Learning about an interesting domain of portfolio theory more than doing novel research.
   2. Matthew: learning about how to pick stocks and evaluate performance
   3. Josiah: learning about what is required for starting up a Hedge Fund
   4. Zhenyuan: learning about optimization techniques
2. What questions do you have?
   1. How do we make decisions on what stock to pick? (Could start with the 48, 100 stocks used in the Sparse and Stable Portfolio paper)
   2. How do we judge how good a portfolio is? Splitting up into train/test/validation split based on the time period (how the Sparse and Stable Portfolio paper does it)
   3. Do we need to autocorrect over time? This might be a more complicated project than merely optimizing for a point in time. 
   4. What do we want our project to be? 
3. Next brief is 2/21, 4-5 slides, 10 minutes (will be graded). What do we need to show for this?
   1. Project Goal
   2. Show some experience with the data and visualizations
   3. High-level approach to three different tasks: Pick Stocks, Weight Stocks, Evaluate the Portfolio
   4. Possibly an overview of theory / techniques required for our project
   5. Don't think that we will have any results in the near-term
4. What statistical techniques do we need to possibly learn?
   1. Least Angle Regression
   2. Lasso Regression
   3. Anything else related to how to pick, weight stocks, and evaluate portfolios
5. What are the next steps?
   1. Quick meeting 10 minutes before class on Tuesday - decide project goal (All)
   2. Get the same datasets that were used in the paper (Josiah)
   3. Begin reproducing results in Stable/Sparse Portfolio construction (Josiah)
   4. Survey wide variety of optimization algorithms (Zhenyuan) 
   5. Learn about Stock Selection (Matt)
   6. Meet on Thursday from 5-6 - begin outlining the presentation then (All)