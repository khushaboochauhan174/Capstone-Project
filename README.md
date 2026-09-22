# Book Data Pipeline & Analytics System

End-to-end pipeline that scrapes book data from [books.toscrape.com](https://books.toscrape.com/), stores it in SQLite, exposes it through a FastAPI REST service, and consumes it via a client that exports CSV and generates a scatter plot visualization.

## Project Structure

```
Khus_Capstone_Project/
├── venv/                  # Python virtual environment
├── scraper.py             # Scrapes the first 20 books from books.toscrape.com
├── database.py            # BookDatabaseManager — SQLite CRUD operations
├── books.db               # SQLite database (auto-created)
├── seed_db.py             # Runs scraper + database together to populate books.db
├── main.py                # FastAPI app exposing REST endpoints
├── client.py               # Fetches data from the API, exports CSV
├── exported_books.csv     # CSV export (created by client.py)
├── visualize.py           # Reads CSV, generates scatter plot
├── price_vs_rating.png    # Chart output (created by visualize.py)
└── requirements.txt       # Python dependencies
```

## Data Flow

```
scraper.py → seed_db.py → database.py → books.db
                                            ↓
                                        main.py (FastAPI)
                                            ↓
                                        client.py
                                            ↓
                                    exported_books.csv
                                            ↓
                                      visualize.py
                                            ↓
                                  price_vs_rating.png
```

## Setup

```bash
# 1. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS/Linux

# 2. Install dependencies
pip install -r requirements.txt
```

## Running the Project

### 1. Scrape and seed the database
```bash
python seed_db.py
```
Scrapes the first 20 books and inserts them into `books.db`.

### 2. Start the API server
```bash
uvicorn main:app --reload
```
Server runs at `http://127.0.0.1:8000`. Interactive docs available at `http://127.0.0.1:8000/docs`.

### 3. Run the client (in a separate terminal, with the server still running)
```bash
python client.py
```
Fetches all books from the API, prints a pandas DataFrame, and exports `exported_books.csv`.

### 4. Generate the visualization
```bash
python visualize.py
```
Reads `exported_books.csv` and saves a Price vs Rating scatter plot as `price_vs_rating.png`.

## API Endpoints

| Method | Endpoint            | Description                     |
|--------|---------------------|----------------------------------|
| GET    | `/books`            | Retrieve all books              |
| GET    | `/books/{book_id}`  | Retrieve a single book by ID    |
| POST   | `/books`            | Create a new book                |
| PUT    | `/books/{book_id}`  | Update an existing book         |
| DELETE | `/books/{book_id}`  | Delete a book by ID              |

### Example: Create a book
```json
POST /books
{
  "title": "Test Book",
  "price": 25.99,
  "in_stock": true,
  "rating": 4
}
```

## Testing CRUD via PowerShell

```powershell
# Read all books
Invoke-RestMethod -Uri "http://127.0.0.1:8000/books"

# Create a book
$body = @{ title = "Test Book"; price = 25.99; in_stock = $true; rating = 4 } | ConvertTo-Json
Invoke-RestMethod -Uri "http://127.0.0.1:8000/books" -Method Post -Body $body -ContentType "application/json"

# Update a book (replace {id})
$update = @{ price = 15.50 } | ConvertTo-Json
Invoke-RestMethod -Uri "http://127.0.0.1:8000/books/{id}" -Method Put -Body $update -ContentType "application/json"

# Delete a book (replace {id})
Invoke-RestMethod -Uri "http://127.0.0.1:8000/books/{id}" -Method Delete
```

## Fields Extracted

| Field     | Description                                    |
|-----------|--------------------------------------------------|
| title     | Full book title                                  |
| price     | Numeric float value (£ symbol stripped)         |
| in_stock  | Availability status (boolean)                    |
| rating    | Integer rating 1–5 (mapped from star-rating class) |
