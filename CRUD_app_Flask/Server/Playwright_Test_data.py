# seed_data.py
from app import db, Book  # Make sure your Book model is imported correctly

# Create all tables if not already created
db.create_all()

# Check if books already exist to avoid duplicates
if Book.query.count() == 0:
    sample_books = [
        {"title": "The Great Gatsby", "publisher": "Scribner", "date": "1925-04-10", "cost": 10.99},
        {"title": "1984", "publisher": "Secker & Warburg", "date": "1949-06-08", "cost": 8.99},
        {"title": "To Kill a Mockingbird", "publisher": "J.B. Lippincott & Co.", "date": "1960-07-11", "cost": 12.5},
    ]

    for book in sample_books:
        new_book = Book(
            title=book["title"],
            publisher=book["publisher"],
            date=book["date"],
            cost=book["cost"]
        )
        db.session.add(new_book)
    db.session.commit()
    print("Sample books added to database.")
else:
    print("Books already exist in the database. Skipping seeding.")
