"""
The program aim to find the optimal weights allocation for each stock that comprise the portfolio,
such that the portfolio risk adjusted rate can be maximized, alternatively means the highest Sharpe Ratio

A list of sample stocks:  AAPL TSLA AMZN MSFT JPM JNJ WMT XOM GOOGL

"""

import numpy as np
import datetime
import yfinance as yf
import argparse
from scipy.optimize import minimize
from colorama import Fore


# assume the risk free rate is 3-Month US Treasury Bill Yield
# https://fred.stlouisfed.org/series/dgs3mo
RISK_FREE = 0.0417

# Parser for user to enter the stock lists
parser = argparse.ArgumentParser(description = "Find the Optimal Weight Allocation among stocks that can achieve the Highest Portfolio Sharpe Ratio " )
parser.add_argument('-s', '--stocks', metavar = '', nargs = '+', required = True, help = 'input all the stock you would like to include for your portfolio')


# Portfolio Optimization
def main():
    # parsing the stocks entered in CLI
    tickers = parser.parse_args()
    stocks = [stock.upper() for stock in tickers.stocks]

    # compute stocks weight by averaging
    initial_weights = np.array(np.round([1/len(stocks)] * len(stocks),5))
    print(Fore.GREEN + f"📈 Portfolio Optimization: {stocks}")
    print('=' * 35)
    print(f'Initial Weights allocated for each stock in portfolio: {initial_weights}')

    # download return data
    daily_returns = extract_price(stocks)
    print(daily_returns.head(10))

    # calculate the portfolio return
    u = portfolio_return(daily_returns, initial_weights)
    print('=' * 35)
    print(f'Annual Portfolio Return accord to initial weights: {u:.2f}')

    #calculate the portfolio volatility
    sigma = portfolio_volatility(daily_returns, initial_weights)
    print('=' * 35)
    print(f'Annual Portfolio Volatility accord to initial weights: {sigma:.2f}')

    # compute the portfolio sharpe ratio
    sharpe_ratio = (u-RISK_FREE)/sigma
    print('=' * 35)
    print(f'Portfolio Sharpe Ratio before Optimization: {sharpe_ratio:.2f}')

    # look for optimized weights allocation
    weights_optimizations(daily_returns, initial_weights)

def extract_price(stocks):
    """extract daily close price for portfolio stocks over the past 365 days/1 year"""
    end = datetime.datetime.today()
    begin = end - datetime.timedelta(days = 365)
    # if ticker not valid ticker, exit the program
    try:
        prices = yf.download(stocks, start=begin, end=end, auto_adjust = True)['Close']
        if prices.isna().all().any():
            raise ValueError
    except ValueError:
        sys.exit("Invalid Ticker")
    return prices.pct_change().dropna()

def portfolio_return(returns, weights):
    """Portfolio_return = R · w"""
    portfolio_returns = returns.dot(weights)
    return np.mean(portfolio_returns) * 252

def portfolio_volatility(returns, weights):
    """Portfolio Variance = wᵀ · Σ · w"""
    covariance_matrix = returns.cov()
    portfolio_variance = weights.dot(covariance_matrix).dot(weights)
    return np.sqrt(portfolio_variance * 252)

def weights_optimizations(returns, initial_weights):
    """Iterate through candidate weights to find the allocation that minimizes the negative sharpe ratio
    Uses SLSQP optimization with constrains:
    - all weights sum up to 1
    - no short sell, each weight between 0 and 1
    Returns:
        1D array of Optimal Weight Vector
    """
    bounds = [(0, 1) for _ in range(len(initial_weights))]
    constraints = {'type': 'eq', 'fun': lambda w: np.sum(w) - 1}
    def neg_sharpe_ratio(weights):
        u = portfolio_return(returns, weights)
        sigma = portfolio_volatility(returns, weights)
        return -(u-RISK_FREE)/sigma

    optimal_weights = minimize(neg_sharpe_ratio, initial_weights, method='SLSQP', bounds=bounds, constraints=constraints)
    print('=' * 35)
    print(f'The Optimal Weights for stock is {np.round(optimal_weights.x,5)}')
    print('=' * 35)
    print(f'After {optimal_weights.nit} numbers of iterations. The Portfolio Sharpe Ratio after Optimization increased to: {-optimal_weights.fun:.2f}')
    return optimal_weights.x

if __name__ == "__main__":
    main()

