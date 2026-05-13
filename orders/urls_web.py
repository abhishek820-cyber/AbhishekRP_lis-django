from django.urls import path
from .views_web import OrderEntryView, PhlebotomistWorklistView, TechnicianWorklistView

urlpatterns = [
    path('new/',                      OrderEntryView.as_view(),            name='order-entry'),
    path('worklist/phlebotomist/',    PhlebotomistWorklistView.as_view(),  name='phlebotomist-worklist'),
    path('worklist/technician/',      TechnicianWorklistView.as_view(),    name='technician-worklist'),
]