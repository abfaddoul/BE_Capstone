from decimal import Decimal
from django.db.models import Sum, Count
from django.utils import timezone
from expenses.models import Expense
from .models import Report


def generate_monthly_report(user, month=None, year=None):
    """Generate or update monthly report for a user"""
    if month is None:
        month = timezone.now().month
    if year is None:
        year = timezone.now().year
    
    # Calculate total expenses for the month
    total_amount = Expense.objects.filter(
        user=user,
        date__month=month,
        date__year=year
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
    
    # Create or update report
    report, created = Report.objects.update_or_create(
        user=user,
        month=month,
        year=year,
        defaults={'total_amount': total_amount}
    )
    
    return report


def get_user_reports(user, year=None):
    """Get all reports for a user, optionally filtered by year"""
    queryset = Report.objects.filter(user=user)
    if year:
        queryset = queryset.filter(year=year)
    return queryset.order_by('-year', '-month')


def get_category_summary(user, month=None, year=None):
    """Get expense summary by category for a specific month"""
    if month is None:
        month = timezone.now().month
    if year is None:
        year = timezone.now().year
    
    return Expense.objects.filter(
        user=user,
        date__month=month,
        date__year=year
    ).values('category').annotate(
        total=Sum('amount'),
        count=Count('id')
    ).order_by('-total')
