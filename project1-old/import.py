import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

with open('books.csv') as booksfile:
     booksreader = csv.reader(booksfile, delimiter=',')
     for row in booksreader:
        if row[0] == "isbn":
            continue
        try:
            db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
                {"isbn": row[0], "title": row[1], "author": row[2], "year": int(row[3])})
            db.commit()
        except:
            print("Already Added")