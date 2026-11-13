import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks if purchase table exists"""

    """extracts the stock ticker, and its accumulated shares"""
    records = db.execute("""
        select
        stock_ticker,
        sum(shares) as 'number of shares',
        sum(shares*price) as 'purchase value',
        sum(shares*price)/sum(shares) as 'AVG purchase price'
        from purchases where user_id = ? group by stock_ticker having sum(shares) > 0""",
                         session["user_id"])

    """dict comprenhension to create {'a': 137.83, 'j': 142.82}"""
    current_price = {x["stock_ticker"]: lookup(x["stock_ticker"])["price"] for x in records}
    """dict comprenhension to create {'a': shares * 137.83, 'j': shares * 142.82}"""
    stock_market_value = {x["stock_ticker"]: x["number of shares"]
                          * current_price[x["stock_ticker"]] for x in records}

    """current cash balance extracted from the user table"""
    current_cash_balance = db.execute(
        "select cash from users where id = ?", session["user_id"])[0]["cash"]

    """ a scalar result, sum of total value for all shares using purchase price"""
    total_purchase_value = db.execute(
        "select sum(shares*price) as total_value from purchases where user_id = ?", session["user_id"])[0]["total_value"]
    """ When user first registred and login, query purchase table will be null"""
    total_purchase_value = total_purchase_value if total_purchase_value is not None else 0

    """ a scalar result, sum of total value for all shares using current price"""
    total_stock_value = sum(i for i in stock_market_value.values())

    total_balance = float(current_cash_balance) + float(total_stock_value)

    return render_template("purchase.html", records=records,
                           current_price=current_price,
                           stock_market_value=stock_market_value,
                           current_cash_balance=current_cash_balance,
                           total_purchase_value=total_purchase_value,
                           total_stock_value=total_stock_value,
                           total_balance=total_balance)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "GET":
        return render_template("buy.html")
    else:
        symbol = request.form.get("symbol").strip()
        shares = request.form.get("shares").strip()

    if not symbol or not lookup(symbol):
        return apology("Symbol is not Valid")
    if not shares.isdigit() or int(shares) <= 0:
        return apology("Shares cannot be fraction/negative")

    """ Look up for current stock price, and check balance"""
    current_price = lookup(symbol)["price"]
    balance = db.execute("select * from users where id = ?", session["user_id"])[0]["cash"]

    """check if enough balance to cover this purchase"""
    if current_price * int(shares) > balance:
        return apology("Purchase not completed, not enough balance")
    else:
        """ create a purchase sqlite3 table and update every successfully purchase"""
        db.execute("""
            CREATE TABLE IF NOT EXISTS purchases (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                stock_ticker VARCHAR(255) NOT NULL,
                shares INTEGER NOT NULL,
                price NUMERIC NOT NULL ,
                direction VARCHAR(255) NOT NULL,
                time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
                )
           """)

        db.execute("insert into purchases (user_id, stock_ticker, shares, price, direction) values(?,?,?,?,?)",
                   session["user_id"], symbol, int(shares), current_price, "Buy")

        """ update user table cash balance after successfully purchases"""
        db.execute("update users set cash = cash - ? where id = ? ",
                   current_price * int(shares), session["user_id"])

        flash(f"You've purchase {shares} {symbol} @ USD {usd(current_price)} Successfully")

    return redirect("/")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    transactions = db.execute("select  * from purchases where user_id =?", session["user_id"])

    return render_template("transaction.html", transactions=transactions)


"""New Feature to allow user to change password"""

@app.route("/change", methods=["GET", "POST"])
def change():
    session.clear()
    if request.method == "GET":
        return render_template("change.html")
    else:
        username = request.form.get("username")
        old = request.form.get("old_password")
        new = request.form.get("new_password")
        rows = db.execute(
            "select hash from users where username = ?",
            username)

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], old):
            return apology("Invalid Username/Password")

        db.execute(
            "update users set hash = ? where username = ?",
            generate_password_hash(new),
            username )

        flash("Password Updated Successfully")

        return render_template("login.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        """Add Features to allow change password"""

        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    if request.method == "GET":
        return render_template("quote.html")

    else:
        symbol = request.form.get("symbol")
        result = lookup(symbol)
        if result:
            return render_template("quoted.html", name=result["name"], price=result["price"], symbol=result["symbol"])
        else:
            return apology("Stock Info Not Exists")


@app.route("/register", methods=["GET", "POST"])
def register():
    """ if user click Registry in Navbar, it will run Get"""
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return apology("Username is missing/already exists")
        if not password or password != confirmation:
            return apology("Password is missing/not match")

        """generate hased password"""
        hashed = generate_password_hash(password, method='scrypt', salt_length=16)

        """ insert the registrant into database"""
        try:
            db.execute("insert into users(username, hash) values (?,?)", username, hashed)
        except ValueError:
            return apology("username already taken")

        row = db.execute("select * from users where username = ?", username)[0]["id"]

        session["user_id"] = row

        return redirect("/")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "GET":

        """pass to sell.html of which shares the user currently holds"""
        holdings = db.execute(
            "select stock_ticker, sum(shares) as inventory from purchases where user_id = ? group by stock_ticker", session["user_id"])

        return render_template("sell.html", holdings=holdings)

    else:
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        """query how many this share user currently owns, if not own any shares of the stock then return 0"""
        current_shares_balance = db.execute(
            "select sum(shares) as n from purchases where user_id =? and stock_ticker = ?", session["user_id"], symbol)[0]["n"]
        current_shares_balance = current_shares_balance if current_shares_balance is not None else 0

        if not symbol:
            return apology("Pls enter a valid stock ticker")
        elif not current_shares_balance:
            return apology(f"You don't own any number of {symbol}")
        elif not shares.isdigit() or int(shares) <= 0:
            return apology("Enter a valid number of shares")
        elif int(shares) > current_shares_balance:
            return apology("You don;t have enough shares for sell")

    """ update user table cash balance after successfully sell"""
    current_price = lookup(symbol)["price"]
    db.execute("update users set cash = cash + ? where id = ? ",
               current_price * int(shares), session["user_id"])

    """update the purchase table everytime of successfully sell"""
    db.execute("insert into purchases (user_id, stock_ticker, shares, price, direction) values(?,?,?,?,?)",
               session["user_id"], symbol, -int(shares), current_price, "Sell")

    flash(f"You've successfully sold {shares} {symbol} @ USD {usd(current_price)}")
    return redirect("/")
