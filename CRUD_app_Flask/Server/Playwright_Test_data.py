import time
import psycopg2
from psycopg2.extras import RealDictCursor

db_config = {
    'host': 'localhost',
    'user': 'postgres',
    'password': 'password123',
    'dbname': 'flask_demo',
    'port': 5432
}

sample_books = [
    ("The Great Gatsby", "Scribner", "1925-04-10", 10.99),
    ("1984", "Secker & Warburg", "1949-06-08", 8.99),
    ("To Kill a Mockingbird", "J.B. Lippincott & Co.", "1960-07-11", 12.5)
]

# Retry until DB is ready (GitHub Actions sometimes start PostgreSQL slowly)
max_retries = 10
for attempt in range(max_retries):
    try:
        conn = psycopg2.connect(**db_config)
        break
    except Exception as e:
        print(f"Database not ready, retrying... ({attempt+1}/{max_retries})")
        time.sleep(5)
else:
    raise Exception("Database connection failed after retries")

cur = conn.cursor(cursor_factory=RealDictCursor)

# Create table if not exists
cur.execute("""
    CREATE TABLE IF NOT EXISTS book (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        publisher TEXT NOT NULL,
        date DATE NOT NULL,
        cost NUMERIC NOT NULL
    )
""")

# Insert sample books
for book in sample_books:
    cur.execute("""
        INSERT INTO book (name, publisher, date, cost)
        SELECT %s, %s, %s, %s
        WHERE NOT EXISTS (
            SELECT 1 FROM book WHERE name=%s AND publisher=%s
        )
    """, (book[0], book[1], book[2], book[3], book[0], book[1]))

conn.commit()
cur.close()
conn.close()
print("Sample books added to database successfully!")
