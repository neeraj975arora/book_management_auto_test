# Playwright_Test_data.py
import psycopg2
from psycopg2.extras import RealDictCursor

# --- Database configuration (match your app.py) ---
db_config = {
    'host': 'localhost',      # GitHub Actions will need a service for this
    'user': 'postgres',
    'password': 'password123',
    'dbname': 'flask_demo'
}

# Sample books to insert
sample_books = [
    ("The Great Gatsby", "Scribner", "1925-04-10", 10.99),
    ("1984", "Secker & Warburg", "1949-06-08", 8.99),
    ("To Kill a Mockingbird", "J.B. Lippincott & Co.", "1960-07-11", 12.5)
]

try:
    # Connect to the database
    conn = psycopg2.connect(**db_config)
    cur = conn.cursor(cursor_factory=RealDictCursor)

    # Create table if it doesn't exist
    cur.execute("""
        CREATE TABLE IF NOT EXISTS book (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            publisher TEXT NOT NULL,
            date DATE NOT NULL,
            Cost NUMERIC NOT NULL
        )
    """)

    # Insert books if they don't already exist
    for book in sample_books:
        cur.execute("""
            INSERT INTO book (name, publisher, date, Cost)
            SELECT %s, %s, %s, %s
            WHERE NOT EXISTS (
                SELECT 1 FROM book WHERE name=%s AND publisher=%s
            )
        """, (book[0], book[1], book[2], book[3], book[0], book[1]))

    conn.commit()
    print("Sample books added to database (if not already present).")

except Exception as e:
    print(f"Error seeding database: {e}")

finally:
    if 'cur' in locals():
        cur.close()
    if 'conn' in locals():
        conn.close()
