from django.shortcuts import render
from django.http import request
from userauthentication import models
from django.views import View
from django.views.generic.edit import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from .forms import UserRegisterForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect
# Create your views here.


class CustomerRegisterView(SuccessMessageMixin, CreateView):
    form_class = UserRegisterForm
    template_name = "auth/register.html"
    success_url = reverse_lazy("user_login")
    
    def form_valid(self, form):
        user = form.save(commit=False)
        user.user_type ="customer"
        user.save()
        return super().form_valid(form)

class BarberRegisterView(SuccessMessageMixin, CreateView):
    form_class = UserRegisterForm
    template_name = "auth/register-barber.html"
    success_url = reverse_lazy("user_login")
    
    def form_valid(self, form):
        user = form.save(commit=False)
        user.user_type ="barber"
        user.save()
        return super().form_valid(form)

class CustomLoginView(SuccessMessageMixin, LoginView):
    template_name = "auth/login.html"
    def get_success_url(self):
        if self.request.user.user_type == "barber":
            return reverse_lazy("barber-dashboard")
        
        return reverse_lazy("home")

class CustomLogoutView(View):
    def post(self, request):
        logout(request)
        return redirect("home")
