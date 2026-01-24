# backend/billing/models.py
from django.db import models

class BillingItem(models.Model):
    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
    ]
    
    TAG_CHOICES = [
        ('SIGNED', 'Signed'),
        ('UNSIGNED', 'Unsigned'),
    ]
    
    title = models.CharField(max_length=300)
    member_name = models.CharField(max_length=200)
    member_id = models.CharField(max_length=50)
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')
    tag_type = models.CharField(max_length=50, choices=TAG_CHOICES, default='SIGNED')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} - {self.member_name}"
    
    class Meta:
        ordering = ['-created_at']