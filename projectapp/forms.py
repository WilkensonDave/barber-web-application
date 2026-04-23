from django.forms import ModelForm
from .models import Appointment
from django import forms


class AppointmentForm(ModelForm):
    class Meta:
        model = Appointment
        fields = ["booking_type", "payment_method", "address"]

class RescheduleForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ["appointment_time"]