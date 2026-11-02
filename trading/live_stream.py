import yfinance as yf
from django.core.cache import cache

# initiate a yfinance websocket instance
# https://ranaroussi.github.io/yfinance/reference/api/yfinance.WebSocket.html#yfinance.WebSocket


# sync websocket, but will only run in backend thread will not block views thread
ws = yf.WebSocket()

def handle(msg):
    ticker = msg.get("id")
    price = msg.get("price")
    change = msg.get("change")
    change_percent = msg.get("change_percent")
    time = msg.get("time")
    #  save the information into cache for 60 secs
    if ticker and price is not None and change is not None and change_percent is not None and time:
        cache.set(f"price_{ticker}",{
            "price": price,
            "change": change,
            "change_percent": change_percent,
        },
        timeout=5)


def run():
    # initially subscribe to all the market tickers that appear in dashboard
    ws.subscribe(['^DJI', '^GSPC', '^IXIC', 'CL=F', 'GC=F', 'BTC-USD', '^FTSE', '^GDAXI', '^FCHI', '^N225', 'BZ=F', 'NG=F', 'RB=F', 'ZC=F', 'ZS=F', 'HG=F', 'YM=F', 'ES=F', 'NQ=F', 'SI=F', '^IRX', '^FVX', '^TNX', '^TYX'])
    ws.listen(handle)


# everytime calling subscribe will add the new ticker to the subscribe list, not a replacement
def add_ticker(symbol):
    ws.subscribe(symbol)

def remove_ticker(symbol):
    ws.unsubscribe(symbol)
