# inventory/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # path('login/', auth_views.LoginView.as_view(), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # path('signup/', views.signup, name='signup'),
    # path('profile/', views.profile, name='profile'),
    path('property/create/', views.create_property, name='create_property'),
    path('property/<int:property_id>/edit/', views.edit_property, name='edit_property'),
    path('property/<int:property_id>/delete/', views.delete_property, name='delete_property'),
]
