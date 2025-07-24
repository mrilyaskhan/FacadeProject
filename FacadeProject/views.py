from django.shortcuts import render
from django.db.models.functions import TruncMonth
from django.db.models import Count
from ongoing_projects.models import OngoingProject
from delivery_notes.models import DeliveryNote
from incoming_material.models import IncomingMaterialReport  # ✅ Correct model name
import json
from django.utils.safestring import mark_safe

def dashboard_view(request):
    # Summary counts
    ongoing = OngoingProject.objects.exclude(status='Done').count()
    completed = OngoingProject.objects.filter(status='Done').count()
    approved_notes = DeliveryNote.objects.filter(status='Approved').count()

    # Group by month using TruncMonth
    ongoing_by_month = (
        OngoingProject.objects
        .annotate(month=TruncMonth('date'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )

    delivery_by_month = (
        DeliveryNote.objects
        .annotate(month=TruncMonth('date'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )

    material_by_month = (
        IncomingMaterialReport.objects
        .annotate(month=TruncMonth('date'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )

    def format_monthly_data(queryset):
        data = {}
        for item in queryset:
            month_name = item['month'].strftime('%b %Y') if item['month'] else 'Unknown'
            data[month_name] = item['count']
        return data

    ongoing_data = format_monthly_data(ongoing_by_month)
    delivery_data = format_monthly_data(delivery_by_month)
    material_data = format_monthly_data(material_by_month)

    # Align all months
    all_months = sorted(set(ongoing_data) | set(delivery_data) | set(material_data))

    chart_data = {
        'months': all_months,
        'ongoing_counts': [ongoing_data.get(month, 0) for month in all_months],
        'delivery_counts': [delivery_data.get(month, 0) for month in all_months],
        'material_counts': [material_data.get(month, 0) for month in all_months],
    }

    context = {
        'ongoing_projects': ongoing,
        'completed_projects': completed,
        'approved_delivery_notes': approved_notes,
        'total_ongoing_projects': ongoing,
        'total_delivery_notes': DeliveryNote.objects.count(),
        'total_incoming_materials': IncomingMaterialReport.objects.count(),  # ✅
        'chart_data': chart_data,
    }

    return render(request, 'dashboard.html', context)
