from django.urls import path
from .views_web import TestMenuView

urlpatterns = [
    path('', TestMenuView.as_view(), name='test-menus'),
]