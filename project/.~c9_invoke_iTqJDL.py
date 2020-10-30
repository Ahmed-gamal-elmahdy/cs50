import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
import random

from helpers import apology, login_required, usd

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
db = SQL("sqlite:///project.db")

@app.route("/")
@login_required
def index():
    rows = db.execute("SELECT COUNT(*) FROM books")
    for row in rows:
        num = row["COUNT(*)"]
    if num == 0:
        return apology("sorry there are no books at the moment")
    else:
        title=[]
        author=[]
        price=[]
        DoP=[]
        f1, f2, f3 = random.sample(range(1, num+1), 3)
        books = db.execute("SELECT * FROM books WHERE id = :f1 OR :f2 OR :f3 ",f1=int(f1),f2=int(f2),f3=int(f3))
        l=0
        for book in books:
            title.append(book["title"])
            author.append(book["author"])
            price.append(book["price"])
            DoP.append(book["DoP"])
            l=l+1
        return render_template("/featured.html",title=title,author=author,price=price,DoP=DoP,l=l)

@app.route("/history")
@login_required
def history():
    """Show history"""
    rows = db.execute("SELECT * FROM history WHERE userid = :userid", userid=session["user_id"])
    book=[]
    price=[]
    time=[]
    state=[]
    DoR=[]
    for row in rows:
        data = db.execute("SELECT * FROM books WHERE id = :bookid", bookid=row["bookid"])
        book.append(data[0]["title"])
        price.append(row["price"])
        time.append(row["time"])
        if row["state"] == 0:
            state.append("bought")
        elif row["state"] == 1:
            state.append("rent")
        elif row["state"] == 2:
            state.append("returned")
        DoR.append(row["DoR"])
    balance=[]
    balancetime=[]
    balancestate=[]
    rows = db.execute("SELECT * FROM balance WHERE userid = :user_id",user_id=session["user_id"])
    for row in rows:
        balance.append(row["cash"]),balancetime.append(row["time"]),balancestate.append(row["add"])
    return render_template("history.html", book=book, price=price, time=time, state=state, DoR=DoR, length=len(price), balance=balance, balancetime=balancetime, balancestate=balancestate, length2=len(balance))


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
        session["user_cash"] = rows[0]["cash"]
        session["user_state"] = rows[0]["status"]
        session["user_serial"] = rows[0]["serial"]

        #lookup the user status
        if session["user_state"] == 2:
            return apology("Your account has been suspended")

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



@app.route("/register", methods=["GET", "POST"])
def register():
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

        # Ensure password was submitted
        elif not request.form.get("Re-enter password"):
            return apology("must confirm your password", 403)

        # Ensure password was submitted
        elif request.form.get("password") != request.form.get("Re-enter password"):
            return apology("the password doesn't match", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 0:
            return apology("the user name already exists or is taken", 403)
        status = 0
           #check if the user is admin
        if request.form.get("serial"):
            if int(request.form.get("serial")) == 6969:
                status = 1
            else:
                status = 0

        serial = random.randint(1000,9999)

        db.execute("INSERT INTO users (username, hash, serial, status) VALUES( :username, :password, :serial, :status)", username=request.form.get("username"),
        password = generate_password_hash(request.form.get("password")), serial=serial, status=status)

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")

@app.route("/ban", methods=["GET", "POST"])
@login_required
def ban():
    if session["user_state"] != 1:
        return apology("Access Forbidden", 403)
    if request.method == "GET":
        return render_template("ban.html")
    else:
        if not request.form.get("username"):
           return apology("You must provide a name.",404)
        rows = db.execute("SELECT username FROM users WHERE username = :username", username=request.form.get("username"))
        if len(rows) != 1 :
            return apology("invalid username ", 403)
        else:
            for row in rows:
                user=row["username"]
            db.execute("UPDATE users SET status = 2 WHERE username = :user", user =user)
            return redirect("/")

@app.route("/addbook", methods=["GET", "POST"])
@login_required
def addBook():
    if session["user_state"] != 1:
        return apology("Access Forbidden", 403)
    """addBook"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure title was submitted
        if not request.form.get("title"):
            return apology("must provide title", 404)
        # Ensure author name was submitted
        elif not request.form.get("author"):
            return apology("must provide author", 404)
        # Ensure date of publish was submitted
        elif not request.form.get("DoP"):
            return apology("must provide date of publish", 404)
        # Ensure genre
        elif not request.form.get("genre") :
            return apology("must provide at least one genre", 404)
        elif not request.form.get("price"):
            return apology("must provide price", 404)
        db.execute("INSERT INTO books (title, DoP, author, genre,price) VALUES( :title, :DoP, :author, :genre,:price)", title=request.form.get("title"), DoP=request.form.get("DoP")
        , author=request.form.get("author"), genre=request.form.get("genre"),price=request.form.get("price"))
        return apology("Book added successfully",200)
    if request.method == "GET":
        return render_template("addbook.html")
    return apology("TODO")

@app.route("/changepassword", methods=["GET", "POST"])
@login_required
def change_password():
    if request.method == "GET":
        return render_template("changepassword.html")
    else:
        rows = db.execute("SELECT * FROM users WHERE username = :username",username=session["user_name"])
        if  not check_password_hash(rows[0]["hash"], request.form.get("Old password")):
            return apology("invalid password", 403)

        # Ensure password was submitted
        elif not request.form.get("Re-enter password"):
            return apology("must confirm your password", 403)

        # Ensure password was submitted
        elif request.form.get("password") != request.form.get("Re-enter password"):
            return apology("the password doesn't match", 403)

        db.execute("UPDATE users SET hash = :password WHERE username = :username",username = session["user_name"], password = generate_password_hash(request.form.get("password")))
        #alert
        return redirect("/")

@app.route("/balance", methods=["GET", "POST"])
@login_required
def balance():
    if request.method == "GET":
        return render_template("balance.html")
    if request.method == "POST":
        balance = request.form.get("balance")
        if not balance:
            return apology("Please enter the amount of money to add")
        db.execute("UPDATE users SET cash = cash + :balance WHERE id = :user_id", balance=balance , user_id =session["user_id"])
        time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        db.execute("INSERT INTO balance (cash, time,userid) VALUES (:cash, :time, :user_id)", user_id=session["user_id"], cash=balance, time=time)
        update_session()
        return redirect("/")

@app.route("/changename", methods=["GET", "POST"])
@login_required
def change_name():
    if request.method == "GET":
        return render_template("changename.html")
    else:
        rows = db.execute("SELECT * FROM users WHERE username = :username",username=session["user_name"])
        if  not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid password", 403)
        else:
            rows = db.execute("SELECT * FROM users WHERE username = :username",username=request.form.get("username"))
            if len(rows) != 0:
                return apology("the user name already is taken", 403)
            if not request.form.get("Re-enter username") :
                return apology("must confirm your username", 403)
            elif request.form.get("username") != request.form.get("Re-enter username"):
                return apology("the username doesn't match", 403)
            db.execute("UPDATE users SET username = :newusername WHERE id = :userid",newusername = request.form.get("username"),userid=session["user_id"])
            session["user_name"] = request.form.get("username")
            update_session()
            #alert
            return redirect("/")

@app.route("/inventory", methods=["GET", "POST"])
@login_required
def inventory():
    if request.method == "GET":
        rows = db.execute("SELECT * FROM history WHERE userid = :userid",userid=session["user_id"])
        bag={}
        for row in rows:
            if row["bookid"] in bag.keys():
                if ((bag[row["bookid"]] == 1) and (row["state"] == 2)):
                    del bag[row["bookid"]]
            else:
                bag[row["bookid"]] = row["state"]
        title=[]
        author=[]
        DoP=[]
        genre=[]
        price=[]
        cash=session["user_cash"]
        for bookid in bag:
            row = db.execute("SELECT * FROM books WHERE id = :book_id ", book_id=bookid)
            title.append(row[0]["title"])
            author.append(row[0]["author"])
            DoP.append(row[0]["DoP"])
            genre.append(row[0]["genre"])
            price.append(row[0]["price"])
        return render_template("inventory.html", title=title, author=author, DoP=DoP, genre=genre, cash=cash, price=price, length=len(title))

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "GET":
        return render_template("buy.html")
    else:
        if not request.form.get("bookname"):
            return apology("invalid book name")
        rows = db.execute("SELECT * FROM books WHERE title = :title", title=request.form.get("bookname"))
        if len(rows) == 0:
            return apology("invalid book name")
        update_session()
        result=session["user_cash"]-rows[0]["price"]
        if(result<0):
            return apology("Sorry,you don't have enough money")
        else:
            db.execute("UPDATE users SET cash = :cash WHERE username = :username",username = session["user_name"], cash = result)
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            db.execute("INSERT INTO history (userid, bookid, price, time, state) VALUES (:userid, :bookid, :price,:time, :state)", userid=session["user_id"], bookid=rows[0]["id"], price=rows[0]["price"],
            time=timestamp, state=0)
            return apology("book bought sucessfully",200)
@app.route("/search", methods=["GET", "POST"])
@login_required
def search():
    if request.method == "GET":
        return render_template("search.html",cash=session["user_cash"] )
    else:
        if not request.form.get("title"):
            return apology("you must enter something")
        else:
            searchby=request.form.get("option")
            if searchby == "Title":
                rows = db.execute("SELECT * FROM books WHERE title = :title", title=request.form.get("title"))
            elif searchby == "Author":
                rows = db.execute("SELECT * FROM books WHERE author = :author", author=request.form.get("title"))
            elif searchby == "Date of publish":
                rows = db.execute("SELECT * FROM books WHERE DoP = :dop", dop=request.form.get("title"))
            title=[]
            author=[]
            DoP=[]
            genre=[]
            price=[]
            cash=session["user_cash"]
            for row in rows:
                title.append(row["title"])
                author.append(row["author"])
                DoP.append(row["DoP"])
                genre.append(row["genre"])
                price.append(row["price"])
            return render_template("result.html",title=title, author=author, DoP=DoP, genre=genre, cash=cash, price=price, length=len(title))

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

def update_session():
    # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",username=session["user_name"])
        # Remember which user has logged in
        session["user_cash"] = rows[0]["cash"]
        session["user_state"] = rows[0]["status"]