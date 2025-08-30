from rest_framework import generics, permissions
from rest_framework.response import Response
from django.utils import timezone
from .models import Report
from .utils import generate_monthly_report, get_user_reports, get_category_summary


class ReportListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        year = self.request.query_params.get('year')
        return get_user_reports(self.request.user, year)
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        data = []
        for report in queryset:
            data.append({
                'id': report.id,
                'month': report.month,
                'year': report.year,
                'total_amount': report.total_amount,
                'created_at': report.created_at
            })
        return Response(data)


class ReportDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Report.objects.filter(user=self.request.user)
    
    def retrieve(self, request, *args, **kwargs):
        month = self.request.query_params.get('month', timezone.now().month)
        year = self.request.query_params.get('year', timezone.now().year)
        
        # Generate or get the report
        report = generate_monthly_report(request.user, int(month), int(year))
        
        # Get category summary
        category_summary = get_category_summary(request.user, int(month), int(year))
        
        data = {
            'month': report.month,
            'year': report.year,
            'total_amount': report.total_amount,
            'category_summary': list(category_summary),
            'created_at': report.created_at
        }
        
        return Response(data)
