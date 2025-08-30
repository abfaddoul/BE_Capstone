from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports')
    month = models.IntegerField()
    year = models.IntegerField()
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'month', 'year']
        ordering = ['-year', '-month']
    
    def __str__(self):
        return f"{self.user.username} - {self.month}/{self.year} - ${self.total_amount}"
