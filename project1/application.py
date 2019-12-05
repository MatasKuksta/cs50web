import csv
import os
import urllib.request
import requests
import goodreads
import psycopg2
import json
res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "JHDKyR1QW0crrofMApghQ", "isbns": "9781632168146"})
print(res.json())

from flask import Flask, session, render_template, request, flash, redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from functools import wraps

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "GET":
        return render_template('login.html')
    else:
        username=request.form.get("loginusername")
        password=request.form.get("loginpassword")
        rows=engine.execute(f"SELECT * FROM users WHERE username='{username}' AND password='{password}'")
        result=rows.fetchall()
        if len(result):
            session["user_id"] = result[0][0]
            return redirect('/search')
        else:
            return render_template('login.html')


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username=request.form.get("registerusername")
        password=request.form.get("registerpassword")
        usercheck = engine.execute(f"SELECT * FROM users WHERE username='{username}'")
        result=usercheck.fetchall()
        print(result)
        if not result:
            engine.execute(f"INSERT INTO users (username, password) VALUES('{username}', '{password}')")
            return redirect("/login")
        else:
            return render_template('register.html')
    else:
        return render_template('register.html')


@app.route("/search", methods=["GET", "POST"])
@login_required
def search():
    if request.method == "GET":
        return render_template('search.html')
    else:
        book=request.form.get("searchtxt")
        books=engine.execute(f"SELECT * FROM books WHERE isbn LIKE '%%{book}%%' OR title LIKE '%%{book}%%' OR author LIKE '%%{book}%%' ")
        result=books.fetchall()
        return render_template('sample.html', bookss=result)


@app.route("/book", methods=["GET", "POST"])
@login_required
def book():
    if request.method == "GET":
        return render_template("search.html")
    else:
        userch = False
        info = request.form.get("result")
        bookse=engine.execute(f"SELECT * FROM books WHERE isbn='{info}' ")
        result1=bookse.fetchall()
        reviewss=engine.execute(f"SELECT * FROM review WHERE isbn='{info}'")
        reviewss=reviewss.fetchall()
        goodreads = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "JHDKyR1QW0crrofMApghQ", "isbns": f"{info}"})
        goodreadsjson = goodreads.json()
        ratingamount = goodreadsjson["books"][0]["ratings_count"]
        average = goodreadsjson["books"][0]["average_rating"]
        if reviewss != []:
            i=0
            for dict in reviewss:
                if session["user_id"] == int(dict[4]):
                    userch = True
                i+=1
        return render_template("names.html", book=result1, otherrev=reviewss, userid=userch, average=average, ratingamount=ratingamount)


@app.route("/review", methods=["GET", "POST"])
@login_required
def review():
    if request.method == "GET":
        return render_template("search.html")
    else:
        user=session["user_id"]
        isbn=request.form.get("isbn")
        review=request.form.get("reviewtext")
        rating=request.form.get("reviewnumber")
        engine.execute(f"INSERT INTO review (isbn, review, rating, user_id) VALUES('{isbn}', '{review}', '{rating}', '{user}')")
        return render_template("search.html")


@app.route("/api/<isbn>", methods=["GET"])
def api(isbn):
    goodreads = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "JHDKyR1QW0crrofMApghQ", "isbns": f"{isbn}"})
    book = engine.execute(f"SELECT * FROM books WHERE isbn ='{isbn}'")
    book = book.fetchall()
    goodreads = goodreads.json()
    jsondict = {"title": book[0][1],
            "author": book[0][2],
            "release_year": book[0][3],
            "isbn": book[0][0],
            "review_count": goodreads["books"][0]["ratings_count"],
            "average_score": goodreads["books"][0]["average_rating"]}
    return json.dumps(jsondict)
