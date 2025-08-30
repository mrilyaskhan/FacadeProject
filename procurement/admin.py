from django.contrib import admin
from .models import (
    Supplier, PurchaseRequest, PurchaseRequestItem,
    PurchaseOrder, PurchaseOrderItem,
    IncomingMaterialReport, IncomingMaterialItem
)

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_person', 'email', 'phone')
    search_fields = ('name', 'email', 'phone')

class PurchaseRequestItemInline(admin.TabularInline):
    model = PurchaseRequestItem
    extra = 1

@admin.register(PurchaseRequest)
class PRAdmin(admin.ModelAdmin):
    list_display = ('id', 'requested_by', 'project', 'status', 'request_date')
    list_filter = ('status', 'request_date')
    inlines = [PurchaseRequestItemInline]

class POItemInline(admin.TabularInline):
    model = PurchaseOrderItem
    extra = 1

@admin.register(PurchaseOrder)
class POAdmin(admin.ModelAdmin):
    list_display = ('po_number', 'supplier', 'order_date', 'status', 'expected_delivery')
    list_filter = ('status',)
    inlines = [POItemInline]

class IMItemInline(admin.TabularInline):
    model = IncomingMaterialItem
    extra = 1

@admin.register(IncomingMaterialReport)
class IMAdmin(admin.ModelAdmin):
    list_display = ('ref_no', 'date', 'purchase_order', 'status')
    inlines = [IMItemInline]
