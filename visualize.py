import sys
import matplotlib.pyplot as plt
import pandas as pd

CSV_PATH = "exported_books.csv"
OUTPUT_PATH = "price_vs_rating.png"

def main():
    try:
        df = pd.read_csv(CSV_PATH)
    except FileNotFoundError:
        print(f"{CSV_PATH} not found. Run client.py first.")
        sys.exit(1)
    plt.figure(figsize=(8, 6))
    plt.scatter(df["price"], df["rating"], alpha=0.7, edgecolors="black")
    plt.title("Book Price vs Rating")
    plt.xlabel("Price (GBP)")
    plt.ylabel("Rating (1-5)")
    plt.yticks([1, 2, 3, 4, 5])
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.tight_layout()
    plt.savefig(OUTPUT_PATH)
    print(f"Saved chart to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
