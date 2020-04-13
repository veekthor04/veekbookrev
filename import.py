import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine("postgres://oimowvrjuwdsmm:8f9424064929aeb7915a201123675383fffe18c87b155bbc3c9d1af685e47eba@ec2-54-217-204-34.eu-west-1.compute.amazonaws.com:5432/d2enoi8q49q28v")
db = scoped_session(sessionmaker(bind=engine))

def main():
    f = open("books.csv")
    reader = csv.reader(f)
    next(reader)
    for isbn, title, author, year in reader:
        db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
          {"isbn": isbn, "title": title, "author": author, "year": year})
    db.commit()
    print("all books added")

if __name__ == "__main__":
    main()
