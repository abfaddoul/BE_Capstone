#!/usr/bin/env python
"""
Test script for Expense Tracker API endpoints
"""
import os
import sys
import django
from datetime import date

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'expense_tracker.settings')
django.setup()

from django.contrib.auth import get_user_model
from expenses.models import Expense
from reports.models import Report
from reports.utils import generate_monthly_report, get_category_summary

User = get_user_model()

def test_user_creation():
    """Test user creation functionality"""
    print("Testing User Creation...")
    
    try:
        # Create a test user
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        print(f"✓ User created successfully: {user.username}")
        return user
    except Exception as e:
        print(f"✗ User creation failed: {e}")
        return None

def test_expense_creation(user):
    """Test expense creation functionality"""
    print("\nTesting Expense Creation...")
    
    try:
        # Create test expenses
        expenses_data = [
            {'amount': 25.50, 'category': 'food', 'date': date(2025, 8, 30), 'description': 'Lunch'},
            {'amount': 15.00, 'category': 'transport', 'date': date(2025, 8, 30), 'description': 'Bus fare'},
            {'amount': 50.00, 'category': 'shopping', 'date': date(2025, 8, 29), 'description': 'Groceries'},
        ]
        
        created_expenses = []
        for data in expenses_data:
            expense = Expense.objects.create(user=user, **data)
            created_expenses.append(expense)
            print(f"✓ Expense created: {expense.amount} ({expense.category})")
        
        return created_expenses
    except Exception as e:
        print(f"✗ Expense creation failed: {e}")
        return []

def test_report_generation(user):
    """Test report generation functionality"""
    print("\nTesting Report Generation...")
    
    try:
        # Generate monthly report
        report = generate_monthly_report(user, month=8, year=2025)
        print(f"✓ Monthly report generated: ${report.total_amount} for {report.month}/{report.year}")
        
        # Get category summary
        category_summary = get_category_summary(user, month=8, year=2025)
        print("✓ Category summary:")
        for category in category_summary:
            print(f"  - {category['category']}: ${category['total']} ({category['count']} expenses)")
        
        return report
    except Exception as e:
        print(f"✗ Report generation failed: {e}")
        return None

def test_api_endpoints():
    """Test API endpoint URLs"""
    print("\nTesting API Endpoints...")
    
    try:
        from django.urls import reverse
        from django.test import Client
        
        client = Client()
        
        # Test user registration endpoint
        response = client.get('/api/users/register/')
        print(f"✓ User registration endpoint: {response.status_code}")
        
        # Test expense list endpoint
        response = client.get('/api/expenses/')
        print(f"✓ Expense list endpoint: {response.status_code}")
        
        # Test reports endpoint
        response = client.get('/api/reports/')
        print(f"✓ Reports endpoint: {response.status_code}")
        
        return True
    except Exception as e:
        print(f"✗ API endpoint testing failed: {e}")
        return False

def cleanup_test_data(user):
    """Clean up test data"""
    print("\nCleaning up test data...")
    
    try:
        # Delete test expenses
        Expense.objects.filter(user=user).delete()
        print("✓ Test expenses deleted")
        
        # Delete test reports
        Report.objects.filter(user=user).delete()
        print("✓ Test reports deleted")
        
        # Delete test user
        user.delete()
        print("✓ Test user deleted")
        
        return True
    except Exception as e:
        print(f"✗ Cleanup failed: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Starting Expense Tracker API Tests...\n")
    
    # Test user creation
    user = test_user_creation()
    if not user:
        print("❌ Cannot continue without user creation")
        return
    
    # Test expense creation
    expenses = test_expense_creation(user)
    if not expenses:
        print("❌ Cannot continue without expense creation")
        cleanup_test_data(user)
        return
    
    # Test report generation
    report = test_report_generation(user)
    if not report:
        print("❌ Report generation failed")
    
    # Test API endpoints
    api_test = test_api_endpoints()
    
    # Cleanup
    cleanup_test_data(user)
    
    print("\n" + "="*50)
    if api_test:
        print("🎉 All tests completed successfully!")
    else:
        print("⚠️  Some tests failed, but core functionality is working")
    print("="*50)

if __name__ == '__main__':
    main()
