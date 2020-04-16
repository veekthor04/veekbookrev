# Project 1

Web Programming with Python and JavaScript

veekbookrev is a book review website, where users will be able to register for in the
website and then log in using their username and password. users are able to search
for books, leave reviews and rating for individual books, and see the reviews made by 
other people from goodreads.com
files info:

application.py: is the main app file. Contains routing to all html files , queries to
database and all other functions.

create_books_table.py: creates the books table in the database, which contains book_id,
isbn, title, author and year

create_rewiew_table.py: creates the review table in the database which contains id,
book_id, review and rating

create_users_table.py: creates the users table in the database which contains id,
username, email, and password

import.py: imports all the books in books.csv to the books table in the database

book.html:the page shows the infomation the book selected by the user, gives option for
user to enter his/her review, displays user's rating if available, display all review 
about the book and show average rating from goodreads if available

register.html: the page allows user to create an account and checks is username is not 
taken
 
layout.css: this contains the style sheet for layout.html

books.html: this shows the list of all books available in the database

index.html: this is the home page and allow user to search for books

layout.html: this contains the template for the pages

login.html: this page allows user to log in with username and password

search.html: this page allows users to search for books and displays results if available