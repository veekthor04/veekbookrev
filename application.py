import os
import requests
import  re


from flask import Flask, session, render_template, jsonify, request, redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

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
message = 'welcome'


@app.route("/", methods = ['GET', 'POST'])
def index():
    message = ''
    if 'loggedin' not in session:
        return render_template('login.html', message = 'login first')
    return render_template("index.html", username = session['username'] )

@app.route("/login", methods = ['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        #get user variables
        username = request.form['username']
        password = request.form['password']

        #check database if info exist
        user_info = db.execute('SELECT * FROM Users WHERE username = :username and password = :password', {"username": username, "password": password   }).fetchone()
        if user_info:
            #get info for current session
            session['loggedin'] = True
            session['id'] = user_info['id']
            session['username'] = user_info['username']
            session['email'] = user_info['email']
            return render_template("index.html", username = session['username'])
        else:
            message = 'Invalid username or password'
    return render_template("login.html", message = message)

@app.route("/register", methods=['GET', 'POST'])
def register():
    message = ''
    if request.method == 'POST' and request.form['username'] != '' and request.form['password'] != '' and request.form['email'] != '':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        username_db  = db.execute('SELECT * FROM Users WHERE username = :username', {"username": username}).fetchone()
        if username_db:
            message = 'username already exist!'
        # email_db = db.execute('SELECT * FROM Users WHERE email = :email', {"email": email}).fetchone()
        # elif email_db: 
        #     message = 'email already exist!'
        # elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
        #     message = 'Invalid email address!'
        # elif not re.match(r'[A-Za-z0-9]+', username):
            #     message = 'username must contain only characters and numbers!'
        else:
            db.execute('INSERT INTO Users( username,password,email) values (:username,:password,:email);' , {"username": username , "password": password, "email": email})
            db.commit()
            message = 'Registration successful'
            return render_template('login.html', message = message)
    return render_template("register.html", message = message)

@app.route("/logout")
def logout():
    #ending session
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    session.pop('password', None)
    session.pop('loggedin', None)
    return render_template('login.html', message = "logout successful")

@app.route("/search", methods = ['GET', 'POST'])
def search():
    message = ''
    if 'loggedin' not in session:
        return render_template('login.html', message = 'login first')

    if request.method == 'POST' and request.form['search_info'] != '':
        if request.form['search_by'] == 'isbn':
            isbn = (request.form['search_info'])
            books = db.execute("SELECT * FROM books WHERE isbn LIKE :isbn", {"isbn": '%' + isbn + '%'}).fetchall()
        elif request.form['search_by'] == 'title':
            title = (request.form['search_info'])
            books = db.execute("SELECT * FROM books WHERE title LIKE :title", {"title": '%' + title + '%'}).fetchall()
        else:
            author =(request.form['search_info'])
            books = db.execute("SELECT * FROM books WHERE author LIKE :author", {"author": '%' + author + '%'}).fetchall()
        return render_template('search.html', message = message, books = books)
    else:
        message = 'empty search box'
    return render_template('search.html', message = message)

@app.route("/books")
def books():
    if 'loggedin' not in session:
        return render_template('login.html', message = 'login first')
    books = db.execute("SELECT * FROM books").fetchall()
    return render_template('books.html', books = books)



@app.route("/books/<int:book_id>", methods = ['GET', 'POST'])
def book(book_id):
    message = ''
    if 'loggedin' not in session:
        return render_template('login.html', message = 'login first')
    average_rating = False
    work_ratings_count = False
    if request.method == 'POST' and request.form['review'] != '' and request.form.get("rating"):
        review = request.form['review']
        rating = request.form['rating']
        db.execute('INSERT INTO reviews( id,book_id,review,rating) values (:id,:book_id,:review,:rating);' , {"id": session['id'] , "book_id": book_id, "review": review,"rating": rating })
        db.commit()
        message = 'review submitted'
    elif request.method == 'POST':
        message = 'fill the review form properly'

    book = db.execute("SELECT * FROM books WHERE book_id = :book_id", {"book_id": book_id}).fetchone()
    if book is None:
        return render_template("search.html", message="no book found.")
    review = db.execute("SELECT * FROM reviews JOIN Users ON reviews.id = Users.id WHERE book_id = :book_id", {"book_id": book_id}).fetchall()
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={'key': 'n8mHOUl5fgaj7uEiG5A2kA', 'isbns': book.isbn})
    user_review = db.execute("SELECT * FROM reviews WHERE id = :id AND book_id = :book_id", {"id": session['id'],"book_id": book_id}).fetchone()
    if res.status_code != 200:
        message = 'unable get review info from goodreads'
    else:
        data = res.json()
        average_rating = data['books'][0]['average_rating']
        work_ratings_count = data['books'][0]['work_ratings_count']
    return render_template('book.html', book = book, review = review, message = message, id = session['id'], average_rating = average_rating, work_ratings_count = work_ratings_count, user_review =user_review )

@app.route("/api/<string:isbn>")
def api(isbn):
    #getting book info from my db
    book = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()
    if book is None:
        return jsonify({"error": "Invalid isbn"}), 404
    #getting rating and rating count from my goodreads db
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={'key': 'n8mHOUl5fgaj7uEiG5A2kA', 'isbns': book.isbn})
    if res.status_code != 200:
        average_rating = ''
        work_ratings_count = ''
    else:
        data = res.json()
        average_rating = data['books'][0]['average_rating']
        work_ratings_count = data['books'][0]['work_ratings_count']
    
    return jsonify({
            "title": book.title,
            "author": book.author,
            "year": book.year,
            "isbn": book.isbn,
            "review_count": work_ratings_count,
            "average_score": average_rating,
        })