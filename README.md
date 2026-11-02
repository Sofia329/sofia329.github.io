# Python Web App with Django - Market Data Dashboard App

by Sofia ()

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


#### 4. Snapshot Export

Users can save the current chart or snapshot to their local desktop using the html2canvas JavaScript library, which captures the rendered DOM as an image.


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

## Overview

The app includes three main HTML pages, each have different views:

#### Dashboard Page

The idea initiated by the [SeekingAlpha](https://seekingalpha.com/) homepage design, which is a broad dashboard to easily and readily to view major indices, futures, commodities, cryptocurrency live price change, such as Dow Jones; S&P 500, Crude Oil; Gold, US treasury bonds, etc.

This page is not restricted by user aunthenticate status, which any user without account/logged in can also view the price dashboard.

[Dashboard Demo](Dashboard.mp4)

#### Info Page

The info page consists mainly three section, the
#### Analysis Page

## Features

- User authentication and role-based access
- Portfolio and asset tracking
- Trading dashboard with summary metrics
- Market data integration (API-based or CSV-based)
- Strategy monitoring and signal generation
- Order history and transaction logging
- Responsive UI for desktop and mobile use
- Admin panel for managing application data
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

