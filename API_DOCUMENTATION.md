# Expense Tracker API Documentation

## Overview
This document provides information about the Expense Tracker API endpoints, request/response formats, and testing instructions.

## Base URL
```
http://localhost:8000
```

## Authentication
Most endpoints require authentication. Use session authentication or basic authentication.

## API Endpoints

### 1. User Management

#### User Registration
- **URL**: `POST /api/users/register/`
- **Description**: Create a new user account
- **Request Body**:
```json
{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "securepassword123"
}
```
- **Response**: 201 Created with user details

#### User Profile
- **URL**: `GET /api/users/profile/`
- **Description**: Get or update current user profile
- **Authentication**: Required
- **Response**: 200 OK with user details

### 2. Expense Management

#### List/Create Expenses
- **URL**: `GET/POST /api/expenses/`
- **Description**: List all expenses or create new expense
- **Authentication**: Required
- **Query Parameters**:
  - `category`: Filter by category
  - `date`: Filter by date
  - `search`: Search in description
  - `ordering`: Sort by amount, date, or created_at
- **Request Body** (POST):
```json
{
    "amount": 25.50,
    "category": "food",
    "date": "2025-08-30",
    "description": "Lunch at restaurant"
}
```

#### Expense Detail
- **URL**: `GET/PUT/DELETE /api/expenses/{id}/`
- **Description**: Retrieve, update, or delete specific expense
- **Authentication**: Required
- **Response**: 200 OK with expense details

### 3. Reports

#### List Reports
- **URL**: `GET /api/reports/`
- **Description**: Get all monthly reports for current user
- **Authentication**: Required
- **Query Parameters**:
  - `year`: Filter by specific year

#### Report Detail
- **URL**: `GET /api/reports/detail/`
- **Description**: Get detailed monthly report with category breakdown
- **Authentication**: Required
- **Query Parameters**:
  - `month`: Month number (1-12)
  - `year`: Year number
- **Response**: 200 OK with report details and category summary

## Expense Categories
- `food` - Food and dining
- `transport` - Transportation costs
- `entertainment` - Entertainment and recreation
- `shopping` - Shopping and retail
- `bills` - Utility bills and services
- `health` - Healthcare expenses
- `education` - Educational costs
- `other` - Miscellaneous expenses

## Testing the API

### 1. Start the Server
```bash
python manage.py runserver
```

### 2. Test User Registration
```bash
curl -X POST http://localhost:8000/api/users/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"testpass123"}'
```

### 3. Test Expense Creation
```bash
curl -X POST http://localhost:8000/api/expenses/ \
  -H "Content-Type: application/json" \
  -d '{"amount":25.50,"category":"food","date":"2025-08-30","description":"Lunch"}'
```

### 4. Test Reports
```bash
curl http://localhost:8000/api/reports/detail/?month=8&year=2025
```

## Django Admin Interface
Access the admin interface at `http://localhost:8000/admin/` to manage users, expenses, and reports directly.

## Error Handling
The API returns appropriate HTTP status codes:
- 200: Success
- 201: Created
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 500: Internal Server Error
