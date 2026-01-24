# backend/billing/admin.py
from django.contrib import admin
from .models import BillingItem

@admin.register(BillingItem)
class BillingItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'member_name', 'member_id', 'status', 'due_date', 'created_at']
    list_filter = ['status', 'tag_type', 'created_at']
    search_fields = ['title', 'member_name', 'member_id']
    list_editable = ['status']
    date_hierarchy = 'created_at'