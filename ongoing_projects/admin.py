from django.contrib import admin
from .models import OngoingProject, ProjectComponentStatus

admin.site.register(OngoingProject)
admin.site.register(ProjectComponentStatus)
