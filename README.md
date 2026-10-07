# CS50 Python - Portfolio Optimization with SciPy

By Sofia

Video overview: (https://youtu.be/rXfWdMdffkA)


### Purpose

The program aims to find the optimal weights allocation for each stock that comprises the portfolio,
such that the portfolio risk adjusted rate can be maximized. Alternatively, the highest Sharpe Ratio.


### Target Audience

A risk-averse investor, when taking on additional risk, expects proportionally higher returns. This portfolio optimization strategy scientifically helps these risk-averse investors make rational decisions about their capital allocation - such as how much of their capital to allocate among stocks in their portofio, so that the portfolio return is maximized given any certain level of risk

### Usage & Installation 

Install the below required python third party libraries

```
pip install -r ./requirement.txt
```

The program takes compulsory command line arguments, and using python library **Argparse** to convert the user's entered stocks into a python list

To understand how to use the program, user can type `python project.py -h` in terminal, it only takes 1 additional CLI argument, which is -s or --stocks that users are required to enter the stock/stocks they have in their portfolio

**Cautious** do not use comma to separate the stocks, just separate stocks with a **whitespace**

### Scope

The Sharpe Ratio is the key metric for this program. It is defined as the excess return of the portfolio over the risk-free rate, divided by the portfolio's volatility. In other words, it measures the risk-adjusted return - the higher, the better.

#### Risk Free Factor

- assume the risk free rate is the 3-Month US Treasury Bill Yield, according to [Market Yield on U.S. Treasury Securities at 3-Month Constant Maturity, Quoted on an Investment Basis](https://fred.stlouisfed.org/series/dgs3mo), risk free rate is quoted as 4.17% in the program.

#### Extract Price Data

- the program using yahoo finance for data source to download all the adjusted close price for stocks over the past 1 year, code denoted as `datetime.timedelta(days = 365)`, it will download as a pandas dataframe, with all the stock tickers as the column names, and datatime timestamp as the row indexes.

- if a ticker is invalid, download won;t be successfully. The column name will still exist, however, all records/rows are filled with NaN, so a `try ... except ...` block implemented to catch such error. If any column have all NAN records, which is `prices.isna().all().any()` is true, the program will throw a `ValueError` and exit the program.

The function returns a 2D pandas DataFrame with the shape of (number of days, number of stocks) to the `main` function

#### Allocation Weights

The initial weights are assigned equally across all stocks, with the total sum equal to 1.

#### Porfolio Return

- Portfolio return measures the **expected annualized return** of a portoflio, calculated as the weighted average of the returns of each individual asset.

- General formula as the below for a 3-asset porfolio

- ![alt text](image-2.png)

- where:
    - R<sub>p</sub> = portfolio return
    - w<sub>i</sub> = weight of asset i
    - r<sub>i</sub> = return of asset i

- The daily portfolio return is calculated as the matrix multiplication between daily returns matrix and weight vector, and converted to annual portfolio return by multiplying 252 trading days.

 ```
 portfolio_returns = returns.dot(weights)
 ```

#### Portolio Volatiltiy

- Portfolio volatility measures the annualized standard deviation of portfolio returns, representing the risk or uncertainty of the portfolio's performance. It accounts for both the individual volatilities of each asset and the correlations between them.

- General formula as the below for a 3-asset porfolio

- ![alt text](image-3.png)

- where:
    - w<sub>i</sub> = weight of asset i
    - σ²<sub>i</sub> =variance of asset i
    - cov(i,j) = covariance between asset i and j


- The daily portfolio volatility is calculated as the matrix multiplication between transposed weight vector, covariance matrix and weight vector. To convert to annual volatility multiplied by the square root of 252 trading days

```
covariance_matrix = returns.cov()
portfolio_variance = weights.dot(covariance_matrix).dot(weights)
```
#### Optimization

The optimization is implemented using the SciPy Optimize library. Since the goal is to maximize the Sharpe Ratio, this is equivalent to minimizing the negative Sharpe Ratio.

- The `scipy.optimize.minimize` function starts with an initial weight vector and iterate through candidate weights to find the optimal allocation that minimizes the negative Sharpe Ratio upon convergence.

- Within the `weights_optimizations` function, a nested `neg_sharpe_ratio` function is defined to calculate the negative Sharpe Ratio. This function is passed to the `fun` paramter of the `scipy.optimize.minize` and called for each iteration.

- The bounds are defined as a list of tuples: `[(0, 1) for _ in range(len(initial_weights))]`, ensuring each weight is between 0 and 1.

- The constraint requires the sum of all weights equals 1: `constraints = {'type': 'eq', 'fun': lambda w: np.sum(w) - 1}`. The constraint is in dictionary format, where `"type": "eq"` means the constraints function must equal zero. The lambda function `lambda w: np.sum(w) - 1` enforces this by returning zero when the weights sum to one.

- The `method='SLSQP'` (Sequential Least Squares Programming) is ideal for this portfolio weights optimization scenario, as it supports both bounds and constraints well and converges to an optimal solutions.


### Unit Test

To test the accuracy of the computed portfolio return and volatility, a separate `test_project.py` file was manually created with a return dataframe and weight vector.

`test_portfolio_return` function and `test_portfolio_volatility` function used to test the portfolio return and portfolio volatility from the project.py file, with a tolerance of 0.0001 to account for floating point imprecision.

In addition, it also tests the weights_optimizations function to verify that the optimized weights comply with the constraints. This is done by implementing the `test_weights_sum_to_one` function and the `test_weights_between_zero_and_one` function


### Limitations

1. The program run uses a constant risk free rate of 4.17%, however, in real world, the risk free rate is varied daily.
2. The program relies on user selection of stocks, rather than provide a general stock selection recommendations
3. The program model based on no short selling allowed assumptions, so the weights is limited to min: 0 and max: 1, in real market, US short sell is allowed
4. The program is entirely relies on historical data to compute the portfolio return and volatility, it is not guaranteed the future return will be repeat, ignoring future expectations, market condition, or fundamental analysis
5. No transaction costs, tax, commission, slippage considered, etc
