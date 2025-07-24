from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_ongoing_projects, name='ongoing_projects_list'),  
    path('add/', views.add_ongoing_project, name='add_ongoing_project'),
    path('view/<int:pk>/', views.view_ongoing_project, name='view_ongoing_project'),
    path('<int:pk>/edit/', views.edit_ongoing_project, name='edit_ongoing_project'),
    path('<int:pk>/delete/', views.delete_ongoing_project, name='delete_ongoing_project'),
    path('export/', views.export_ongoing_projects_to_excel, name='export_ongoing_projects_to_excel'),
    path('ongoing/<int:pk>/export_excel/', views.export_single_project_excel, name='export_ongoing_project_excel'),
    path('ongoing/<int:pk>/download_pdf/', views.download_single_project_pdf, name='download_ongoing_project_pdf'),

]
