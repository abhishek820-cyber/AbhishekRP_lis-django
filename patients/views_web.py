from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

class PatientRegisterView(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request):
        return render(request, 'patient_register.html')

class PatientListView(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request):
        return render(request, 'patient_list.html')