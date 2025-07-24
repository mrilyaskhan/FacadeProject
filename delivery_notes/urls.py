from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_delivery_notes, name='delivery_notes_list'),
    path('add/', views.add_delivery_note, name='add_delivery_note'),
    path('export/', views.export_delivery_notes_excel, name='export_delivery_notes_excel'),
    path('<int:pk>/edit/', views.edit_delivery_note, name='edit_delivery_note'),
    path('delete/<int:pk>/', views.delete_delivery_note, name='delete_delivery_note'),
    path('view/<int:pk>/', views.view_delivery_note, name='view_delivery_note'),
    path('delivery-note/<int:pk>/export/', views.export_single_delivery_note_excel, name='export_single_delivery_note_excel'),
]
