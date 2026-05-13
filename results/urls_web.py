from django.urls import path
from .views_web import ClinicalResultView

urlpatterns = [
    path('', ClinicalResultView.as_view(), name='clinical-results'),
]