# Python Web App with Django -- Market Data Dashboard App

by Sofia ()

The project is for CS50WEB final project, a Django-based web application for tracking market data among different asset classes, incluing but not limited to stocks/indices/futures/commodities/cryptocurrency. The project is useful for user who would like an organizaed plotting dashboard of an asset price trend, or a table of the asset's up-to-date performance. The app also allows a refresh for fetch up-to-date data and enable to download a local copy in client's own desktop.


## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Environment Variables](#environment-variables)
- [Database Setup](#database-setup)
- [Running the Project](#running-the-project)
- [Testing](#testing)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

## Distinctioveness and Complexity

This application delivers rich interactive visualizations powered by `Plotly.js` for charting, with financial data sourced from Yahoo Finance through the Python `yfiannce` package.

**Disclaimer**: For production or commercial deployment, it's strongly recommended to use professional market data vendors such as **Finnhub**, **Refinitive**, or **QUODD**. The `yfinance` package acts as an unofficial scraper for Yahoo Finance, which introduces potential latency in real-time price delivery, which is a critical concern in real trading environments where low-latency data is essential.

#### 1. Data Acquisiton:

This application leverages both WebSoket and REST APIs from `yfinance`:

- Sync WebSocket - Used for live streaming data. Given the project's scope (a single WebSocket connection), a synchronous/blocking approach is sufficient. This consumes only one thread, making the callback design straightforward without the complexity of async handling.

- REST API - Handles historical data, snapshots, and on-demand queries.

#### 2. Data Storage Strategy

Rather than persisting all fetched data to a database, the project employs **Django's LocMemCache** (local memory cache) to store frequently accesses REST API responses. This enables:

- Faster retrieval: subsequent requests for the same data are served directly from current process memory. When the runserver restarts, the cache is cleared from the process.

#### 3. Frontend Interaction (AJAX)

- The frontend uses JavaScript AJAX with GET requests to dynamically render HTML pages, such as, on refresh button click, it will triggers re-fetch metric information, and when DOM tree loaded, it will automatically subscribe to the ticker to render its live streaming prices.

#### 4. Optimization Settings

- When running Django's development server(runserver), the framework spawns two processes:
    - Main Process - handles actual requests
    - Reloader Process - watches for code changes and auto-starts the server
Both processes execute the `ready()` method defined in `apps.py`, which means the WebSocket subscription logic would run twice  - once in each process. This duplication wastes memory and resources, and could lead to duplicate data streams or connection conflicts. To prevent this, the application explicitly checks for the reloader process and skips the subscription logic by checking if the environment variable contains `RUN_MAIN` which only the main process will contains it. Code denoted as `if os.environ.get("RYB_MAIN") != "true"`

#### 4. Snapshot Export

- Users can save the current chart/snapshot to their local desktop using the htm2canvas JavaScript library, which captures the rendered DOM as an image.



## Project Structure

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


## Overview

This project provides a trading platform built with Django that can help users:

- View market data and watchlists
- Analyze asset performance
- Simulate or monitor trading strategies
- Manage account and portfolio information
- Display dashboard summaries and recent activity

It is suitable for academic projects, trading simulations, or as a foundation for a more advanced real-world trading system.

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

