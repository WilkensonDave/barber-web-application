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
from barbers.models import BarberProfile, Notifications
from customers.models import CustomerProfile, CustomerNotifications
from projectapp.models import Appointment, Service, Billing
from datetime import datetime, timedelta
from .utils import generate_time_slots, combine_date_time, calculate_extra_fee, SearchBarbers, paginateBarbers
from .forms import AppointmentForm, RescheduleForm
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.conf import settings
import stripe
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.utils.decorators import method_decorator
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
        custom_range, barbers = paginateBarbers(self.request, my_query, 6)
        context["barbers"] = barbers
        context["custom_range"] = custom_range
        context["search_query"] = self.request.GET.get("search_query", "")
        return context

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
                billing = Billing()
                billing.customer = appointment.customer
                billing.appointment = appointment
                billing.sub_total = appointment.service.price
                billing.tax = appointment.service.price*5/100
                billing.total = billing.sub_total + billing.tax + appointment.extra_fee
                billing.status = "Unpaid"
                billing.save()
            
            if payment_method == "online":
                return redirect("checkout", billing_id=billing.billing_id)
            return redirect("customer-dashboard")
        
        else:
            messages.error(request, "Please enter correct data. The one provided was invalid.")
            return redirect("book-appointment", service.id)

class Checkout(TemplateView):
    template_name = "project/checkout.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        billing_id = self.kwargs.get("billing_id")
        billing = get_object_or_404(Billing, billing_id=billing_id)
        context["billing"] = billing
        context["billing_id"] = billing_id
        context["stripe_public_key"] = settings.STRIPE_PUBLIC_KEY
        return context

#In understand this for to night.
#Continue stripe tomorrow and test session creation

@method_decorator(csrf_exempt, name="dispatch")
class Stripe_payment(View):
    def post(self, request, billing_id):
        billing = get_object_or_404(Billing, billing_id=billing_id, customer=request.user.customer_profile)
        stripe.api_key = settings.STRIPE_SECRET_KEY

        checkout_session = stripe.checkout.Session.create(
            customer_email=billing.customer.user.email,
            payment_method_types=['card'],    
            line_items=[
                { 
                    'price_data':{
                        'currency':"USD",
                        'product_data':{
                            'name':f"Appointment for {billing.customer.full_name}"
                        },
                        'unit_amount':int(billing.total * 100)
                    },
                    
                    'quantity':1
                }
            ],
            
            mode="payment",
            success_url=request.build_absolute_uri(reverse("stripe_payment_verify", args=[billing.billing_id])) + "?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=request.build_absolute_uri(reverse("stripe_payment_verify", args=[billing.billing_id])) + "?session_id={CHECKOUT_SESSION_ID}"
        )
        return JsonResponse({"sessionId":checkout_session.id})

class stripe_payment_verify(View):
    def get(self, request, billing_id):
        billing = Billing.objects.get(billing_id=billing_id)
        session_id=request.GET.get("session_id")
        session = stripe.checkout.Session.retrieve(session_id)
        
        if session.payment_status == "paid":
            if billing.status == "Unpaid":
                billing.status = "Paid"
                billing.save()
                billing.appointment.status = "confirmed"
                billing.appointment.payment_status = "paid"
                billing.appointment.save()
                
                Notifications.objects.create(
                    barber=billing.appointment.barber,
                    appointment=billing.appointment,
                    type="new appointment"
                )
                
                CustomerNotifications.objects.create(
                    customer=billing.appointment.customer,
                    appointment=billing.appointment,
                    type="appointment scheduled"
                )
            return redirect(f"/payment_status/{billing.billing_id}/?payment_status=paid")
        return redirect(f"/payment_status/{billing.billing_id}/?payment_status=failed")


class PaymentStatus(TemplateView):
    template_name = "project/payment-status.html"
    
    def get_context_data(self, **kwargs):
        context  = super().get_context_data(**kwargs)
        billing_id = self.kwargs.get("billing_id")
        billing = get_object_or_404(Billing, billing_id=billing_id)
        payment_status = self.request.GET.get("payment_status")
        context["billing"] = billing
        context["payment_status"] = payment_status
        return context


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
