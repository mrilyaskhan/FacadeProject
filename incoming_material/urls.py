from django.urls import path
from . import views

urlpatterns = [
    path('', views.incoming_material_list, name='incoming_material_list'),
    path('add/', views.add_incoming_material, name='add_incoming_material'),
    path('view/<int:pk>/', views.view_incoming_material, name='view_incoming_material'),
    path('delete/<int:pk>/', views.delete_incoming_material, name='delete_incoming_material'),
    path('edit/<int:pk>/', views.edit_incoming_material, name='edit_incoming_material'),
    path('export/<int:pk>/', views.export_incoming_material_excel, name='export_incoming_material_excel'),
    path('export/all/', views.export_all_incoming_material_excel, name='export_all_incoming_material_excel'),
]
