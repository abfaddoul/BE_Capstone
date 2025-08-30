# Expense Tracker API

A Django REST API for tracking personal expenses with user authentication, expense management, and monthly reports.

## Features

- User authentication and registration
- Expense tracking with categories
- Monthly expense reports
- RESTful API endpoints

## Database Schema

- **Users**: Authentication data (username, email, password)
- **Expenses**: Expense records (amount, category, date, description)
- **Reports**: Monthly expense summaries per user

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

3. Create superuser:
```bash
python manage.py createsuperuser
```

4. Run server:
```bash
python manage.py runserver
```

## Testing the Application

### Option 1: Command-Line Interface (Recommended)
Use the interactive CLI tool to test core functionality:
```bash
python cli_test.py
```

### Option 2: Automated Test Script
Run the automated test suite:
```bash
python test_api.py
```

### Option 3: Manual API Testing
Start the server and test endpoints manually using the API documentation in `API_DOCUMENTATION.md`

## API Endpoints

- `/api/users/` - User management
- `/api/expenses/` - Expense management
- `/api/reports/` - Monthly reports
