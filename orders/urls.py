from django.urls import path
from .views import OrderListCreateView, OrderDetailView, OrderCollectView, OrderReceiveView
from results.views import ResultCreateView, OrderReportView

urlpatterns = [
    path('',                        OrderListCreateView.as_view(), name='api-order-list'),
    path('<int:pk>/',               OrderDetailView.as_view(),     name='api-order-detail'),
    path('<int:pk>/collect/',       OrderCollectView.as_view(),    name='api-order-collect'),
    path('<int:pk>/receive/',       OrderReceiveView.as_view(),    name='api-order-receive'),
    path('<int:order_id>/results/', ResultCreateView.as_view(),    name='api-order-results'),
    path('<int:order_id>/report/',  OrderReportView.as_view(),     name='api-order-report'),
]