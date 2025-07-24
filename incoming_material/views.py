from django.shortcuts import render, get_object_or_404, redirect
from .models import IncomingMaterialReport, IncomingMaterialItem
from .forms import IncomingMaterialReportForm, IncomingMaterialItemForm
from django.forms import inlineformset_factory
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
import openpyxl
from django.http import HttpResponse

@login_required
def incoming_material_list(request):
    query = request.GET.get('q')
    reports_list = IncomingMaterialReport.objects.all().order_by('-id')

    if query:
        reports_list = reports_list.filter(
            Q(ref_no__icontains=query) |
            Q(items__item_name__icontains=query) |
            Q(items__supply_name__icontains=query)
        ).distinct()

    paginator = Paginator(reports_list, 8)  # 8 items per page
    page_number = request.GET.get('page')
    reports = paginator.get_page(page_number)

    return render(request, 'incoming_material/list.html', {
        'reports': reports,
        'query': query
    })


@login_required
def add_incoming_material(request):
    ItemFormSet = inlineformset_factory(
        IncomingMaterialReport,
        IncomingMaterialItem,
        form=IncomingMaterialItemForm,
        extra=1,
        can_delete=True
    )

    if request.method == 'POST':
        form = IncomingMaterialReportForm(request.POST)
        formset = ItemFormSet(request.POST, prefix='form')

        if form.is_valid() and formset.is_valid():
            report = form.save()
            items = formset.save(commit=False)
            for item in items:
                item.report = report
                item.save()
            return redirect('incoming_material_list')
    else:
        form = IncomingMaterialReportForm()
        formset = ItemFormSet(queryset=IncomingMaterialItem.objects.none(), prefix='form')

    return render(request, 'incoming_material/add.html', {
        'form': form,
        'formset': formset
    })

@login_required
def view_incoming_material(request, pk):
    report = get_object_or_404(IncomingMaterialReport, pk=pk)
    return render(request, 'incoming_material/view.html', {'report': report})

@login_required
def delete_incoming_material(request, pk):
    report = get_object_or_404(IncomingMaterialReport, pk=pk)
    report.delete()
    return redirect('incoming_material_list')

@login_required
def edit_incoming_material(request, pk):
    report = get_object_or_404(IncomingMaterialReport, pk=pk)

    ItemFormSet = inlineformset_factory(
        IncomingMaterialReport,
        IncomingMaterialItem,
        form=IncomingMaterialItemForm,
        extra=0,
        can_delete=True
    )

    if request.method == 'POST':
        form = IncomingMaterialReportForm(request.POST, instance=report)
        formset = ItemFormSet(request.POST, instance=report, prefix='form')

        if form.is_valid() and formset.is_valid():
            print("FORM VALID ✅")
            print("FORMSET VALID ✅")

            form.save()
            formset.save()
            return redirect('view_incoming_material', pk=pk)
        else:
            print("❌ Form errors:", form.errors)
            print("❌ Formset errors:")
            for subform in formset:
                print(subform.errors)

    else:
        form = IncomingMaterialReportForm(instance=report)
        formset = ItemFormSet(instance=report, prefix='form')

    return render(request, 'incoming_material/edit.html', {
        'form': form,
        'formset': formset,
        'report': report,
    })

@login_required
def export_incoming_material_excel(request, pk):
    report = get_object_or_404(IncomingMaterialReport, pk=pk)
    items = report.items.all()

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Incoming Material Report"

    # Header row
    ws.append([
        "S. No", "Item Name", "Dimensions", "Quantity", "Supply Name", "Unit", "Notes"
    ])

    # Item rows
    for i, item in enumerate(items, start=1):
        ws.append([
            i,
            item.item_name,
            item.dimensions,
            item.quantity,
            item.supply_name,
            item.unit,
            item.notes,
        ])

    # Prepare the response
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    filename = f"IncomingMaterial-{report.ref_no}.xlsx"
    response['Content-Disposition'] = f'attachment; filename={filename}'
    wb.save(response)
    return response

@login_required
def export_all_incoming_material_excel(request):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Incoming Material"

    headers = ['Ref No', 'Date', 'Item Name', 'Dimensions', 'Quantity', 'Supply Name', 'Unit', 'Notes']
    ws.append(headers)

    for report in IncomingMaterialReport.objects.all():
        for item in report.items.all():
            ws.append([
                report.ref_no,
                report.date.strftime("%d-%m-%Y"),
                item.item_name,
                item.dimensions,
                item.quantity,
                item.supply_name,
                item.unit,
                item.notes
            ])

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=Incoming_Material_All.xlsx'
    wb.save(response)
    return response