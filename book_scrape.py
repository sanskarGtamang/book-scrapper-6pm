import requests
from bs4 import BeautifulSoup
import sqlite3

URL ="http://books.toscrape.com/" 

# install git
# create repository in github

# go to git bash
# git config --global user.name "sanskarGtamang"
# git config --global user.email "sanskar.211330@ncit.edu.np"

# git init
# git status => if you want to check what are the status of files
# git diff => if you want to check what are the changes
# git add .
# git commit -m "Your message"
# copy paste git code from github

# 1. git add .
# 2. git commit -m "Your message"
# 3. git push origin

# git config --global user.name "sanskarGtamang"
# git config --global user.email "sanskar.211330@ncit.edu.np"
# This is git tutorial
NO_OF_PAGES = 50

page = 1
URL = f"https://books.toscrape.com/catalogue/page-{page}.html"


def insert_book(title, currency, price):
    conn = sqlite3.connect("books.sqlite3")
    cursor = conn.cursor()
    cursor.execute(
      """
        INSERT INTO books (title, currency, price) VALUES (?, ?, ?)
    """,
      (title, currency, price)
    )
    conn.commit()
    conn.close()

def create_database():
     conn = sqlite3.connect("books.sqlite3")
     cursor = conn.cursor()
     cursor.execute(
       """
      CREATE TABLE IF NOT EXISTS books(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        currency TEXT,
        price REAL
      )
      """
     )
     conn.commit()
     conn.close()

def scrape_book(url):
  response = requests.get(url)
  print(response.status_code)
  if response.status_code != 200:
    print(f"Failed to fetch this page, status code: {response.status_code}")
    return


  response.encoding = response.apparent_encoding

  soup = BeautifulSoup(response.text,"html.parser")
  books = soup.find_all("article",class_="product_pod")
  print(books)
  for book in books:
    title = book.h3.a["title"]  # Local variable 'title' is assigned to but never used
    price_text = book.find("p", class_="price_color").text
    print(title, price_text,type(price_text))
    currency = price_text[0]
    price = price_text[1:]

    insert_book(title,currency,price)


create_database()
scrape_book(URL)

# Beautiful Soup Documentation
