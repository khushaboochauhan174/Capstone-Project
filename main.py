from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from database import BookDatabaseManager

app = FastAPI(title="Books API", version="1.0")
db = BookDatabaseManager()

class BookIn(BaseModel):
    title: str
    price: float = Field(gt=0)
    in_stock: bool
    rating: int = Field(ge=1, le=5)

class BookUpdate(BaseModel):
    title: str | None = None
    price: float | None = Field(default=None, gt=0)
    in_stock: bool | None = None
    rating: int | None = Field(default=None, ge=1, le=5)

class BookOut(BookIn):
    id: int

@app.get("/books", response_model=list[BookOut])
def get_books():
    return db.get_all_books()

@app.get("/books/{book_id}", response_model=BookOut)
def get_book(book_id: int):
    book = db.get_book_by_id(book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.post("/books", response_model=BookOut, status_code=201)
def create_book(book: BookIn):
    new_id = db.create_book(title=book.title, price=book.price, in_stock=book.in_stock, rating=book.rating)
    return db.get_book_by_id(new_id)

@app.put("/books/{book_id}", response_model=BookOut)
def update_book(book_id: int, book: BookUpdate):
    existing = db.get_book_by_id(book_id)
    if existing is None:
        raise HTTPException(status_code=404, detail="Book not found")
    updates = book.model_dump(exclude_unset=True)
    if updates:
        db.update_book(book_id, **updates)
    return db.get_book_by_id(book_id)

@app.delete("/books/{book_id}", status_code=204)
def delete_book(book_id: int):
    deleted = db.delete_book(book_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Book not found")
    return None
