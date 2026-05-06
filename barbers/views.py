from django.shortcuts import render
from django.http import request
from userauthentication import models
from django.views import View
from django.views.generic.edit import CreateView
from django.views.generic import UpdateView, ListView, TemplateView, DeleteView, DetailView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from userauthentication.models import User
from django.contrib.auth.views import LoginView, LogoutView
from barbers.forms import BarberProfileForm, ServiceForm, timeSlotsForm
from barbers.models import BarberProfile, Notifications, Availability
from projectapp.models import Service, Category, Appointment, Billing
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.core.paginator import Paginator
# Create your views here.


class BarberProfileView(SuccessMessageMixin, UpdateView):
    model = BarberProfile
    form_class = BarberProfileForm
    template_name ="barber/profile.html"
    success_message = "Profile update successfully"
    
    def get_object(self):
        return self.request.user.barber_profile
    
    def get_success_url(self):
        return reverse_lazy("barber-dashboard")


class BarberDashBoard(ListView):
    model = Appointment
    template_name = "barber/dashboardbarber.html"
    
    def get_object(self):
        return self.request.user.barber_profile
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        barber = self.request.user.barber_profile
        total = Billing.objects.filter(appointment__service__owner=barber, status="Paid").aggregate(total_amount=Sum("total"))
        total_booking = Appointment.objects.filter(barber=barber, payment_status="paid").count()
        notifications = Notifications.objects.filter(barber=barber)
        context["total_amount"] = total["total_amount"] or 0
        context["total_booking"] = total_booking
        context["notifications"] = notifications
        return context

class CreateServiceView(SuccessMessageMixin, CreateView):
    model = Service
    form_class = ServiceForm
    template_name = "barber/createservice.html"
    
    def form_valid(self, form):
        form.instance.owner = self.request.user.barber_profile
        return super().form_valid(form)
    
    def get_initial(self):
        initial = super().get_initial()
        initial['category'] = Category.objects.get(name="Haircut")
        return initial
    
    def get_success_url(self):
        return reverse_lazy("barber-dashboard")


class AllServices(SuccessMessageMixin, ListView):
    model = Service
    template_name = "barber/allservices.html"
    context_object_name = "services"
    def get_object(self):
        return self.request.user.barber_profile

class AcceptAppointment(SuccessMessageMixin, View):
    def post(self, request, pk):
        appointment = get_object_or_404(Appointment, pk=pk, barber=request.user.barber_profile)
        
        if appointment.status == "confirmed":
            appointment.status = "accepted"
            appointment.save()
    
        return redirect("barber_dashboard")
    
class CancelAppointment(SuccessMessageMixin, View):
    def post(self, request, pk):
        appointment = get_object_or_404(Appointment, pk=pk, barber=request.user.barber_profile)
        
        appointment.status = "cancel"
        appointment.save()
        
        return redirect("barber-dashboard")

class MarkAppointmentCompleted(SuccessMessageMixin, View):
    def post(self, request, pk):
        appointment = get_object_or_404(Appointment, pk=pk, barber=request.user.barber_profile)
        
        appointment.status = "completed"
        appointment.save()
        return redirect("barber-dashboard")

class NotificationSeeen(SuccessMessageMixin, View):
    def post(self, request, pk):
        notification = get_object_or_404(Notifications, pk=pk, barber=request.user.barber_profile)
        
        notification.seen = True
        notification.save()
        return redirect("barber-dashboardd")


class AllNotifications(SuccessMessageMixin, ListView):
    model = Notifications
    template_name = "barber/all-notifications.html"
    context_object_name = "allnotifications"

    def get_object(self):
        return self.request.user.barber_profile

    
class BarberDetails(DetailView):
    model = BarberProfile
    template_name = "barber/barber-details.html"
    context_object_name = "barber"

class BarberAppointments(ListView):
    model = Appointment
    paginate_by = 6
    ordering = ["-created_at"]
    template_name = "barber/appointments.html"
    context_object_name = "appointments"

    def get_object(self):
        return self.request.user.barber_profile
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        appointments = Appointment.objects.filter(barber=self.request.user.barber_profile)
        paginator = Paginator(appointments, 5)
        page_number = self.request.GET.get("page")
        context["page_obj"] = paginator.get_page(page_number)
        return context

class CreateTimeSlots(CreateView):
    model = Availability
    form_class = timeSlotsForm
    template_name = "barber/create-timeslots.html"
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["barber"] = self.request.user.barber_profile
        return kwargs
    
    def form_valid(self, form):
        form.instance.barber = self.request.user.barber_profile
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy("barber-dashboard")
    
class BarberSchedule(ListView):
    model = Availability
    template_name = "barber/barber-schedule.html"
    
    def get_object(self):
        return self.request.user.barber_profile

class UpdateSchedule(UpdateView):
    model = Availability
    form_class = timeSlotsForm
    template_name="barber/update-schedule.html"
    
    def get_queryset(self):
        return Availability.objects.filter(barber=self.request.user.barber_profile)
    
    def get_success_url(self):
        return reverse_lazy("barber-dashboard")

class BarberAppointmentDetails(DetailView):
    model = Appointment
    template_name = "barber/appointment-details.html"
    context_object_name = "appointment"


class ActivateAppointment(View):
     def post(self, request, pk):
        appointment = get_object_or_404(Appointment, pk=pk, barber=request.user.barber_profile)
        appointment.status = "confirmed"
        appointment.save()
        return redirect("barber-dashboard")