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

## API Endpoints

- `/api/users/` - User management
- `/api/expenses/` - Expense management
- `/api/reports/` - Monthly reports
