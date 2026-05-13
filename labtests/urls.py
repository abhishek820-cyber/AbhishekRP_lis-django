from django.urls import path
from .views import TestMenuListCreateView, TestMenuDetailView, AssayListCreateView, AssayDetailView

urlpatterns = [
    path('menus/',          TestMenuListCreateView.as_view(), name='api-menu-list'),
    path('menus/<int:pk>/', TestMenuDetailView.as_view(),     name='api-menu-detail'),
    path('assays/',         AssayListCreateView.as_view(),    name='api-assay-list'),
    path('assays/<int:pk>/', AssayDetailView.as_view(),       name='api-assay-detail'),
]