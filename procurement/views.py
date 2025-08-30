from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Supplier, PurchaseRequest, PurchaseOrder, IncomingMaterialReport
from .forms import SupplierForm, PRForm, PRItemFormSet, POForm, POItemFormSet, IMReportForm, IMItemFormSet
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages

# Suppliers
@login_required
def supplier_list(request):
    qs = Supplier.objects.all()
    return render(request, 'procurement/suppliers_list.html', {'suppliers': qs})

@login_required
def supplier_add(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('supplier_list')
    else:
        form = SupplierForm()
    return render(request, 'procurement/supplier_add.html', {'form': form})

# Purchase Requests
# Helper function to check if user is manager
def is_manager(user):
    return user.is_superuser or user.groups.filter(name='Manager').exists()

@login_required
def pr_list(request):
    query = request.GET.get('q', '')  # for optional search
    page_number = request.GET.get('page', 1)

    # Base queryset
    if is_manager(request.user):
        prs_qs = PurchaseRequest.objects.filter(status='pending').order_by('-request_date')
        is_manager_view = True
    else:
        prs_qs = PurchaseRequest.objects.filter(requested_by=request.user).order_by('-request_date')
        is_manager_view = False

    # Optional search by project string
    if query:
        # Filter in Python only if a search query exists
        prs_qs = [pr for pr in prs_qs if query.lower() in str(pr.project).lower()]

    # Pagination: 10 per page
    paginator = Paginator(prs_qs, 10)
    prs_page = paginator.get_page(page_number)

    context = {
        'prs': prs_page,
        'is_manager': is_manager_view,
        'query': query,
    }
    return render(request, 'procurement/pr_list.html', context)


@login_required
@user_passes_test(is_manager)
def pr_approve(request, pk):
    pr = get_object_or_404(PurchaseRequest, pk=pk)
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "approve":
            pr.status = "approved"
            pr.approved_by = request.user
        elif action == "reject":
            pr.status = "rejected"
            pr.approved_by = request.user
        pr.save()
        return redirect('pr_list')
    return render(request, 'procurement/pr_approve.html', {'pr': pr})

@login_required
def pr_add(request):
    if request.method == 'POST':
        form = PRForm(request.POST)
        if form.is_valid():
            pr = form.save(commit=False)
            pr.requested_by = request.user  # assign the logged-in user
            pr.save()

            formset = PRItemFormSet(request.POST, instance=pr)
            if formset.is_valid():
                formset.save()
                return redirect('pr_list')
            else:
                print(formset.errors)  # debug formset errors
        else:
            print(form.errors)  # debug main form errors
            formset = PRItemFormSet()
    else:
        form = PRForm()
        formset = PRItemFormSet()

    return render(request, 'procurement/pr_add.html', {'form': form, 'formset': formset})


@login_required
def pr_detail(request, pk):
    pr = get_object_or_404(PurchaseRequest, pk=pk)
    return render(request, 'procurement/pr_detail.html', {'pr': pr})

# Purchase Orders
@login_required
def po_list(request):
    pos = PurchaseOrder.objects.all().order_by('-order_date')
    return render(request, 'procurement/po_list.html', {'pos': pos})

@login_required
def po_add(request):
    if request.method == 'POST':
        form = POForm(request.POST)
        formset = POItemFormSet(request.POST)
        if form.is_valid():
            po = form.save(commit=False)
            formset = POItemFormSet(request.POST, instance=po)
            if formset.is_valid():
                po.save()
                formset.save()
                messages.success(request, f"PO {po.po_number} created successfully.")
                return redirect('po_list')
            else:
                print("Formset errors:", formset.errors)
        else:
            print("Form errors:", form.errors)
            formset = POItemFormSet(request.POST)
    else:
        form = POForm()
        formset = POItemFormSet()
    return render(request, 'procurement/po_add.html', {'form': form, 'formset': formset})

@login_required
def request_received_po(request, pk):
    po = get_object_or_404(PurchaseOrder, pk=pk)
    if po.status == "sent" and not po.received_request:
        po.received_request = True
        po.save()
        messages.success(request, f"Received request submitted for PO {po.po_number}")
    else:
        messages.error(request, "This PO cannot be marked as received request.")
    return redirect("po_detail", pk=pk)


@login_required
@user_passes_test(lambda u: u.is_superuser or u.groups.filter(name__in=['Manager']).exists())
def approve_received_po(request, pk):
    po = get_object_or_404(PurchaseOrder, pk=pk)
    if po.received_request and po.status == "sent":
        po.status = "received"
        po.received_request = False
        po.save()

        from .models import IncomingMaterialReport, IncomingMaterialItem
        import uuid

        # Create Material Report
        report = IncomingMaterialReport.objects.create(
            purchase_order=po,
            ref_no=f"{po.po_number}-{uuid.uuid4().hex[:6]}",
            supplier_name=po.supplier.name if po.supplier else None,
            status="received",
            notes=f"Auto-created from PO {po.po_number}",
            approved_by=request.user   # ✅ assign the approver
        )

        # Create Material Items
        for item in po.items.all():
            IncomingMaterialItem.objects.create(
                report=report,
                po_item=item,
                item_name=item.item_name,
                quantity=item.quantity,
                unit=item.unit,
            )

        messages.success(request, f"PO {po.po_number} marked as received. Material Report {report.ref_no} created.")
    else:
        messages.error(request, "This PO cannot be approved as received.")

    return redirect("im_list")



def po_detail(request, pk):
    po = get_object_or_404(PurchaseOrder, pk=pk)

    # Check if user is Manager
    is_manager = request.user.groups.filter(name="Manager").exists()

    return render(request, 'procurement/po_detail.html', {
        'po': po,
        'is_manager': is_manager,
    })

# Incoming Materials
@login_required
def im_list(request):
    reports = IncomingMaterialReport.objects.select_related('approved_by', 'purchase_order').all()

    # Add a helper attribute to each report
    for r in reports:
        if r.approved_by:
            if r.approved_by.is_superuser:
                r.approved_role = "Admin"
            elif r.approved_by.groups.filter(name="Manager").exists():
                r.approved_role = "Manager"
            else:
                r.approved_role = "User"
        else:
            r.approved_role = None

    return render(request, 'procurement/im_list.html', {'reports': reports})


@login_required
def im_add(request):
    if request.method == 'POST':
        form = IMReportForm(request.POST)
        if form.is_valid():
            rpt = form.save()
            formset = IMItemFormSet(request.POST, instance=rpt)
            if formset.is_valid():
                formset.save()
                return redirect('im_list')
    else:
        form = IMReportForm()
        formset = IMItemFormSet()
    return render(request, 'procurement/im_add.html', {'form': form, 'formset': formset})

@login_required
def im_detail(request, pk):
    rpt = get_object_or_404(IncomingMaterialReport, pk=pk)
    return render(request, 'procurement/im_detail.html', {'report': rpt})
