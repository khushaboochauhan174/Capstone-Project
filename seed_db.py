from database import BookDatabaseManager
from scraper import scrape_books

def main():
    books = scrape_books(limit=20)
    print(f"Scraped {len(books)} books.")
    db = BookDatabaseManager()
    db.clear_all()
    for book in books:
        db.create_book(title=book["title"], price=book["price"], in_stock=book["in_stock"], rating=book["rating"])
    print(f"Inserted {len(books)} books into books.db.")
    db.close()

if __name__ == "__main__":
    main()
