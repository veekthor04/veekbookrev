import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():
     users_table= db.execute("CREATE TABLE Users (id SERIAL PRIMARY KEY,username VARCHAR UNIQUE NOT NULL,email VARCHAR UNIQUE NOT NULL,password VARCHAR NOT NULL)")
     db.commit()

if __name__ == "__main__":
    main()
