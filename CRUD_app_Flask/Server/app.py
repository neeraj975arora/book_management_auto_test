from flask import Flask, jsonify, request
from flask_cors import CORS
from flasgger import Swagger
import psycopg2
from psycopg2 import OperationalError, IntegrityError, DataError, DatabaseError
from psycopg2.extras import RealDictCursor
from datetime import datetime

app = Flask(__name__)
CORS(app)

# --- Swagger Configuration ---
swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Book CRUD API",
        "description": "Flask REST API for managing books with PostgreSQL backend",
        "version": "1.0.0",
        "contact": {
            "name": "IBS Developer",
            "email": "developer@example.com",
        },
    },
    "basePath": "/",
}
swagger = Swagger(app, template=swagger_template)

# --- Database configuration ---
db_config = {
    'host': 'localhost',
    'port': 5433,               
    'user': 'postgres',
    'password': 'root@root123',
    'dbname': 'CRUD_flask'
}

# --- Utility: Database connection ---
def get_db_connection():
    try:
        connection = psycopg2.connect(**db_config)
        return connection
    except OperationalError as e:
        raise OperationalError(f"Database connection failed: {str(e)}")

# --- Global Error Handlers ---
@app.errorhandler(400)
def bad_request_error(e):
    return jsonify({"error": "Bad Request", "details": str(e)}), 400

@app.errorhandler(404)
def not_found_error(e):
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(500)
def internal_error(e):
    return jsonify({"error": "Internal Server Error", "details": str(e)}), 500

@app.errorhandler(Exception)
def generic_error(e):
    return jsonify({"error": "Unexpected Error", "details": str(e)}), 500

# --- Validation Helper ---
def validate_book_data(data):
    if not data:
        return "Missing request body"
    required_fields = ['publisher', 'name', 'date', 'Cost']
    for field in required_fields:
        if field not in data:
            return f"Missing field: {field}"
    try:
        datetime.strptime(data['date'], "%Y-%m-%d")
    except ValueError:
        return "Invalid date format. Use YYYY-MM-DD."
    try:
        float(data['Cost'])
    except (ValueError, TypeError):
        return "Invalid cost. Must be a numeric value."
    return None

# --- Routes ---
@app.route('/', methods=['GET'])
def get_books():
    """
    Get all books
    ---
    tags:
      - Books
    responses:
      200:
        description: List of all books
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              publisher:
                type: string
              name:
                type: string
              date:
                type: string
                format: date
              Cost:
                type: number
      503:
        description: Database unavailable
      500:
        description: Internal server error
    """
    try:
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT * FROM book")
        result = cursor.fetchall()
        return jsonify(result), 200
    except OperationalError:
        return jsonify({"error": "Database unavailable"}), 503
    except DatabaseError as e:
        return jsonify({"error": "Database query failed", "details": str(e)}), 500
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'connection' in locals(): connection.close()

@app.route('/create', methods=['POST'])
def create_books():
    """
    Create a new book
    ---
    tags:
      - Books
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - publisher
            - name
            - date
            - Cost
          properties:
            publisher:
              type: string
            name:
              type: string
            date:
              type: string
              format: date
              example: "2025-10-09"
            Cost:
              type: number
              example: 199.99
    responses:
      201:
        description: Book created successfully
      400:
        description: Invalid input or constraint violation
      503:
        description: Database unavailable
    """
    try:
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400
        new_book = request.get_json()
        validation_error = validate_book_data(new_book)
        if validation_error:
            return jsonify({"error": validation_error}), 400

        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO book (publisher, name, date, Cost) VALUES (%s, %s, %s, %s)",
            (new_book['publisher'], new_book['name'], new_book['date'], new_book['Cost'])
        )
        connection.commit()
        return jsonify({"message": "Book created successfully", "data": new_book}), 201
    except IntegrityError:
        return jsonify({"error": "Constraint violation (duplicate or null field)"}), 400
    except DataError:
        return jsonify({"error": "Invalid data type or value"}), 400
    except OperationalError:
        return jsonify({"error": "Database unavailable"}), 503
    except Exception as e:
        return jsonify({"error": "Internal Server Error", "details": str(e)}), 500
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'connection' in locals(): connection.close()

@app.route('/update/<int:id>', methods=['PUT'])
def update_book(id):
    """
    Update a book by ID
    ---
    tags:
      - Books
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID of the book to update
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            publisher:
              type: string
            name:
              type: string
            date:
              type: string
              format: date
            Cost:
              type: number
    responses:
      200:
        description: Book updated successfully
      400:
        description: Invalid data
      404:
        description: Book not found
      503:
        description: Database unavailable
    """
    try:
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400
        updated_book = request.get_json()
        validation_error = validate_book_data(updated_book)
        if validation_error:
            return jsonify({"error": validation_error}), 400

        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE book SET publisher=%s, name=%s, date=%s, Cost=%s WHERE id=%s",
            (updated_book['publisher'], updated_book['name'], updated_book['date'], updated_book['Cost'], id)
        )
        if cursor.rowcount == 0:
            return jsonify({"error": "Book not found"}), 404

        connection.commit()
        return jsonify({"message": "Book updated successfully", "data": updated_book}), 200
    except IntegrityError:
        return jsonify({"error": "Constraint violation"}), 400
    except OperationalError:
        return jsonify({"error": "Database unavailable"}), 503
    except Exception as e:
        return jsonify({"error": "Internal Server Error", "details": str(e)}), 500
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'connection' in locals(): connection.close()

@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_book(id):
    """
    Delete a book by ID
    ---
    tags:
      - Books
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID of the book to delete
    responses:
      200:
        description: Book deleted successfully
      404:
        description: Book not found
      503:
        description: Database unavailable
    """
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM book WHERE id=%s", (id,))
        if cursor.rowcount == 0:
            return jsonify({"error": "Book not found"}), 404
        connection.commit()
        return jsonify({"message": "Book deleted successfully"}), 200
    except OperationalError:
        return jsonify({"error": "Database unavailable"}), 503
    except Exception as e:
        return jsonify({"error": "Internal Server Error", "details": str(e)}), 500
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'connection' in locals(): connection.close()

@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check
    ---
    tags:
      - System
    responses:
      200:
        description: API is healthy and database reachable
      503:
        description: Database unreachable
    """
    try:
        conn = get_db_connection()
        conn.close()
        return jsonify({"status": "healthy"}), 200
    except OperationalError:
        return jsonify({"status": "unhealthy", "reason": "Database unreachable"}), 503

# --- App Entry Point ---
if __name__ == '__main__':
    app.run(debug=True)