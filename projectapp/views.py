from django.shortcuts import render, redirect
from django.http import request
from userauthentication import models
from django.views import View
from django.views.generic.edit import CreateView
from django.views.generic import UpdateView, ListView, TemplateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from userauthentication.models import User
from django.contrib.auth.views import LoginView, LogoutView
from barbers.forms import BarberProfileForm
from barbers.models import BarberProfile
from customers.models import CustomerProfile
from projectapp.models import Appointment, Service
from datetime import datetime, timedelta
from .utils import generate_time_slots, combine_date_time, calculate_extra_fee, SearchBarbers, paginateBarbers
from .forms import AppointmentForm, RescheduleForm
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
# Create your views here.

class HomePage(ListView):
    model = BarberProfile
    template_name = "project/index.html"
    context_object_name = "barbers"
    
    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get("search_query")
        return SearchBarbers(queryset, query)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        my_query = context["barbers"]
        custom_range, barbers = paginateBarbers(self.request, my_query, 1)
        context["barbers"] = barbers
        context["custom_range"] = custom_range
        context["search_query"] = self.request.GET.get("search_query", "")
        return context

class CheckoutView(TemplateView):
    template_name = "project/checkout.html"


class BookAppointmentView(View):
    def get(self, request, service_id):
        service = Service.objects.get(id=service_id)
        form = AppointmentForm()
        return render(request, "project/book-appointment.html", {"service":service, "form":form})
    
    def post(self, request, service_id):
        service = Service.objects.get(id=service_id)
        barber = service.owner
        form = AppointmentForm()
        date = request.POST.get("date")
        time = request.POST.get("time")
        
        if date and not time:
            slots = generate_time_slots(barber, service, date)
            return render(request, "project/book-appointment.html", {
                "form":form,
                "slots":slots,
                "selected_date":date,
                "service":service,
                "barber":barber
            })
        
        if date and time:
            booking_type = request.POST.get("booking_type")
            extra_fee = calculate_extra_fee(booking_type)
            booking_type = booking_type
            payment_method = request.POST.get("payment_type")
            address = request.POST.get("address")
            appointment_time = combine_date_time(date, time)
            appointment = Appointment.objects.create(
                appointment_time=appointment_time,
                customer=request.user.customer_profile,
                barber=barber,
                service=service,
                address=address if booking_type=="home" else None,
                payment_method=payment_method,
                extra_fee = extra_fee,
                status="confirmed" if payment_method=="cash" else "pending"
            )
            appointment.save()

            if payment_method == "online":
                return redirect("checkout", appointment.id)
                
            print(request.POST)
            return redirect("home")
        
        else:
            messages.error(request, "Please enter correct data. The one provided was invalid.")
            print("error")
            return redirect("book-appointment", service.id) 


class ReScheduleAppointment(UpdateView):
    model = Appointment
    form_class = RescheduleForm
    template_name = "project/reschedule.html"
    
    def get_object(self):
        return get_object_or_404(Appointment, 
            id=self.kwargs.get("appointment_id"),
            customer=self.request.user.customer_profile
        )
    
    def get_success_url(self):
        return reverse_lazy("customer-dashboard")

class AllBarbersServices(ListView):
    model = Service
    ordering = ["-id"]
    template_name = "project/all-project-services.html"
    context_object_name = "services"


class Allberbers(ListView):
    model = BarberProfile
    ordering = ["full_name"]
    template_name = "project/barbers.html"
    context_object_name = "barbers"
