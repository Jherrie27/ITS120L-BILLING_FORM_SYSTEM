# backend/billing/views.py
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import BillingItem
import json

def dashboard(request):
    """Main dashboard view"""
    in_progress = BillingItem.objects.filter(status='in_progress')
    done = BillingItem.objects.filter(status='done')
    
    context = {
        'in_progress': in_progress,
        'done': done,
    }
    return render(request, 'dashboard.html', context)

@csrf_exempt
@require_POST
def update_status(request):
    """Update billing item status via AJAX"""
    try:
        data = json.loads(request.body)
        item_id = data.get('item_id')
        new_status = data.get('status')
        
        item = get_object_or_404(BillingItem, id=item_id)
        item.status = new_status
        item.save()
        
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)

@csrf_exempt
@require_POST
def create_item(request):
    """Create new billing item"""
    try:
        data = json.loads(request.body)
        item = BillingItem.objects.create(
            title=data.get('title'),
            member_name=data.get('member_name'),
            member_id=data.get('member_id'),
            due_date=data.get('due_date'),
            status=data.get('status', 'in_progress'),
            tag_type=data.get('tag_type', 'SIGNED')
        )
        return JsonResponse({'success': True, 'item_id': item.id})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)
    
    ##(jherrie) para sa analytics 

    from django.db.models import Count
from django.utils import timezone
from django.shortcuts import render

from .models import PenaltyForm  # adjust if your model name differs


def analytics_view(request):
    # Base queryset
    transactions = PenaltyForm.objects.all()

    # Summary counts
    total_transactions = transactions.count()
    pending_count = transactions.filter(status="Pending").count()
    paid_count = transactions.filter(status="Paid").count()
    waived_count = transactions.filter(status="Waived").count()

    # Transactions grouped by date (daily)
    daily_data = (
        transactions
        .extra(select={'day': "date(created_at)"})
        .values('day')
        .annotate(count=Count('id'))
        .order_by('day')
    )

    # Prepare data for charts
    dates = [item['day'].strftime("%Y-%m-%d") for item in daily_data]
    daily_counts = [item['count'] for item in daily_data]

    context = {
        "total_transactions": total_transactions,
        "pending_count": pending_count,
        "paid_count": paid_count,
        "waived_count": waived_count,
        "dates": dates,
        "daily_counts": daily_counts,
    }

    return render(request, "analytics.html", context)
