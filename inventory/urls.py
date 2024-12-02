# inventory/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # path('login/', auth_views.LoginView.as_view(), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # path('signup/', views.signup, name='signup'),
    # path('profile/', views.profile, name='profile'),
    # path('create/', views.property_create, name='create_property'),
    # path('<int:property_id>/edit/', views.property_edit, name='edit_property'),
    # path('<int:property_id>/delete/', views.property_delete, name='delete_property'),
]
