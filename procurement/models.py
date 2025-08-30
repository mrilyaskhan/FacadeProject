from django.db import models
from django.conf import settings
from django.utils import timezone

# ---------- Supplier ----------
class Supplier(models.Model):
    name = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=120, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    rating = models.PositiveSmallIntegerField(blank=True, null=True)  # 1..5
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


# ---------- Purchase Request (header) ----------
PR_STATUS = [
    ('pending', 'Pending'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
]

class PurchaseRequest(models.Model):
    requested_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='approved_requests'
    )
    project = models.ForeignKey('ongoing_projects.OngoingProject', on_delete=models.SET_NULL, null=True, blank=True)
    request_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=PR_STATUS, default='pending')
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"PR-{self.id} ({self.get_status_display()})"



# ---------- Purchase Request Item (lines) ----------
class PurchaseRequestItem(models.Model):
    purchase_request = models.ForeignKey(PurchaseRequest, on_delete=models.CASCADE, related_name='items')
    item_name = models.CharField(max_length=255)
    sku = models.CharField(max_length=100, blank=True, null=True)
    quantity = models.DecimalField(max_digits=12, decimal_places=3, default=1)
    unit = models.CharField(max_length=30, default='pcs')
    date_needed = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.item_name} ({self.quantity} {self.unit})"


# ---------- Purchase Order ----------
PO_STATUS = [
    ('draft', 'Draft'),
    ('sent', 'Sent'),
    ('received', 'Received'),
    ('cancelled', 'Cancelled'),
]

class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=50, unique=True, blank=True)  # auto-generated if blank
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    linked_prs = models.ManyToManyField(PurchaseRequest, blank=True)
    order_date = models.DateField(auto_now_add=True)
    expected_delivery = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=PO_STATUS, default='draft')
    notes = models.TextField(blank=True, null=True)

    # --- NEW FIELDS for Received workflow ---
    received_request = models.BooleanField(default=False)  # user requested received
    received_approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='received_approved'
    )

    class Meta:
        ordering = ['-order_date']

    def __str__(self):
        return self.po_number or f"PO-{self.id}"

    def save(self, *args, **kwargs):
        if not self.po_number:
            stamp = timezone.now().strftime("%Y%m%d%H%M%S")
            self.po_number = f"PO{stamp}"
        super().save(*args, **kwargs)



# ---------- Purchase Order Items ----------
class PurchaseOrderItem(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name='items')
    item_name = models.CharField(max_length=255)
    sku = models.CharField(max_length=100, blank=True, null=True)
    quantity = models.DecimalField(max_digits=12, decimal_places=3, default=1)
    unit = models.CharField(max_length=30, default='pcs')
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    total_price = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.total_price = (self.quantity or 0) * (self.unit_price or 0)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.item_name} ({self.quantity} {self.unit})"


# ---------- Incoming Material (Goods Receipt) ----------
IM_STATUS = [
    ('pending', 'Pending'),
    ('received', 'Received'),
    ('partial', 'Partially Received'),
]

class IncomingMaterialReport(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    ref_no = models.CharField(max_length=150, unique=True)
    supplier_name = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, choices=IM_STATUS, default='pending')
    notes = models.TextField(blank=True, null=True)

    # ✅ New field to track who approved the material
    approved_by = models.ForeignKey(
        "auth.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="approved_reports"
    )

    def __str__(self):
        return f"{self.ref_no} - {self.date}"


class IncomingMaterialItem(models.Model):
    report = models.ForeignKey(IncomingMaterialReport, on_delete=models.CASCADE, related_name='items')
    po_item = models.ForeignKey(PurchaseOrderItem, on_delete=models.SET_NULL, null=True, blank=True)
    item_name = models.CharField(max_length=255)
    quantity = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    unit = models.CharField(max_length=30, default='pcs')
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.item_name} ({self.quantity} {self.unit})"

