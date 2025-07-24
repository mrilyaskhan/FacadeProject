from django.urls import path
from .views import profile_view, add_user_view

urlpatterns = [
    path('profile/', profile_view, name='profile'),
    path('add-user/', add_user_view, name='add_user'),
]
