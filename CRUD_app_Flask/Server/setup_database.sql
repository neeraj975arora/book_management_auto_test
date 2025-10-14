-- PostgreSQL Database Setup Script for Flask CRUD App
-- Execute this script as postgres superuser

-- Create the database
CREATE DATABASE "CRUD_flask";

-- Connect to the new database
\c "CRUD_flask";

-- Create the book table with all required fields
CREATE TABLE book (
    id SERIAL PRIMARY KEY,
    publisher VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    date DATE NOT NULL,
    Cost DECIMAL(10, 2) NOT NULL
);

-- Insert sample data for testing
INSERT INTO book (publisher, name, date, Cost) VALUES
('Penguin Random House', 'Python Crash Course', '2023-01-15', 299.99),
('O''Reilly Media', 'Learning Flask', '2023-06-20', 399.50),
('Manning Publications', 'Flask Web Development', '2024-03-10', 449.00);

-- Create a user for the Flask application (optional but recommended)
-- CREATE USER flask_user WITH PASSWORD 'flask_password';
-- GRANT ALL PRIVILEGES ON DATABASE "CRUD_flask" TO flask_user;
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO flask_user;
-- GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO flask_user;

-- Display the created table structure
\d book;

-- Show sample data
SELECT * FROM book;

-- Display success message
\echo 'Database setup completed successfully!'
\echo 'Database: CRUD_flask'
\echo 'Table: book'
\echo 'Sample data inserted: 3 books'