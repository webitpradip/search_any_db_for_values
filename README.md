# Database-Agnostic Search Application

A Django-based web application that provides dynamic search functionality across various types of databases.

## Features

- Support for multiple database types:
  - MySQL
  - PostgreSQL
  - Oracle
  - MongoDB
  - SQL Server
  - SQLite
- Dynamic database connection
- Cross-table search functionality
- Clean and responsive user interface

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd search_any_db_for_values
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Unix or MacOS:
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Apply database migrations:
```bash
python manage.py migrate
```

5. Run the development server:
```bash
python manage.py runserver
```

The application will be available at `http://localhost:8000`

## Usage

1. Select the database type from the dropdown menu
2. Enter the connection details:
   - Host (not required for SQLite)
   - Database name (or file path for SQLite)
   - Username (not required for SQLite)
   - Password (not required for SQLite)
3. Enter the search value
4. Click "Search Database" to perform the search

The results will be displayed in a table format, showing:
- Table name
- Column name (where the match was found)
- Matching rows with all their columns

## Security Considerations

- The application handles database credentials securely
- All database connections are properly closed after use
- Input validation is performed to prevent SQL injection
- For production use:
  - Enable SSL/TLS
  - Set DEBUG = False
  - Update SECRET_KEY
  - Configure proper security settings

## Dependencies

- Django
- SQLAlchemy
- Database-specific drivers:
  - PyMySQL (MySQL)
  - psycopg2-binary (PostgreSQL)
  - pymongo (MongoDB)
  - cx-Oracle (Oracle)
  - pyodbc (SQL Server)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
