from django import forms
from django.forms import inlineformset_factory, DateInput
from .models import (
    Supplier, PurchaseRequest, PurchaseRequestItem,
    PurchaseOrder, PurchaseOrderItem,
    IncomingMaterialReport, IncomingMaterialItem
)

# --------------------------
# Supplier Form
# --------------------------
class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = '__all__'

# --------------------------
# Purchase Request Form
# --------------------------
class PRForm(forms.ModelForm):
    class Meta:
        model = PurchaseRequest
        fields = ['project', 'notes']

# Inline Formset for PurchaseRequest Items
PRItemFormSet = inlineformset_factory(
    PurchaseRequest, PurchaseRequestItem,
    fields=['item_name', 'sku', 'quantity', 'unit', 'date_needed', 'notes'],
    widgets={'date_needed': DateInput(attrs={'type': 'date'})},
    extra=1, can_delete=True
)

# --------------------------
# Purchase Order Form
# --------------------------
class POForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrder
        fields = ['po_number', 'supplier', 'linked_prs', 'expected_delivery', 'status', 'notes']
        widgets = {
            'expected_delivery': DateInput(attrs={'type': 'date'}),
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # show only approved PRs
            self.fields['linked_prs'].queryset = PurchaseRequest.objects.filter(status='approved')


# Inline Formset for PurchaseOrder Items
POItemFormSet = inlineformset_factory(
    PurchaseOrder, PurchaseOrderItem,
    fields=['item_name', 'sku', 'quantity', 'unit', 'unit_price'],
    extra=1, can_delete=True
)

# --------------------------
# Incoming Material Report Form
# --------------------------
class IMReportForm(forms.ModelForm):
    class Meta:
        model = IncomingMaterialReport
        fields = ['purchase_order', 'ref_no', 'supplier_name', 'status', 'notes']

# Inline Formset for IncomingMaterial Items
IMItemFormSet = inlineformset_factory(
    IncomingMaterialReport, IncomingMaterialItem,
    fields=['po_item', 'item_name', 'quantity', 'unit', 'notes'],
    extra=1, can_delete=True
)
