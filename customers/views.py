from django.shortcuts import render
from django.http import request
from userauthentication import models
from django.views import View
from django.views.generic.edit import CreateView
from django.views.generic import UpdateView, TemplateView, DetailView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from userauthentication.models import User
from django.contrib.auth.views import LoginView, LogoutView
from customers.forms import CustomerProfileForm
from customers.models import CustomerProfile, CustomerNotifications
from django.views.generic import ListView
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from projectapp.models import Appointment

# Create your views here.

class CustomerProfileView(SuccessMessageMixin, UpdateView):
    model = CustomerProfile
    form_class = CustomerProfileForm
    template_name ="customer/profile.html"
    
    def get_object(self):
        return self.request.user.customer_profile
    
    def get_success_url(self):
        return reverse_lazy("customer-dashboard")

class NotificationSeeen(SuccessMessageMixin, View):
    def post(self, request, pk):
        notification = get_object_or_404(CustomerNotifications, pk=pk, customer=request.user.customer_profile)
        
        notification.seen = True
        notification.save()
        return redirect("customer_dashboard")

class AllNotifications(SuccessMessageMixin, ListView):
    model = CustomerNotifications
    template_name = "customer/notifications.html"
    context_object_name = "allnotifications"

    def get_object(self):
        return self.request.user.customer_profile


class CustomerCancelAppointment(SuccessMessageMixin, View):
    def get(self, request, appointment_id):
        appointment = get_object_or_404(Appointment, id=appointment_id, customer=request.user.customer_profile)
        return render(request, "customer/confirm_cancel.html", {"appointment":appointment})
    
    def post(self, request, appointment_id):
        appointment = get_object_or_404(Appointment, id=appointment_id, customer=request.user.customer_profile)
        
        appointment.status = "cancel"
        appointment.save()
        
        return redirect("customer-dashboard")

    
class CustomerDashBoard(ListView):
    model = Appointment
    template_name = "customer/userdashboard.html"
    context_object_name = "appointments"

    def get_object(self):
        return self.request.user.customer_profile


class CustomerReactivateAppointment(View):
    
    def post(self, request, appointment_id):
        appointment = get_object_or_404(Appointment, id=appointment_id, customer=request.user.customer_profile)
        
        if appointment.booking_type == "Cash":
            appointment.status = "confirmed"
        else:
            appointment.status = "pending"
        
        appointment.save()
        
        return redirect("customer-dashboard")


class CustomerAppointmentDetails(DetailView):
    model = Appointment
    template_name = "customer/appointment-details.html"
    context_object_name = "appointment"


class CustomerAppointments(ListView):
    model = Appointment
    ordering = ["-created_at", "-id"]
    template_name = "customer/appointments.html"
    context_object_name = "appointments"
    
    
    def get_object(self):
        return self.request.user.customer_profile

