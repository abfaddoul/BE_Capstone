from django.contrib import admin
from .models import Report


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['user', 'month', 'year', 'total_amount', 'created_at']
    list_filter = ['year', 'month', 'created_at']
    search_fields = ['user__username']
    ordering = ['-year', '-month']
