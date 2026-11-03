# Python Web App with Django - Market Data Dashboard App

by Sofia (https://youtu.be/nsK15UgfhmM)

The project is for CS50WEB final project, a Django-based web application for tracking market data among different asset classes, incluing but not limited to stocks/indices/futures/commodities/cryptocurrency. The project is useful for user who would like an organizaed plotting dashboard of an asset price trend, or a table of the asset's up-to-date performance. The app also allows a refresh for fetch up-to-date data and enable to download a local copy in client's own desktop.


## Distinctiveness and Complexity

This application delivers rich interactive visualizations powered by `Plotly.js` for charting, with financial data sourced from Yahoo Finance through the Python `yfiannce` package.

**Disclaimer**: For production or commercial deployment, it's strongly recommended to use professional market data vendors such as **Finnhub**, **Refinitive**, or **QUODD**. The `yfinance` package acts as an unofficial scraper for Yahoo Finance, which introduces potential latency in real-time price delivery, which is a critical concern in real trading environments where low-latency data is essential.

#### 1. Data Acquisiton:


This application leverages both WebSocket and REST APIs from `yfiannce`. The WebSocket can be implemented as either an asynchronous or synchronous instance, and I have chosen the synchronous, or blocking WebSocket for this project. The reason for this choice is that the project scope only requires live stream subscriptions for a limited list of tickers, so a single long-running blocking connection on one thread is sufficient. This approach also keeps the callback design straightforward, as there is no need for async handling or complex concurrency management. An async websocket connection would be better suited when there is a larger data scale that genuinely requires more connections. In such cases, a trade-off between increasing threads and memory management would need to be considered.

For the REST API, standard HTTP methods such as GET, POST, PUT, and DELETE are used to interact with the server. In this project, I primarily use GET requests to fetch ticker information from `yfinance`, specifically the `fast_info` and `info` attributes of the `yfinance` Ticker object.


#### 2. Data Storage Strategy

Rather than persisting all fetched data to a database, the project employs Django's **LocMemCache**  (local memory cache) to store frequently accessed REST API responses. This approach enables faster retrieval, as subsequent requests for the same data are served directly from the current process memory.

For real production environments, using REST API without cache or database storage would easily hit the rate limits set by the API provider, or increase the costs of frequent API calls. However, it's important to note that when the `runserver` restarts, the current process ends, and the cache is cleared from memory. This means all cached data will be lost and will need to be re-fetched on the next run, after which the updated data will be cached in the new process.


#### 3. Frontend Interaction (AJAX)

The frontend uses JavaScript AJAX with GET requests to dynamically render HTML pages. This provides the flexibility to refresh the content of the current page without a full page reload from the server, and it can do so in response to specific events. For example, when the user clicks the refresh button, it triggers a re-fetch of the metric information, and when the DOM tree is loaded, the page automatically subscribes to the ticker to render its live streaming prices.

To signal that the GET request actually comes from JavaScript rather than normal brower navigation, I have usd query parameters to differentiate between the two in the views functions. Additionally, I passed the ticker symbol through query parameter to fetch the updated information for the specific ticker the user's choosen.


#### 4. Optimization Settings

When running Django's development server (runserver), the framework spawns two proceses: the main process, which handles actual requests, and the reloader process, which watches for code changes and auto-restarts the server. Both processess execute the `ready()` method defined in `apps.py`, which means the WebSocket subscription logic would run twice - once in each process. This duplication wastes memory and resources, and could lead to duplicate data streams or connection conflicts. To prevent this, the application explicitly checks for the reloader process and skips the subscription logic by verifying the environment variable `RUN_MAIN`, which is only set in the main process. This check is implemented with the code: `if os.environ.get("RUN_MAIN") != "true"`


#### 5. Snapshot Export

Users can save the current chart or snapshot to their local desktop using the html2canvas JavaScript library, which captures the rendered DOM as an image.

#### 6. Mobile Responseive

The app is built with mobile responsiveness in mind, using `<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">` in the layout, it will respond to different viewport sizes on mobile or laptop.


## Project Structure

The tree structure below demonstrates the file organization of this Django web application. The app is named `trading` and contains three main API routings - analysis, info, and dashboard - in addition to the standard login, logout, and register URL patterns. Each URL routing has its corresponding views function that renders the appropriate HTML page as well as css sylesheet for the design.

The project also includes a `live_stream.py` file, which defines the callback function for the WebSocket subscription and is executed when the server starts.

The helper file - `market.py` is assists the views functions by serializing the yfinance download dataframe and setting a cache key for caching storage.


```text
trading_project/
├── capstone
│   ├── asgi.py
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── db.sqlite3
├── manage.py
├── README.md
├── requirements.txt
└── trading
    ├── admin.py
    ├── apps.py
    ├── __init__.py
    ├── live_stream.py
    ├── market.py
    ├── migrations
    │   ├── 0001_initial.py
    │   ├── 0002_tickermeta_risk_earning_dividend_analystrating_and_more.py
    │   ├── 0003_rename_earnings_growth_earning_earning_growth_and_more.py
    │   └── __init__.py
    ├── models.py
    ├── static
    │   └── trading
    │       ├── analysis.css
    │       ├── chart.js
    │       ├── dashboard.css
    │       ├── dashboard.js
    │       └── info.css
    ├── templates
    │   └── trading
    │       ├── analysis.html
    │       ├── dashboard.html
    │       ├── index.html
    │       ├── layout.html
    │       ├── login.html
    │       └── register.html
    ├── tests.py
    ├── urls.py
    └── views.py
```

## Features

- User authentication and role-based access
- Asset live price tracking
- Trading dashboard with summary metrics
- Market data integration (API-based)
- Responsive UI for desktop and mobile use
- Database-backed persistence with Django ORM

## Tech Stack

- Python
- Django
- SQLite Database & Cache
- HTML / CSS / JavaScript
- Bootstrap CSS Library
- Requests / API integration
- WebSocket API & REST API via yfinance
- JavaScript AJAX


## Overview

The app includes three main HTML pages, each have different views:

#### Dashboard Page

The idea was initiated by the [SeekingAlpha](https://seekingalpha.com/) homepage design, which is a dashboard for a broad range of indices, futures, commodities across the US and the world, to present their live price changes by categories of US; World; Future; Commodity and Treasury.

The page is not restricted by user authentication status, meaning any user without a registered account or login can also view the price dashboard.

Each asset is clickable to view its price chart. The dashboard uses the yfinance WebSocket API to establish a long-lived connection that continuously feeds new prices, which are then cached in LocMemCache for later polling needs. My `dashboard.js` then sets up polling with a `setInterval` of 5 seconds. The reason I haven't built an in-app WebSocket server to auto-push the new feed data to the frontend, rather than just acting as a yfinance WebSocket API client, is due to the implementation difficulty. A Django server would further involve Django Channels, an ASGI server, Consumers, and additional settings.


It's important to note that the yfinance WebSocket API returns data fields including `id`, `price`, `time`, `currency`, `exchange`, `day_high`, `day_low`, `change`, `change_percent`, and more. In my dashboard, I only cached the `price`, `change`, and `change_percent` data from this live stream feed. Since yfinance provides the current price, the change is calculated as the current price against either the previous market close (if the market is close) or the current market open price (if the market is open), rather than being calculated from tick-by-tick price changes every second. When the market is open, it will be a dynamic change of prices render in red color for a price drop and green color for a price up, if the market is close, it will be static data which fetched from yfianne REST API using `fast_info` method for the `Ticker` object.

The below is a demo play of Dashboard Page


#### Info Page

The info page (or the index page) consists mainly of three sections: the live price section, the plotting section, and the information metric section.

The **live price section** operates on a similar mechanism to the dashboard page, which involves polling with a  `setInterval` of 5 seconds to request a refreshed price from the cache. This refreshed price is the continuously feed data from the yfinance WebSocket API. The change displayed shows the price change of the current price against the market open price, which will dynamically move up and down while the market is open. Unlike the dashboard, when the market is closed, the live price section for a single asset will show nothing, leaving it is an empty space.

The **chart section** is built with the data sent by the server's `info` views function, which is denoted as the `OHLC` data - respectivaly open, high, low, and close data. Each dimension is downloaded with `yfinance.download` for the past `MAX` period (rules defined in the `market.py` file, which will be discussed later)

Code denoted as below:

```
OHLC = yf.download(
    tickers,
    # default is "MAX" period, Yahoo Finance don't have MAX for indices, so indices will use 10 years
    # to call the history price for indices, e.g. extract_price(world_watchlist, period="10y")
    period = period,
    interval = "1d",
    auto_adjust = False,
    multi_level_index = True,
    progress = False)
```
Similar to the chart section, the **information metric** section is also built with data sent by the server, but it takes the data from the `yfinance fast_info` module, which contains a short list of data mainly surrounding the ticker's price dimensions, which is less time consumed than calling `yfiannce info` module. Users are allowed to press the refresh button to make a real API call towards yfinance to fetch the newest data and re-render the metric table with the new data without page reload.

The below is a demo play of Info Page

#### Analysis Page

The analysis page uses the data returned by the `analysis` views function, which sends a GET request to the yfinance API to query the `info` of a ticker. It returns tabular metric information including a ticker's valuation, risk, earnings, dividend, and analyst ratings metrics. The page also allows users to save a local copy of the populated table dashboard.

The below is a demo play of Analysis Page


## Architecture

In the below sections, will talk about on models, live_stream implementation, market data serialization, JS frontend design logic, and etc.

#### Models

Django's built-in models help with persistent data storage. In this Dashboard app, I have stored a ticker's `info` data in Django's built-in Sqlite3 database, as this data is considered less likely to change. In total, there are 6 models: TickerMeta, Valuation, Dividend, Risk, Earnings, and AnalystRating. All of these models have a one-to-one relationship based on the ticker's unique identifier. The code denotes the 1-1 relationship as `ticker = models.OneToOneField(TickerMeta, on_delete=models.CASCADE, related_name="analyst_rating")`

The six models are mainly used to render the `analysis` page, which renders the page according to different aspects. For example, a ticker's Meta information includes the ticker's short name, long name, exchange, currency, quote type, and time. A ticker's valuation information includes market cap, trailing PE, forward PE, price-to-book ratio, and enterprise value, in a one-to-one relationship with the Ticker's Meta table. Dividend information includes dividend rate, yield, ex-dividend date, dividend date, and payout ratio. Risk information includes beta and short ratio. Earnings information includes earnings timestamp, earnings quarterly growth, earnings growth, revenue growth, trailing EPS, and forward EPS. Analyst rating information includes target high price, target low price, recommendation mean, and average analyst rating.

One thing to note here is that datetime data, such as the ex-dividend date, dividend date, and earnings timestamp, extracted from yfinance, is returned as a `UNIX Timestamp`, which needs to be converted to a python `Datetime` object in order to update or store in the database. The code is as belows:

```
def timestamp (ex_div):
    if isinstance(ex_div, (int, float)):
        ex_div = datetime.datetime.fromtimestamp(ex_div)
    else:
        ex_div = None
    return ex_div
```

In `models.py`, I serialize each model instance into a python dict when retrieving records from the database. This dict is sent to the frontend for rendering. While HTML could work directly with model instances, I chose to define a `serialize` function for each model for clearner look. Since I didn't use JavaScript to fetch data, serialization is optional but keeps code consistent. Datetime fields are converted to strings using `strftime`


```
def serialize(self):
    return {
        "dividend_rate": self.dividend_rate,
        "dividend_yield": self.dividend_yield,
        "ex_dividend_date": self.ex_dividend_date.strftime("%b %d %Y, %I:%M %p") if self.ex_dividend_date else None,
        "dividend_date": self.dividend_date.strftime("%b %d %Y, %I:%M %p") if self.dividend_date else None,
        "payout_ratio": self.payout_ratio,
    }

```

#### Live Stream Websocke API

In the `live_stream.py` file, I have defined a callback function that the listener will call each time to save the live stream data in cache for 5 seconds using a cache key. The in my dashboard and info views function will polling for these live stream data every 5 seconds.

I have also included an `add_ticker` function that allows a new ticker to be added to the same subscription. This effect has been tested and confirmed that the yfinance subscription will addd the new ticker to the existing subscription ticker list, rather than overwrite it. Each time when user enter a ticker in the `info` page, it will call this `add_ticker` function to add it to the subscription list and listen to new price feed in, this achieves the result of a dynamic live price panel in the `info` HTML page in frontend.

The dashboard HTML page starts listening to price changes when the server starts running, according to the `run` function (this is a function to defines the start of a websocket connection ) that is automatically called when the `runserver`command is executed:

```
def run():
    # initially subscribe to all the market tickers that appear in dashboard
    ws.subscribe(['^DJI', '^GSPC', '^IXIC', 'CL=F', 'GC=F', 'BTC-USD', '^FTSE', '^GDAXI', '^FCHI', '^N225', 'BZ=F', 'NG=F', 'RB=F', 'ZC=F', 'ZS=F', 'HG=F', 'YM=F', 'ES=F', 'NQ=F', 'SI=F', '^IRX', '^FVX', '^TNX', '^TYX'])
    ws.listen(handle)
```

To further mention that a WebSocket may block a thread due to its long-lived connection, in the `apps.py` file, I have set up a new thread via `threading.Thread()` instead of occupying the `views` threads to handle the requests of this synchronous WebSocket connection. This new thread acts as the trigger function that calls the websocket `run` function to start listening for live stream data when the app starts. The code is shown below:

```
from . import live_stream
threading.Thread(
    target=live_stream.run,
    daemon=True,
    name="yf-ws-stream",
).start()
```

#### Helper File - Market.Py

`Market.py` is a helper file for the views functions. It contains watchlist dicts for indices, futures, commodities, and treasuries, each mapping tickers to full names for the dashboard to read easily.

It includes an `extract_price` function that downloads data for each watchlist from yfinance, returning a multi-index-column pandas dataframe. The first column layer contains open, close, high, low and adjusted close, earch further split by ticker. This structure requires extract transformation in views functions.

The `extract_price` function's default period is `MAX` for most assets, except indices, which lack a `MAX` period restricted by yfinance - I used 10-year data for them instead. The DataFrame is cached for 24 hours, as historical data is unlikely to change. Its main purpose is to plot the dashboard for each watchlist.

`Market.py` also defines `ticker_info` and `full_info`, which wrap yfinance's `fast_info` and `info` methods. `ticker_info` caches price data for 15 minutes to render the metric section on the info page, while `full_info` persists data to the databse for the analysis page.

Finally, a serialize function converts a single ticker's multi-index OHLC data into separate columns for plotting HIgh-Low, Close-Open, and Close-Adj Close charts.



#### Plotting with JS Plotly

`Chart.js`, located in the static folder, is responsible for plotting on the info page, while `Dashboard.js`, also located in the static folder, is responsible for plotting on the dashboard page. Both implement the Plotly JS library and are loaded statically in their corresponding HTML pages. All charts/plots use Plotly's rangeselector to allow users to navigate through 1m, 6m, YTD, 1y, and All Data ranges.

`Chart.js` and `Dashboard.js` receive data safeguarded by `JSON_SCRIPT`, which safely serializes the python dict passed by the server into a JavaScript recognizable JSON string, which is then parsed into a JSON object using `JSON.parse`. This ensures proper data handling when passing data from the backend to the frontend, the HTML code is shown below:

```
   {{US_Watchlist|json_script:"us_watchlist"}}
   {{World_Watchlist|json_script:"world_watchlist"}}
   {{Commodities_Watchlist|json_script:"commodities_watchlist"}}
   {{Future_Watchlist|json_script:"future_watchlist"}}
   {{Treasury_Watchlist|json_script:"treasury_watchlist"}}
   <div id="dashboard-chart" style = "width: 100%; height: 600px;"></div>
```

## How to Run Locally

To run the project, first install the required packages:

```
pip install -r /requirements.txt
```

To initialize the Djanho SQLlite database by running the following commands:

```
python manage.py makemigrations
python manage.py migrate
```

Finally, start a server on your local host at 127.0.0.1:8000 at the default 8000 port:

```
python manage.py runserver
```

## Restrictions and Future Improvement


The current app features are considered simple and neat. To build an real app with more features, I propose the following improvements:

1. Allow users to select 2-5 tickers and overlay their price charts on a single graph for direct visual comparison.
2. Add a correlation matrix using heatmap to show how closely the selected tickers move together over time.
3. Add a watchlist button to save all user-entered records and provide portfolio recommendations.
4. Add more features of UI design, such as add typewritter effect in the main page, or a auto pop-up login window.
5. Consider implementing a CI/CD pipeline and containerzing the app using Docker, with the goal of eventually deploying it to a cloud platform for real-world use.
