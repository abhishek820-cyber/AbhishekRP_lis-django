from django.urls import path
from .views import UserListCreateView, UserDetailView, UserAccessListCreateView

urlpatterns = [
    path('',        UserListCreateView.as_view(),    name='api-user-list'),
    path('<int:pk>/', UserDetailView.as_view(),      name='api-user-detail'),
    path('access/', UserAccessListCreateView.as_view(), name='api-user-access'),
]