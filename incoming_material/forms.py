from django import forms
from .models import IncomingMaterialReport, IncomingMaterialItem

class DateInput(forms.DateInput):
    input_type = 'date'  # ensures HTML5 date input

class IncomingMaterialReportForm(forms.ModelForm):
    class Meta:
        model = IncomingMaterialReport
        fields = ['date', 'ref_no']
        widgets = {
            'date': DateInput(attrs={'class': 'form-control small-input'}),
        }

class IncomingMaterialItemForm(forms.ModelForm):
    class Meta:
        model = IncomingMaterialItem
        fields = ['item_name', 'dimensions', 'quantity', 'supply_name', 'unit', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'class': 'notes-textarea'}),
        }
