from django.urls import path
from .views_web import PatientRegisterView, PatientListView

urlpatterns = [
    path('',         PatientListView.as_view(),     name='patient-list'),
    path('register/', PatientRegisterView.as_view(), name='patient-register'),
]