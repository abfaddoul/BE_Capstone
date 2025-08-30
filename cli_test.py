#!/usr/bin/env python
"""
Command-line interface for testing Expense Tracker core functionality
"""
import os
import sys
import django
from datetime import date, datetime

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'expense_tracker.settings')
django.setup()

from django.contrib.auth import get_user_model
from expenses.models import Expense
from reports.models import Report
from reports.utils import generate_monthly_report, get_category_summary

User = get_user_model()

class ExpenseTrackerCLI:
    def __init__(self):
        self.current_user = None
    
    def show_menu(self):
        """Display main menu"""
        print("\n" + "="*50)
        print("💰 EXPENSE TRACKER CLI")
        print("="*50)
        print("1. Create Test User")
        print("2. Add Test Expenses")
        print("3. Generate Monthly Report")
        print("4. Show Category Summary")
        print("5. List All Expenses")
        print("6. List All Reports")
        print("7. Test API Endpoints")
        print("8. Cleanup Test Data")
        print("9. Exit")
        print("="*50)
    
    def create_test_user(self):
        """Create a test user"""
        try:
            username = input("Enter username (or press Enter for 'testuser'): ").strip()
            if not username:
                username = 'testuser'
            
            email = input("Enter email (or press Enter for 'test@example.com'): ").strip()
            if not email:
                email = 'test@example.com'
            
            password = input("Enter password (or press Enter for 'testpass123'): ").strip()
            if not password:
                password = 'testpass123'
            
            # Check if user already exists
            user, created = User.objects.get_or_create(
                username=username,
                defaults={'email': email}
            )
            
            if created:
                user.set_password(password)
                user.save()
                print(f"✓ User '{username}' created successfully!")
            else:
                print(f"✓ User '{username}' already exists!")
            
            self.current_user = user
            return user
            
        except Exception as e:
            print(f"✗ Error creating user: {e}")
            return None
    
    def add_test_expenses(self):
        """Add test expenses"""
        if not self.current_user:
            print("❌ Please create a user first!")
            return
        
        try:
            # Sample expense data
            expenses_data = [
                {'amount': 25.50, 'category': 'food', 'date': date(2025, 8, 30), 'description': 'Lunch at restaurant'},
                {'amount': 15.00, 'category': 'transport', 'date': date(2025, 8, 30), 'description': 'Bus fare'},
                {'amount': 50.00, 'category': 'shopping', 'date': date(2025, 8, 29), 'description': 'Groceries'},
                {'amount': 80.00, 'category': 'bills', 'date': date(2025, 8, 28), 'description': 'Electricity bill'},
                {'amount': 30.00, 'category': 'entertainment', 'date': date(2025, 8, 27), 'description': 'Movie tickets'},
            ]
            
            created_count = 0
            for data in expenses_data:
                expense, created = Expense.objects.get_or_create(
                    user=self.current_user,
                    amount=data['amount'],
                    category=data['category'],
                    date=data['date'],
                    description=data['description'],
                    defaults={'user': self.current_user}
                )
                if created:
                    created_count += 1
                    print(f"✓ Expense created: ${expense.amount} ({expense.category})")
                else:
                    print(f"⚠ Expense already exists: ${expense.amount} ({expense.category})")
            
            print(f"\n✓ {created_count} new expenses added!")
            
        except Exception as e:
            print(f"✗ Error adding expenses: {e}")
    
    def generate_monthly_report(self):
        """Generate monthly report"""
        if not self.current_user:
            print("❌ Please create a user first!")
            return
        
        try:
            month = input("Enter month (1-12, or press Enter for current month): ").strip()
            year = input("Enter year (or press Enter for current year): ").strip()
            
            if not month:
                month = datetime.now().month
            else:
                month = int(month)
            
            if not year:
                year = datetime.now().year
            else:
                year = int(year)
            
            # Generate report
            report = generate_monthly_report(self.current_user, month, year)
            print(f"\n📊 Monthly Report for {month}/{year}")
            print(f"Total Amount: ${report.total_amount}")
            print(f"Generated: {report.created_at}")
            
            # Show category summary
            category_summary = get_category_summary(self.current_user, month, year)
            if category_summary:
                print("\nCategory Breakdown:")
                for category in category_summary:
                    print(f"  - {category['category'].title()}: ${category['total']} ({category['count']} expenses)")
            else:
                print("\nNo expenses found for this month.")
                
        except Exception as e:
            print(f"✗ Error generating report: {e}")
    
    def show_category_summary(self):
        """Show category summary for current month"""
        if not self.current_user:
            print("❌ Please create a user first!")
            return
        
        try:
            current_month = datetime.now().month
            current_year = datetime.now().year
            
            category_summary = get_category_summary(self.current_user, current_month, current_year)
            
            if category_summary:
                print(f"\n📈 Category Summary for {current_month}/{current_year}")
                total = sum(cat['total'] for cat in category_summary)
                print(f"Total Expenses: ${total}")
                print("\nBreakdown:")
                for category in category_summary:
                    percentage = (category['total'] / total) * 100
                    print(f"  - {category['category'].title()}: ${category['total']} ({percentage:.1f}%)")
            else:
                print(f"\nNo expenses found for {current_month}/{current_year}")
                
        except Exception as e:
            print(f"✗ Error showing category summary: {e}")
    
    def list_expenses(self):
        """List all expenses for current user"""
        if not self.current_user:
            print("❌ Please create a user first!")
            return
        
        try:
            expenses = Expense.objects.filter(user=self.current_user).order_by('-date', '-created_at')
            
            if expenses:
                print(f"\n📝 Expenses for {self.current_user.username}:")
                print("-" * 60)
                for expense in expenses:
                    print(f"${expense.amount:>8.2f} | {expense.category:<15} | {expense.date} | {expense.description}")
                print("-" * 60)
                print(f"Total: {expenses.count()} expenses")
            else:
                print("\nNo expenses found.")
                
        except Exception as e:
            print(f"✗ Error listing expenses: {e}")
    
    def list_reports(self):
        """List all reports for current user"""
        if not self.current_user:
            print("❌ Please create a user first!")
            return
        
        try:
            reports = Report.objects.filter(user=self.current_user).order_by('-year', '-month')
            
            if reports:
                print(f"\n📊 Reports for {self.current_user.username}:")
                print("-" * 50)
                for report in reports:
                    print(f"{report.month:>2}/{report.year} | ${report.total_amount:>10.2f} | {report.created_at.strftime('%Y-%m-%d %H:%M')}")
                print("-" * 50)
                print(f"Total: {reports.count()} reports")
            else:
                print("\nNo reports found.")
                
        except Exception as e:
            print(f"✗ Error listing reports: {e}")
    
    def test_api_endpoints(self):
        """Test API endpoint accessibility"""
        try:
            from django.test import Client
            
            client = Client()
            endpoints = [
                ('/api/users/register/', 'User Registration'),
                ('/api/users/profile/', 'User Profile'),
                ('/api/expenses/', 'Expense List'),
                ('/api/reports/', 'Reports List'),
            ]
            
            print("\n🔗 Testing API Endpoints:")
            print("-" * 40)
            
            for endpoint, name in endpoints:
                try:
                    response = client.get(endpoint)
                    status = response.status_code
                    if status in [200, 401, 403]:  # Valid responses
                        print(f"✓ {name}: {status}")
                    else:
                        print(f"⚠ {name}: {status}")
                except Exception as e:
                    print(f"✗ {name}: Error - {e}")
            
            print("-" * 40)
            print("Note: 401/403 responses are expected for protected endpoints")
            
        except Exception as e:
            print(f"✗ Error testing API endpoints: {e}")
    
    def cleanup_test_data(self):
        """Clean up all test data"""
        if not self.current_user:
            print("❌ No user to clean up!")
            return
        
        try:
            confirm = input("⚠️  This will delete ALL test data. Are you sure? (yes/no): ").strip().lower()
            if confirm != 'yes':
                print("Cleanup cancelled.")
                return
            
            # Delete expenses
            expense_count = Expense.objects.filter(user=self.current_user).count()
            Expense.objects.filter(user=self.current_user).delete()
            
            # Delete reports
            report_count = Report.objects.filter(user=self.current_user).count()
            Report.objects.filter(user=self.current_user).delete()
            
            # Delete user
            username = self.current_user.username
            self.current_user.delete()
            self.current_user = None
            
            print(f"✓ Cleanup completed:")
            print(f"  - {expense_count} expenses deleted")
            print(f"  - {report_count} reports deleted")
            print(f"  - User '{username}' deleted")
            
        except Exception as e:
            print(f"✗ Error during cleanup: {e}")
    
    def run(self):
        """Main CLI loop"""
        print("🚀 Welcome to Expense Tracker CLI!")
        print("This tool helps you test the core functionality of the Expense Tracker API.")
        
        while True:
            self.show_menu()
            
            try:
                choice = input("\nEnter your choice (1-9): ").strip()
                
                if choice == '1':
                    self.create_test_user()
                elif choice == '2':
                    self.add_test_expenses()
                elif choice == '3':
                    self.generate_monthly_report()
                elif choice == '4':
                    self.show_category_summary()
                elif choice == '5':
                    self.list_expenses()
                elif choice == '6':
                    self.list_reports()
                elif choice == '7':
                    self.test_api_endpoints()
                elif choice == '8':
                    self.cleanup_test_data()
                elif choice == '9':
                    print("\n👋 Goodbye!")
                    break
                else:
                    print("❌ Invalid choice. Please enter a number between 1-9.")
                    
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Unexpected error: {e}")

if __name__ == '__main__':
    cli = ExpenseTrackerCLI()
    cli.run()
