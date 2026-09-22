import re
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://books.toscrape.com/"
RATING_WORDS = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}

def scrape_books(limit: int = 20) -> list[dict]:
    response = requests.get(BASE_URL, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    book_cards = soup.select("article.product_pod")[:limit]
    books = []
    for card in book_cards:
        title = card.h3.a["title"].strip()
        raw_price = card.select_one("p.price_color").text.strip()
        price = float(re.sub(r"[^\d.]", "", raw_price))
        availability_text = card.select_one("p.instock.availability").text.strip()
        in_stock = "In stock" in availability_text
        rating_class = card.select_one("p.star-rating")["class"]
        rating_word = next((c for c in rating_class if c in RATING_WORDS), None)
        rating = RATING_WORDS.get(rating_word, 0)
        books.append({"title": title, "price": price, "in_stock": in_stock, "rating": rating})
    return books

if __name__ == "__main__":
    for book in scrape_books():
        print(book)
