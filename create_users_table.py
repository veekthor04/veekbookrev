import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

#engine = create_engine(os.getenv("DATABASE_URL"))
engine = create_engine("postgres://oimowvrjuwdsmm:8f9424064929aeb7915a201123675383fffe18c87b155bbc3c9d1af685e47eba@ec2-54-217-204-34.eu-west-1.compute.amazonaws.com:5432/d2enoi8q49q28v")
db = scoped_session(sessionmaker(bind=engine))

def main():
     users_table= db.execute("CREATE TABLE Users (id SERIAL PRIMARY KEY,username VARCHAR UNIQUE NOT NULL,email VARCHAR UNIQUE NOT NULL,password VARCHAR NOT NULL)")
     db.commit()

if __name__ == "__main__":
    main()
