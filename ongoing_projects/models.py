from django.db import models

# Define choices first
STATUS_CHOICES = [
    ("N/A", "N/A"),
    ("In Progress", "In Progress"),
    ("Done", "Done"),
]

class OngoingProject(models.Model):
    code = models.CharField(max_length=50)
    po_number = models.CharField("Contract / P.O No", max_length=100)
    client = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    po_description = models.TextField()
    po_amount = models.DecimalField(max_digits=12, decimal_places=2)
    budgetary_cost = models.DecimalField(max_digits=12, decimal_places=2)
    expected_profit = models.DecimalField(max_digits=12, decimal_places=2)
    down_payment = models.CharField(max_length=100, blank=True, null=True)
    shop_drawing = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateField(null=True, blank=True)
    
    # ✅ Add status field after STATUS_CHOICES is defined
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="In Progress")

    def __str__(self):
        return self.code

    def update_status(self):
        components = self.components.all()  
        for comp in components:
            if any([
                comp.material_procurement != 'Done',
                comp.fabrication != 'Done',
                comp.hdg != 'Done',
                comp.powder_coating != 'Done',
                comp.erection != 'Done',
            ]):
                self.status = 'In Progress'
                self.save()
                return
        self.status = 'Complete'
        self.save()

class ProjectComponentStatus(models.Model):
    project = models.ForeignKey(OngoingProject, on_delete=models.CASCADE, related_name='components')
    component = models.CharField(max_length=100)
    material_procurement = models.CharField(max_length=20, choices=STATUS_CHOICES, default="N/A")
    fabrication = models.CharField(max_length=20, choices=STATUS_CHOICES, default="N/A")
    hdg = models.CharField(max_length=20, choices=STATUS_CHOICES, default="N/A")
    powder_coating = models.CharField(max_length=20, choices=STATUS_CHOICES, default="N/A")
    erection = models.CharField(max_length=20, choices=STATUS_CHOICES, default="N/A")

    def __str__(self):
        return self.component

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.project.update_status()

