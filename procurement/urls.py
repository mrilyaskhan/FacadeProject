from django.urls import path
from . import views

urlpatterns = [
    # Suppliers
    path('suppliers/', views.supplier_list, name='supplier_list'),
    path('suppliers/add/', views.supplier_add, name='supplier_add'),

    # Purchase Requests
    path('purchase-requests/', views.pr_list, name='pr_list'),
    path('purchase-requests/add/', views.pr_add, name='pr_add'),
    path('purchase-requests/<int:pk>/', views.pr_detail, name='pr_detail'),
    path('purchase-requests/<int:pk>/approve/', views.pr_approve, name='pr_approve'),


    # Purchase Orders
    path('purchase-orders/', views.po_list, name='po_list'),
    path('purchase-orders/add/', views.po_add, name='po_add'),
    path('purchase-orders/<int:pk>/', views.po_detail, name='po_detail'),
    path("purchase-orders/<int:pk>/request-received/", views.request_received_po, name="request_received_po"),
    path("purchase-orders/<int:pk>/approve-received/", views.approve_received_po, name="approve_received_po"),

    # Incoming Material (goods receipt)
    path('incoming-materials/', views.im_list, name='im_list'),
    path('incoming-materials/add/', views.im_add, name='im_add'),
    path("incoming-materials/<int:pk>/", views.im_detail, name="im_detail"),
]
