from django.db import models

class DeliveryNote(models.Model):
    # removed so_number
    ref_number = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Pending'), ('Approved', 'Approved')],
        default='Pending'
    )
    branch = models.CharField(max_length=100, default="Steel Department")

    # client fields
    client_name = models.CharField(max_length=255, blank=True)
    contract_no = models.CharField(max_length=255, blank=True)
    supply_to = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=255, blank=True)

    pdf_file = models.FileField(upload_to='pdfs/', blank=True, null=True)
    
    def __str__(self):
        return f"{self.client_name} - {self.ref_number}"

class DeliveryItem(models.Model):
    delivery_note = models.ForeignKey(
        DeliveryNote,
        on_delete=models.CASCADE,
        related_name='items'
    )
    description = models.TextField()
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=50)
    remarks = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.delivery_note.ref_number}: {self.description} ({self.quantity} {self.unit})"


