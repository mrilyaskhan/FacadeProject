from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from delivery_notes.views import dashboard

def public_landing_view(request):
    return redirect('login')

urlpatterns = [
    path('admin/', admin.site.urls),

    # Public root URL (no login required)
    path('', public_landing_view, name='home'),

    # Dashboard (protected)
    path('dashboard/', dashboard, name='dashboard'),

    # Login/logout
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # Password change
    path('accounts/password_change/', auth_views.PasswordChangeView.as_view(template_name='accounts/password_change.html'), name='password_change'),
    path('accounts/password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'), name='password_change_done'),
    path('accounts/', include('accounts.urls')),

    # App URLs
    path('delivery/', include('delivery_notes.urls')),
    path('incoming/', include('incoming_material.urls')),
    path('ongoing/', include('ongoing_projects.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
