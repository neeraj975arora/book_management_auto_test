# Flask CRUD App with PostgreSQL & Swagger UI

## Description

This is a simple Flask CRUD application that manages a list of books stored in a PostgreSQL database. The app allows users to create, read, update, and delete books through a React frontend. It also provides interactive API documentation using **Swagger UI** powered by the **Flasgger** module. 


## Issues Resolved

**a) Mixed-case field names (SQLAlchemy & PostgreSQL 16.10)**
PostgreSQL requires mixed-case column names (e.g., `Cost`) to be enclosed in double quotes (`"Cost"`). SQLAlchemy ORM doesn’t auto-handle this quoting, causing query failures.
**Fix:** Renamed all mixed-case fields to lowercase (e.g., `Cost` → `cost`) for cross-platform compatibility.

---

**b) Running `setup_database.sql` on Linux**
The `postgres` Linux user (created without a home directory) can only access files in open directories.
**Fix:** Copy script to `/tmp` and set open permissions before running:

```bash
sudo cp setup_database.sql /tmp/
sudo chmod 777 /tmp/setup_database.sql
sudo -u postgres psql -f /tmp/setup_database.sql
```

---

**c) Password for `postgres` DB user**
By default, PostgreSQL installs `postgres` without a password, blocking authenticated access.
**Fix:**

```bash
sudo -u postgres psql -c "ALTER USER postgres PASSWORD '123456';"
```

Enables password-based login for SQLAlchemy and admin tools.


## Project Structure

```
CRUD_APP/
├── client/                         # React frontend
│   ├── public/
│   ├── src/
│   ├── package.json
│   └── README.md
├── server/                         # Flask + PostgreSQL backend
│   ├── app.py
│   ├── requirements.txt
│   ├── tests/
|   |--- postman_tests   
│   └── README.md
└── README.md
```

## Prerequisites

Ensure the following are installed on your system:

- **Python 3.8+**
- **PostgreSQL 12+**
- **Node.js 16+** (for React frontend)
- **pip** (Python package manager)
- **npm** (Node package manager)

## Virtual Environment Setup (Recommended)

Using a virtual environment isolates your Python dependencies and avoids conflicts with system packages. This is **highly recommended** for Python projects.

### Creating and Activating Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```


## Dependencies Overview

The `requirements.txt` file contains all necessary Python packages:

- **Flask==3.0.0** - Core web framework
- **flask-cors==4.0.0** - Cross-Origin Resource Sharing support
- **flasgger==0.9.7.1** - Swagger/OpenAPI documentation
- **psycopg2-binary==2.9.9** - PostgreSQL database adapter
- **pytest==7.4.3** - Testing framework
- **pandas==2.1.3** - Data analysis for test reports
- **Jinja2==3.1.2** - Template engine for reports

## Technologies Used

### Backend

- Flask (Backend Framework)
- Flask-CORS (Cross-Origin Resource Sharing)
- psycopg2-binary (PostgreSQL driver for Python)
- **Flasgger** (Swagger UI for API documentation)

### Frontend

- React
- Axios (for API calls)
- Bootstrap (for styling)

## Installation & Setup

### Backend Setup (Flask + PostgreSQL)

1. **Navigate to the server directory:**

   ```bash
   cd CRUD_app_Flask/server
   ```

2. **Create and activate virtual environment:**

   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Python dependencies using requirements.txt:**

   ```bash
   pip install -r requirements.txt
   ```

 3.  **Downloading PostgreSQL and setup password for PostgreSQL**
   ```bash
  apt install postgresql
  sudo -i -u postgres -psql -ALTER USER postgres WITH PASSWORD 'yourpassword'; -\q
   ```
  ** Switch to PostgreSQL user **
  ```bash
  sudo -i -u postgres -psql
  psql
    ```

   **Create a database in PostgreSQL:**

   ```sql
   CREATE DATABASE demo_flask;
   ```

   **Create the book table:**

   ```sql
   CREATE TABLE book (
       id SERIAL PRIMARY KEY,
       publisher VARCHAR(255),
       name VARCHAR(255),
       date DATE
   );
   ```

### 🧩 4. How to Initialize PostgreSQL Database

Before running the Flask backend, you need to set up your PostgreSQL database and user credentials.

#### Step 1: Copy the SQL setup file
```bash
sudo cp setup_database.sql /tmp
```

#### Step 2. Run the SQL script as the PostgreSQL user:
```bash
sudo -u postgres psql -f /tmp/setup_database.sql
```

This will create the required database and tables defined inside your setup_database.sql file.

#### Step 3. (Optional) Set a password for the PostgreSQL postgres user:
```bash
sudo -u postgres psql -c "ALTER USER postgres PASSWORD '123456';"
```

💡 Tip:
Replace '123456' with your own secure password.
You’ll need to update this password in your Flask app’s database configuration:
```bash
db_config = {
    'host': 'localhost',
    'user': 'postgres',
    'password': '123456',  # Update this if you change it
    'dbname': 'demo_flask'
}
```

#### 4. Verify the database setup:
```bash
sudo -u postgres psql
\l   # List all databases
\c demo_flask   # Connect to your app's database
\dt  # List all tables
```

If you see the book table listed, your database has been initialized successfully ✅

5. **Configure the database connection:**

   Open `app.py` and update the `db_config` object with your PostgreSQL credentials:

   ```python
   db_config = {
       'host': 'localhost',
       'user': 'your-postgres-username',  # Default is often 'postgres'
       'password': 'your-postgres-password',
       'dbname': 'demo_flask'
   }
   ```

6. **Run the Flask application:**

   ```bash
   python app.py
   ```

   The backend server will start on `http://localhost:5000`

   ### API Documentation (Swagger UI)

   - Once the server is running, open your browser and go to:
     - [http://127.0.0.1:5000/apidocs/](http://127.0.0.1:5000/apidocs/)
   - This interactive Swagger UI is auto-generated by Flasgger and lets you explore, test, and understand all API endpoints.

   **Best Practice:** Always use Swagger UI for quick API testing and documentation. Flasgger automatically generates docs from your route docstrings.

### Frontend Setup (React)

1. **Open a new terminal and navigate to the client directory:**

   ```bash
   cd client
   ```

2. **Install Node.js dependencies:**

   ```bash
   npm install
   ```
3. **Start the React development server:**

   ```bash
   npm run dev
   ```

   The frontend will start on `http://localhost:5173`

## Usage

1. **Start the backend server** (Flask app on port 5000)
2. **Start the frontend client** (React app on port 5173)
3. **Open your browser** and navigate to `http://localhost:5173` for the React UI
4. **API Documentation:** Visit [http://127.0.0.1:5000/apidocs/](http://127.0.0.1:5000/apidocs/) for interactive API docs and testing

You should see the book management interface where you can:

- View all books
- Add new books
- Edit existing books
- Delete books

## API Endpoints

The Flask backend provides the following REST API endpoints:

- `GET /` - Retrieve all books
- `POST /create` - Create a new book
- `PUT /update/<id>` - Update an existing book by ID
- `DELETE /delete/<id>` - Delete a book by ID
- `GET /health` - Health check endpoint

### Detailed API Documentation

For complete API documentation with request/response examples, visit the **Swagger UI** at:
[http://127.0.0.1:5000/apidocs/](http://127.0.0.1:5000/apidocs/) (when server is running)

## Testing

### 🎯 Unified Test Framework (Recommended)

**One-Command Testing:** Run all tests and generate unified reports:

```bash
./run_all_tests.sh
```

This master script will:
- ✅ Check server and database health
- 🧪 Run pytest unit tests (14 tests)
- 📡 Execute Newman API tests (58 assertions)  
- 📊 Generate unified HTML report combining all results
- 📈 Provide detailed coverage analysis

**Individual Test Execution:**

```bash
# Run only pytest unit tests
bash Server/run-pytest.sh

# Run only Newman API tests  
cd postman_tests && ./run_newman.sh

# Generate unified report (combines all results)
python3 app_test.py
```

**Test Reports Location:**
- **Unified Report:** `postman_tests/combined_test_report.html`
- **Coverage Analysis:** `TEST_COVERAGE_REPORT.md`
- **Newman Report:** `postman_tests/newman-report.html`
- **Pytest JSON:** `Server/tests/pytest/pytest-report.json`

### Manual API Testing with Thunder Client / Postman

You can manually test all API endpoints using **Thunder Client** (VS Code extension) or **Postman**. Make sure your Flask server is running on `http://localhost:5000` before testing.

#### 1. **Health Check**
- **Method:** `GET`
- **URL:** `http://localhost:5000/health`
- **Headers:** None required
- **Body:** None
- **Expected Response:** 
  ```json
  {
    "status": "healthy"
  }
  ```

#### 2. **Get All Books**
- **Method:** `GET`
- **URL:** `http://localhost:5000/`
- **Headers:** None required
- **Body:** None
- **Expected Response:** 
  ```json
  [
    {
      "id": 1,
      "publisher": "Penguin",
      "name": "Python Programming",
      "date": "2024-01-15",
      "cost": 299.99
    }
  ]
  ```

#### 3. **Create New Book**
- **Method:** `POST`
- **URL:** `http://localhost:5000/create`
- **Headers:** 
  ```
  Content-Type: application/json
  ```
- **Body (JSON):**
  ```json
  {
    "publisher": "O'Reilly",
    "name": "Learning Flask",
    "date": "2024-10-11",
    "cost": 399.99
  }
  ```
- **Expected Response:** 
  ```json
  {
    "message": "Book created successfully",
    "data": {
      "publisher": "O'Reilly",
      "name": "Learning Flask",
      "date": "2024-10-11",
      "cost": 399.99
    }
  }
  ```

#### 4. **Update Existing Book**
- **Method:** `PUT`
- **URL:** `http://localhost:5000/update/{id}` (replace {id} with actual book ID, e.g., `http://localhost:5000/update/1`)
- **Headers:** 
  ```
  Content-Type: application/json
  ```
- **Body (JSON):**
  ```json
  {
    "publisher": "Updated Publisher",
    "name": "Updated Book Name",
    "date": "2024-12-01",
    "cost": 499.99
  }
  ```
- **Expected Response:** 
  ```json
  {
    "message": "Book updated successfully",
    "data": {
      "publisher": "Updated Publisher",
      "name": "Updated Book Name",
      "date": "2024-12-01",
      "cost": 499.99
    }
  }
  ```

#### 5. **Delete Book**
- **Method:** `DELETE`
- **URL:** `http://localhost:5000/delete/{id}` (replace {id} with actual book ID, e.g., `http://localhost:5000/delete/1`)
- **Headers:** None required
- **Body:** None
- **Expected Response:** 
  ```json
  {
    "message": "Book deleted successfully"
  }
  ```

### Testing Workflow Recommendation

1. **Start with Health Check** - Verify server is running
2. **Get All Books** - Check current state (might be empty initially)
3. **Create a Book** - Add test data
4. **Get All Books again** - Verify the book was created
5. **Update the Book** - Modify the created book
6. **Get All Books again** - Verify the update
7. **Delete the Book** - Remove the test book
8. **Get All Books again** - Verify deletion

### Thunder Client Setup (VS Code)

1. **Install Thunder Client extension** in VS Code
2. **Create a new collection** named "Book API Tests"
3. **Add each endpoint** as described above
4. **Save the collection** for future use

### Postman Setup

1. **Import the existing collection:** Use `postman_tests/book_api_postman_collection.json`
2. **Or create manually:** Add each endpoint as described above
3. **Set environment variable:** Create `base_url = http://localhost:5000`
4. **Use {{base_url}}** in your requests for easy switching between environments

### Automated Postman Tests

The project includes Postman collection for automated API testing:

1. **Navigate to the Postman tests directory:**

   ```bash
   cd Server/postman_tests
   ```

2. **Run automated tests with Newman:**

   ```bash
   ./run_newman.sh
   ```

3. **Generate unified test report:**
   ```bash
   python3 merge_reports.py
   ```

## Troubleshooting

### Common Issues

1. **Database Connection Error:**

   - Ensure PostgreSQL is running
   - Verify database credentials in `app.py`
   - Check if the database and table exist

2. **CORS Errors:**

   - Ensure Flask-CORS is installed
   - Check that the backend is running on port 5000

3. **Frontend Can't Connect to Backend:**
   - Verify both servers are running
   - Check that the API URL in React matches the Flask server URL

## Development & Best Practices

- Backend: Flask with PostgreSQL
- Frontend: React with Bootstrap
- API Testing: Postman/Newman
- **API Documentation:** Flasgger/Swagger UI ([http://127.0.0.1:5000/apidocs/](http://127.0.0.1:5000/apidocs/))
- **Virtual Environment:** Always use a virtual environment for Python dependencies

## Troubleshooting

### Virtual Environment Issues

1. **Virtual environment not activating:**
   ```bash
   # Make sure you're in the correct directory
   pwd
   ls -la  # Check if 'venv' folder exists
   
   # Try full path activation
   source ./venv/bin/activate
   ```

2. **Package installation fails:**
   ```bash
   # Upgrade pip first
   pip install --upgrade pip
   
   # Then install requirements
   pip install -r requirements.txt
   ```

3. **Permission denied on Linux/Mac:**
   ```bash
   # Use python3 explicitly
   python3 -m venv venv
   source venv/bin/activate
   python3 -m pip install -r requirements.txt
   ```

4. **Checking if virtual environment is active:**
   ```bash
   # Your terminal prompt should show (venv)
   # Or check Python path:
   which python
   # Should point to your venv directory
   ```

### Dependency Management

- **Update requirements.txt:** After installing new packages:
  ```bash
  pip freeze > requirements.txt
  ```

- **Install specific versions:** Pin versions in requirements.txt for consistency
- **Clean install:** Delete `venv` folder and recreate if issues persist

## License

This project is for educational purposes.










