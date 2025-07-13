from django.urls import path
from .views import dashboard, settings_view, edit_profile

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('settings/', settings_view, name='settings'),
    path('edit-profile/', edit_profile, name='edit_profile'),
]
