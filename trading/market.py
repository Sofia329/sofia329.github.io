"""
The below is design as the index page without require user to login, it displays major indexes,
futures, commodities, bonds from yahoo finance.

The design of the home page is inspired by: https://seekingalpha.com/

"""
import yfinance as yf
from django.core.cache import cache


# https://finance.yahoo.com/markets/world-indices/
# https://finance.yahoo.com/markets/commodities/
us_watchlist = {
    "^DJI": "Dow Jones",
    "^GSPC": "S&P 500",
    "^IXIC": "Nasdaq",
    "CL=F": "Crude Oil",
    "GC=F": "Gold",
    "BTC-USD": "Bitcoin"
}

# https://finance.yahoo.com/markets/world-indices/
world_watchlist = {
    "^FTSE": "FTSE 100",
    "^GDAXI": "DAX",
    "^FCHI": "CAC 40",
    # "^GDOW": "Global Dow",
    "^N225": "Nikkei 225",
    # "^DJSH": "Shanghai"
}

# https://finance.yahoo.com/markets/commodities/
commodities_watchlist = {
    "BZ=F": "Brent",
    "NG=F": "Natural Gas",
    "RB=F": "Gasoline",
    "ZC=F": "Corn",
    "ZS=F": "Soybeans",
    "HG=F": "Copper"
}

# https://finance.yahoo.com/markets/commodities/
future_watchlist = {
    "YM=F": "Dow Futures",
    "ES=F": "S&P Futures",
    "NQ=F": "Nasdaq Futures",
    "GC=F": "Gold",
    "SI=F": "Silver",
    "CL=F": "Crude Oil"
}

# https://finance.yahoo.com/markets/bonds/
treasury_watchlist = {
    "^IRX": "US 3 Month",
    "^FVX": "US 5 Year",
    "^TNX": "US 10 Year",
    "^TYX": "US 30 Year",
}


def extract_price(watchlist, period="max"):

    """
    extract_price function will cache the REST API data from yahoo finance into Django Local Memory Cache
    It allows retrieve the cached data from the memeory of current process upto 1 day/24 hours,
    if re-start the Django Server/kill the current process, it will call yfinance which do a REST API call to
    yahoo finance again to gather all the watchlist data.

    watchlist is a dict, so it is an iterable pass to yf.download, yfinance will batch download
    OHLC - Open, High, Low, Close, Adj Close data in MultiIndex column as below:

    MultiIndex([
        ('Close',     'AAPL'),
        ('Adj Close', 'AAPL'),
        ('High',      'AAPL'),
        ...
        ('Close',     'MSFT'),
        ('Adj Close', 'MSFT'),
        ('High',      'MSFT'),

    ])

    the return OHLC is a pandas dataframe object

    """
    tickers = list(watchlist.keys())

    # this is refer to Generative AI for setting up cache key, the cache key will be exactly same for the same watchlist
    # e.g. output for multiple stocks:  yf_MAX_1d_AAPL-MSFT-TSLA ;
    # e.g. output for single stocks:  yf_MAX_1d_AAPL ;
    # e.g. output for indices: yf_1y_1d_^FTSE-^GDAXI;
    key = f"yf_{period}_1d_{'-'.join(sorted(set(tickers)))}"

    # retrieve data from Local Memeory Cache (LocMemCache)
    data = cache.get(key)

    if data is not None:
        return data

    # REST API to retrieve daily data for max period
    OHLC = yf.download(
        tickers,
        # default is "MAX" period, Yahoo Finance don;t have MAX for indices, so indices will use 10 years
        # when call the history price for indices, e.g. extract_price(world_watchlist, period="10y")
        period = period,
        interval = "1d",
        auto_adjust = False,
        multi_level_index = True,
        progress = False)

    # if download dataframe is empty, will not save into cache
    if OHLC.empty:
        return None

    # store cache in LocMemCache for 24 hour
    cache.set(key, OHLC, timeout = 60 * 60 * 24)
    # return a pandas dataframe object
    return OHLC


# serialization for a dataframe with a single ticker, not a list of tickers
def serialize(price, ticker):

    """
    plot time series chart using OHLC dataframe via JS plotly library
    this function is to prepare the OHLC data into JSON format.
    it returns as python dict.

    it takes two inputs, price dataframe, and a single ticker that user's input

    """

    chart_data = {
        "dates": price["Close"][ticker].index.strftime("%Y-%m-%d").tolist(),
        "high": price["High"][ticker].round(2).dropna().tolist(),
        "low" : price["Low"][ticker].round(2).dropna().tolist(),
        "open": price["Open"][ticker].round(2).dropna().tolist(),
        "close": price["Close"][ticker].round(2).dropna().tolist(),
        "adj_close": price["Adj Close"][ticker].round(2).dropna().tolist(),
        "ticker": ticker

    }

    return chart_data



def ticker_info(ticker):
    """
    this is used to return the metrics of the company price data to substitute a missing price where websocket api is unable to listen/subscribe a ticker
    this will use yfinance ticker.fast_info, which will be quicker than ticket.info, cache it for 15 minutes given the regular change of the price data
    this will apply to a single ticker only, and will return a python dict
    """
    # catch error if request API failed
    try:
        key = f"info_{ticker}"
        cache_data = cache.get(key)

        # if cached, then get info from cache
        if cache_data is not None:
            return cache_data

        data = yf.Ticker(ticker)
        info = {**data.fast_info} # using fast_info which will be quicker than info

    except Exception:
        print (f"{ticker} failed to request the ticker information")
        return None

    # cached for 15 minutes
    cache.set(key, info, timeout = 60 * 15)
    return info

def full_info(ticker):

    """
    this is used to return the full metrcis of the company performance or generation information about a company risk, dividend, earning, analyst rating, valuation, etc.
    this will use yfinance ticker._info, which will be slower each time call it, cache for 24 hrs, giving the rarely changes of these data
    thsi apply to a single ticker only, and will return an yfinance info object

    * changed to store the long-lasting full info into databased rather than cache into LocMemCache
    """
    try:
        full_info = yf.Ticker(ticker).info
    except Exception:
        print(f"{ticker}: failed to fetch full info")
        return None

    # return the yfinance info object
    return full_info
