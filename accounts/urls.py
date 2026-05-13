from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import LoginView, LogoutView, SessionTokenView

urlpatterns = [
    path('login/',          LoginView.as_view(),        name='api-login'),
    path('logout/',         LogoutView.as_view(),        name='api-logout'),
    path('token/refresh/',  TokenRefreshView.as_view(),  name='api-token-refresh'),
    path('session-token/',  SessionTokenView.as_view(),  name='api-session-token'),
]