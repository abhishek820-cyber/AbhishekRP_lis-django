from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Frontend template routes
    path('', include('accounts.urls_web')),
    path('patients/', include('patients.urls_web')),
    path('orders/',   include('orders.urls_web')),
    path('results/',  include('results.urls_web')),
    path('labtests/', include('labtests.urls_web')), 

    # REST API endpoints
    path('api/v1/auth/',    include('accounts.urls')),
    path('api/v1/users/',   include('accounts.urls_users')),
    path('api/v1/patients/', include('patients.urls')),
    path('api/v1/tests/',   include('labtests.urls')),
    path('api/v1/orders/',  include('orders.urls')),
]