from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

class TestMenuView(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request):
        return render(request, 'testmenu.html')