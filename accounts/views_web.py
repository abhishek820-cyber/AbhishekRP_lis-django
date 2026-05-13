from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from orders.models import OrderTransaction


class LoginWebView(View):
    """Renders login form and handles credential submission."""

    def get(self, request):
        # Already logged in — skip straight to dashboard
        if request.user.is_authenticated:
            return redirect('dashboard')
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)

        if user and user.is_active:
            login(request, user)
            return redirect('dashboard')

        # Generic error — never reveal which field was wrong
        return render(request, 'login.html', {
            'error': 'Invalid credentials. Please try again.'
        })


class LogoutWebView(View):
    def get(self, request):
        logout(request)
        return redirect('login')


class DashboardView(LoginRequiredMixin, View):
    """Role-specific dashboard with summary counts."""
    login_url = '/login/'

    def get(self, request):
        try:
            role = request.user.profile.role
        except Exception:
            role = 'Admin'

        context = {'role': role}

        # Build summary cards based on role
        if role in ('Admin', 'Physician', 'Nurse'):
            from patients.models import PatientMaster
            from django.utils import timezone
            context['total_patients'] = PatientMaster.objects.count()
            context['orders_today']   = OrderTransaction.objects.filter(
                ordered_at__date=timezone.now().date()
            ).count()

        if role in ('Phlebotomist', 'Admin'):
            context['pending_collection'] = OrderTransaction.objects.filter(
                order_status=OrderTransaction.STATUS_ORDERED
            ).count()

        if role in ('LabTechnician', 'Admin'):
            context['pending_lab'] = OrderTransaction.objects.filter(
                order_status=OrderTransaction.STATUS_COLLECTED
            ).count()
            context['in_lab'] = OrderTransaction.objects.filter(
                order_status=OrderTransaction.STATUS_IN_LAB
            ).count()

        return render(request, 'dashboard.html', context)