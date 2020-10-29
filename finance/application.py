import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    rows=db.execute("SELECT * FROM history WHERE username = :username ", username=session["user_name"])
    qoute={}
    for row in rows:
        if row["symbol"] in qoute.keys():
            qoute[row["symbol"]] = qoute[row["symbol"]] + row["number"]
        else:
            qoute[row["symbol"]] = row["number"]
    names=[]
    symbols=[]
    shares=[]
    price=[]
    total=[]
    rows = db.execute("SELECT * FROM users WHERE id = :user_id ", user_id=session["user_id"])
    money = rows[0]["cash"]
    """loop for every symbol in the dict """
    for x in qoute:
        data = lookup(x)
        names.append(data["name"]), symbols.append(data["symbol"]), shares.append(qoute[x]), price.append(data["price"]), total.append(data["price"]*qoute[x])
    final = round(money,2)
    for x in total:
        final= final + x
    return render_template("index.html", names=names, symbols=symbols, shares=shares, price=price, total=total, length=len(names), cash=round(money,2), final=round(final,2))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "GET":
        return render_template("buy.html")
    """Get stock quote."""
    if request.method == "POST":
        # Ensure symbol was submitted
        if not request.form.get("symbol"):
            return apology("must provide symbol", 403)
        elif not request.form.get("shares"):
            return apology("must type number of shares", 403)
        elif lookup(request.form.get("symbol")) == None:
            return apology("Company not found", 403)
        data = lookup(request.form.get("symbol"))
        rows = db.execute("SELECT * FROM users WHERE id = :user_id ", user_id=session["user_id"])
        shares = request.form.get("shares")
        cos = float(shares) * data["price"]
        money = rows[0]["cash"]
        if money >= cos:
            db.execute("UPDATE users SET cash = :ncash WHERE id = :user_id ", ncash=money-cos, user_id=session["user_id"])
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            db.execute("INSERT INTO history (username, symbol, price, number, time) VALUES (:username, :symbol, :price, :number, :time)", username=session["user_name"], price=data["price"], symbol=data["symbol"], time=timestamp, number=shares)
            return redirect("/")
        else:
            return apology("You don't have enought money")
    return apology("TODO")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    rows = db.execute("SELECT * FROM history WHERE username = :username", username=session["user_name"])
    symbol=[]
    number=[]
    price=[]
    time=[]
    for row in rows:
        symbol.append(row["symbol"]), number.append(row["number"]), price.append(row["price"]),time.append(row["time"])
    return render_template("history.html",symbols=symbol, numbers=number, prices=price, time=time, length=len(symbol))


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
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["user_name"] = rows[0]["username"]
        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
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
    if request.method == "GET":
        return render_template("quote.html")
    """Get stock quote."""
    if request.method == "POST":
        # Ensure symbol was submitted
        if not request.form.get("symbol"):
            return apology("must provide symbol", 403)
        if lookup(request.form.get("symbol")) == None:
            return apology("Company not found", 403)
        data = lookup(request.form.get("symbol"))
        return render_template("quoted.html", name=data["name"], price=data["price"], symbol=data["symbol"])
    return apology("TODO")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
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
        # Ensure repassword was submitted
        elif not request.form.get("repassword"):
            return apology("you must retype the password", 403)
        # Ensure repassword and password are the same
        elif request.form.get("repassword") != request.form.get("password") :
            return apology("password mismatch", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # Ensure username doesn't exist and password is correct
        if len(rows) != 0 :
            return apology("invalid username ", 403)
        db.execute("INSERT INTO users (username, hash) VALUES( :username, :hashpassword)", username=request.form.get("username") , hashpassword = generate_password_hash(request.form.get("password")))
        # Redirect user to login page
        return redirect("/login")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


    return apology("TODO")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    names = []
    symbols = []
    shares = []
    rows=db.execute("SELECT * FROM history WHERE username = :username ", username=session["user_name"])
    qoute={}
    for row in rows:
        if row["symbol"] in qoute.keys():
            qoute[row["symbol"]] = qoute[row["symbol"]] + row["number"]
        else:
            qoute[row["symbol"]] = row["number"]
    for x in qoute:
        data = lookup(x)
        names.append(data["name"]), symbols.append(data["symbol"]), shares.append(qoute[x])
    """Sell shares of stock"""
    if request.method == "GET":
        return render_template("sell.html", names=names, symbols=symbols, shares=shares, length=len(symbols))
    if request.method == "POST":
        # Ensure symbol was submitted
        if not request.form.get("soldshares"):
            return apology("must provide number", 403)
        # hna ya 5wl  #
        elif int(request.form.get("soldshares")) > shares[int(request.form.get("menu"))]:
            return apology("your selected value is above owned shares")
        value = int(request.form.get("menu"))
        data = lookup(symbols[value])
        rows = db.execute("SELECT * FROM users WHERE id = :user_id ", user_id=session["user_id"])
        shares = int(request.form.get("soldshares"))
        cos = float(shares) * data["price"]
        money = rows[0]["cash"]
        db.execute("UPDATE users SET cash = :ncash WHERE id = :user_id ", ncash=money+cos, user_id=session["user_id"])
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        db.execute("INSERT INTO history (username, symbol, price, number, time) VALUES (:username, :symbol, :price, :number, :time)", username=session["user_name"], price=data["price"], symbol=data["symbol"], time=timestamp, number=shares*(-1))
    return redirect("/")

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
