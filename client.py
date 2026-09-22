import sys
import pandas as pd
import requests

API_URL = "http://127.0.0.1:8000/books"
OUTPUT_CSV = "exported_books.csv"

def main():
    try:
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()
    except requests.exceptions.ConnectionError:
        print("Could not reach the API. Is uvicorn main:app running?")
        sys.exit(1)
    books = response.json()
    df = pd.DataFrame(books)
    print(df)
    df.to_csv(OUTPUT_CSV, index=False)
    print(f"\nExported {len(df)} rows to {OUTPUT_CSV}")

if __name__ == "__main__":
    main()
