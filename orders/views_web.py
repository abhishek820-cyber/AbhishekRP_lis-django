from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

class OrderEntryView(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request):
        return render(request, 'order_entry.html')

class PhlebotomistWorklistView(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request):
        return render(request, 'phlebotomist_worklist.html')

class TechnicianWorklistView(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request):
        return render(request, 'technician_worklist.html')