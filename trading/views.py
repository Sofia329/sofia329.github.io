from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django.http import JsonResponse
import datetime
import math
from django.core.cache import cache
from .models import User, TickerMeta,Valuation, Dividend, Risk, Earning, AnalystRating

import yfinance as yf
from .market import extract_price, serialize ,ticker_info, full_info, us_watchlist, world_watchlist, commodities_watchlist, future_watchlist, treasury_watchlist
from .live_stream import add_ticker

# when the server start, it will query all the prices for the below 5 watchlists, it will save in the memory of the current process until the server restart
# cache the below data as they are history price data upto today, which won't change, so no need to repeately calling REST API to Yahoo Finance via yfiannce package
# websocket API to get the most updated data to supplement the current data, and real-time assets prices.

US_Watchlist = extract_price(us_watchlist, period="max")
World_Watchlist =  extract_price(world_watchlist, period="max")
Commodities_Watchlist = extract_price(commodities_watchlist, period="max")
Future_Watchlist = extract_price(future_watchlist, period="max")
Treasury_Watchlist = extract_price(treasury_watchlist, period="max")


TICKERS = ['^DJI', '^GSPC', '^IXIC', 'CL=F', 'GC=F', 'BTC-USD', '^FTSE', '^GDAXI', '^FCHI', '^N225', 'BZ=F', 'NG=F', 'RB=F', 'ZC=F', 'ZS=F', 'HG=F', 'YM=F', 'ES=F', 'NQ=F', 'SI=F', '^IRX', '^FVX', '^TNX', '^TYX']


for df in [US_Watchlist, World_Watchlist, Commodities_Watchlist, Future_Watchlist, Treasury_Watchlist]:
    df.index = df.index.strftime('%Y-%m-%d')

# define a function for loop through each watchlist dict, to get the live_stream data for all tickers
def live_stream(ticker):
    live_price = cache.get(f"price_{ticker}")
    if live_price:
        return{
            "price": live_price["price"],
            "change": live_price["change"],
            "change_percent": live_price["change_percent"],
        }
    return None

# convert yfinance Ticker.info returned UNIX Timestamp to Python Datetime object so be able to save into the ORM Dividend Model
def timestamp (ex_div):
    if isinstance(ex_div, (int, float)):
        ex_div = datetime.datetime.fromtimestamp(ex_div)
    else:
        ex_div = None
    return ex_div

def dashboard(request):
    if request.method == "GET":

        # if AJAX to fetch for live stream price data for the dashboad
        if "livestream" in request.GET:
            liveprice = {ticker: live_stream(ticker) for ticker in TICKERS}
            return JsonResponse({
                "liveprice": liveprice
            })

        # define a function to combine ploting data, ticker full name, live stream data packed for each ticker per each watchlist grouping
        # watchlist is a dict defined in market.py,
        def combine_data(watchlist, data):
            combine = []
            plot = data["Close"].dropna().to_dict()
            for ticker, fullname in watchlist.items():
                info = ticker_info(ticker)
                live = live_stream(ticker)
                plot_data = plot.get(ticker)
                # if live stream didn't subscribe successfully initially, then use the yfinance fast_info price
                if live is None and info:
                    current_price = info.get("lastPrice")
                    prev_close = info.get("previousClose")
                    if current_price is not None and prev_close is not None:
                        change = round(current_price-prev_close,2)
                        change_percent = (current_price-prev_close)/prev_close * 100
                        live = {"price": current_price, "change": change ,"change_percent": change_percent}
                combine.append({
                    "ticker": ticker,
                    "fullname": fullname,
                    "livestream": live,
                    "plot": plot_data
                })
            return combine

        return render(request, "trading/dashboard.html", {

            # pass for live stream price, ticker fullnane, plot data for dashboard table
            "US_Watchlist": combine_data(us_watchlist, US_Watchlist),
            "World_Watchlist": combine_data(world_watchlist, World_Watchlist),
            "Commodities_Watchlist": combine_data(commodities_watchlist, Commodities_Watchlist),
            "Future_Watchlist": combine_data(future_watchlist, Future_Watchlist),
            "Treasury_Watchlist":combine_data(treasury_watchlist, Treasury_Watchlist),
            "show_dashboard": True
        })

@login_required
def info(request):
    if request.method == "GET":

        # if AJAX fetch for a live API refreshed price data using request.GET to check the query parameter of the AJAX
        ticker = request.GET.get("ticker")
        if ticker and "livestream" not in request.GET:
            info = yf.Ticker(ticker).fast_info # this is live API fetch from yfinance using Ticker.fast_info rather than fetch from cache
            if info:
                info = {"ticker":ticker, **info}
                return JsonResponse({
                    "INFO": info
                })
            return JsonResponse({"INFO":None})

        # if AJAX fetch for a live stream price of the submitted ticker, JS will fetch every 5 secs to see the price changing effect
        if ticker and "livestream" in request.GET:
            # add the ticker to websocket subscribe to real-time price change
            add_ticker(ticker)
            return JsonResponse ({
                "liveprice": live_stream(ticker)
            })

        # rednering the page as normal page, not AJAX
        return render(request, "trading/index.html",{
            "show_chart": False
        })


    # request method is POST, render the page with plot and metrics for a single instrument
    ticker = request.POST["ticker"].strip().upper()
    # if user enter an empty ticker, then return error message
    if not ticker:
        messages.error(request, "Ticker cannot be empty")
        return render(request, "trading/index.html", {"show_chart": False})
    try:
        metrics = {"ticker": ticker, **ticker_info(ticker)}
        name = full_info(ticker)
        # extract_price will take a dict type watchlist, and will cache to local memory for each query
        price = extract_price({ticker: ticker}, period = "5y")
        OHLC = serialize(price, ticker)
        fullname =  name.get("longName") or name.get("shortName") if name else ticker

        if metrics is None or price is None:
            raise ValueError

        # for key, value in metrics.items():
        #     if isinstance(value, float) and math.isnan(value):
        #         metrics[key] = None

        return render(request, "trading/index.html", {
            "OHLC" : OHLC,
            "INFO": metrics,
            "fullname" : fullname,
            "LIVE" : live_stream(ticker),
            "show_chart": True
        })
    except Exception as e:
        messages.error(request, f"failed to fetch {ticker} : {e}")
        return render(request, "trading/index.html", {"show_chart": False})

@login_required
def analysis(request):
    if request.method == "GET":
        return render(request, "trading/analysis.html")

    # check if the user input a valid ticker, if missing ticker, return the render template with the warning message: Missing Ticker"
    ticker = request.POST.get("ticker").strip().upper()
    if not ticker:
        return render(request, "trading/analysis.html", {"error": "Missing Ticker"})


    # get Ticker().info from yfinance API, it will be refreshed every 24 hrs/cached for 24 hrs
    info = full_info(ticker)

    if not info:
        # if the fetch Ticker.info is none, then render ticker is delist/none, etc.
        return render(request, "trading/analysis.html", {"error": "Ticker is Wrong/Not Found"})

    # use Django get_or_create to extract the info records from Models if exist,
    # otherwise, create the info records and save into database
    # the ticker meta information is consistent so use get or create, but the valuation, risk, earning, etc use update or create to get the updated data

    tickermeta, created_tickermeta = TickerMeta.objects.update_or_create(
        ticker = ticker,
        defaults = {
            "short_name" : info.get("shortName"),
            "long_name" : info.get("longName"),
            "quote_type" : info.get("quoteType"),
            "currency" : info.get("currency"),
            "exchange" : info.get("exchange"),
        }
    )
    valuation, created_valuation = Valuation.objects.update_or_create(
        ticker = tickermeta,
        defaults = {
            "market_cap" : info.get("marketCap"),
            "trailing_pe" : info.get("trailingPE"),
            "forward_pe" : info.get("forwardPE"),
            "price_to_book" : info.get("priceToBook"),
            "enterprise_value" : info.get("enterpriseValue")
        }
    )
    dividend, created_dividend = Dividend.objects.update_or_create(
        ticker = tickermeta,
        defaults = {
            "dividend_rate" : info.get("dividendRate"),
            "dividend_yield" : info.get("dividendYield"),
            # yfiannce will return UNIX Timestamp like: 1786320000
            "ex_dividend_date" : timestamp(info.get("exDividendDate")),
            "dividend_date" : timestamp(info.get("dividendDate")),
            "payout_ratio" : info.get("payoutRatio")
        }
    )
    risk, created_risk = Risk.objects.update_or_create(
        ticker = tickermeta,
        defaults = {
            "beta" : info.get("beta"),
            "short_ratio" : info.get("shortRatio")
        }
    )
    earning, created_earning = Earning.objects.update_or_create(
        ticker = tickermeta,
        defaults = {
            "earning_timestamp" : timestamp(info.get("earningsTimestamp")),
            "earning_quarterly_growth" : info.get("earningsQuarterlyGrowth"),
            "earning_growth" : info.get("earningsGrowth"),
            "revenue_growth" : info.get("revenueGrowth"),
            "trailing_eps" : info.get("trailingEPS"),
            "forward_eps" : info.get("forwardEPS")
        }
    )
    analyst_rating, created_analyst_rating = AnalystRating.objects.update_or_create(
        ticker = tickermeta,
        defaults = { "target_high_price" : info.get("targetHighPrice"),
            "target_low_price" : info.get("targetLowPrice"),
            "recommendation_mean" : info.get("recommendationMean"),
            "average_analyst_rating" : info.get("averageAnalystRating")
            }
    )

    tickermeta = tickermeta.serialize()
    valuation = valuation.serialize()
    dividend = dividend.serialize()
    risk = risk.serialize()
    earning = earning.serialize()
    analyst_rating = analyst_rating.serialize()

    return render(request, "trading/analysis.html", {
        "tickermeta": tickermeta,
        "valuation": valuation,
        "dividend": dividend,
        "risk": risk,
        "earning": earning,
        "analystrating": analyst_rating
    })

# Create your views here.
def index(request):
    # authenticated users
    if request.user.is_authenticated:
        return render(request, "trading/index.html")
    # Everyone else is prompted to sign in
    else:
        return HttpResponseRedirect(reverse("login"))

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            messages.error(request, "Invalid Username and/or Password.")
            return render(request, "trading/login.html")
    else:
        return render(request, "trading/login.html")

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully")
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":

        # Get user registered username, email and password
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "trading/register.html", {
                "message": "Passwords must match."
            })

        # Attemp to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "trading/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "trading/register.html")
