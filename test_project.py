import pandas as pd
import numpy as np
from pytest import approx
from project import portfolio_return, portfolio_volatility, weights_optimizations

# the below portfolio have an approx annual portfolio return of 2.709, and annual portfolio volatility of 0.17695
WEIGHTS = np.array([0.3,0.7])
RETURNS = pd.DataFrame({
    "AMZN":[0.01, 0.02, -0.01, 0.03],
    "APLE":[0.02, -0.01, 0.01, 0.02]
})

def test_portfolio_return():
    assert portfolio_return(RETURNS, WEIGHTS) == approx(2.709, abs = 0.0001)

def test_portfolio_volatility():
    assert portfolio_volatility(RETURNS, WEIGHTS) == approx(0.17695, abs = 0.0001)

def test_weights_sum_to_one():
    weights = weights_optimizations(RETURNS, WEIGHTS)
    assert np.sum(weights) == approx(1, abs = 0.000001)

def test_weights_between_zero_and_one():
    weights =  weights_optimizations(RETURNS, WEIGHTS)
    assert (weights >=0).all() and (weights <= 1).all()


