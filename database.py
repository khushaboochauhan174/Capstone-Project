import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "books.db"

class BookDatabaseManager:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._create_table()

    def _create_table(self) -> None:
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                price REAL NOT NULL,
                in_stock INTEGER NOT NULL,
                rating INTEGER NOT NULL
            )
            """
        )
        self.conn.commit()

    def create_book(self, title, price, in_stock, rating):
        cursor = self.conn.execute(
            "INSERT INTO books (title, price, in_stock, rating) VALUES (?, ?, ?, ?)",
            (title, price, int(in_stock), rating),
        )
        self.conn.commit()
        return cursor.lastrowid

    def get_all_books(self):
        rows = self.conn.execute("SELECT * FROM books").fetchall()
        return [self._row_to_dict(row) for row in rows]

    def get_book_by_id(self, book_id):
        row = self.conn.execute("SELECT * FROM books WHERE id = ?", (book_id,)).fetchone()
        return self._row_to_dict(row) if row else None

    def update_book(self, book_id, **fields):
        if not fields:
            return False
        allowed = {"title", "price", "in_stock", "rating"}
        updates = {k: v for k, v in fields.items() if k in allowed}
        if not updates:
            return False
        if "in_stock" in updates:
            updates["in_stock"] = int(updates["in_stock"])
        set_clause = ", ".join(f"{col} = ?" for col in updates)
        values = list(updates.values()) + [book_id]
        cursor = self.conn.execute(f"UPDATE books SET {set_clause} WHERE id = ?", values)
        self.conn.commit()
        return cursor.rowcount > 0

    def delete_book(self, book_id):
        cursor = self.conn.execute("DELETE FROM books WHERE id = ?", (book_id,))
        self.conn.commit()
        return cursor.rowcount > 0

    def clear_all(self):
        self.conn.execute("DELETE FROM books")
        self.conn.commit()

    @staticmethod
    def _row_to_dict(row):
        return {
            "id": row["id"],
            "title": row["title"],
            "price": row["price"],
            "in_stock": bool(row["in_stock"]),
            "rating": row["rating"],
        }

    def close(self):
        self.conn.close()
