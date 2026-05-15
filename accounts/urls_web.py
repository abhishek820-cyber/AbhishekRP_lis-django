from django.urls import path
from .views_web import LoginWebView, LogoutWebView, DashboardView, UserManagementView

urlpatterns = [
    path('',           DashboardView.as_view(),  name='home'),
    path('login/',     LoginWebView.as_view(),   name='login'),
    path('logout/',    LogoutWebView.as_view(),  name='logout'),
    path('dashboard/', DashboardView.as_view(),  name='dashboard'),
    path('users/',      UserManagementView.as_view(),  name='user-management'),
]