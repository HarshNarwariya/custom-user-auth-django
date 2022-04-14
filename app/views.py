from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

# Create your views here.
class Home(LoginRequiredMixin, View):
    login_url = 'accounts:login'

    def get(self, request):
        return HttpResponse('Thanks for login')