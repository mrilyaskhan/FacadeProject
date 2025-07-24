from django.db import models

class IncomingMaterialReport(models.Model):
    date = models.DateField()
    ref_no = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.ref_no} - {self.date}"

class IncomingMaterialItem(models.Model):
    report = models.ForeignKey(IncomingMaterialReport, on_delete=models.CASCADE, related_name='items')
    item_name = models.CharField(max_length=200)
    dimensions = models.CharField(max_length=100)
    quantity = models.IntegerField()
    supply_name = models.CharField(max_length=200)
    unit = models.CharField(max_length=50)
    notes = models.TextField(blank=True, null=True)
