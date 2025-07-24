from django import forms
from .models import DeliveryNote
from django.forms import modelformset_factory
from .models import DeliveryItem

class DeliveryNoteForm(forms.ModelForm):
    class Meta:
        model = DeliveryNote
        fields = [
            'client_name', 'contract_no', 'supply_to', 'location',
            'ref_number', 'date', 'status', 'pdf_file'
        ]

class DeliveryItemForm(forms.ModelForm):
    class Meta:
        model = DeliveryItem
        fields = ['description', 'quantity', 'unit', 'remarks']
        


