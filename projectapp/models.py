from django.db import models
from userauthentication.models import User
from barbers.models import BarberProfile
from customers.models import CustomerProfile
import uuid
from django.dispatch import receiver
from shortuuid.django_fields import ShortUUIDField
from django.utils import timezone
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Service(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    owner = models.ForeignKey(BarberProfile, on_delete=models.CASCADE, null=True, blank=True, related_name="services")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    duration = models.IntegerField(help_text="Duration in minutes")
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

class Appointment(models.Model):
    STATUS = [
        ("pending", "pending"),
        ("completed", "completed"),
        ("confirmed", "comfirmed"),
        ("cancelled", "cancelled"),
    ]
    
    PAYMENT_METHOD = [
    ('online', 'online'),
    ('cash', 'cash'),
    ]
    
    PAYMENT_STATUS = [
        ("unpaid", "unpaid"),
        ("paid", "paid"),
    ]
    
    BoOKING_TYPE = [
        ("shop", "At Shop"),
        ("home", "Home Service")
    ]
    
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    barber = models.ForeignKey(BarberProfile, on_delete=models.CASCADE, related_name="barber_appointment")
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, related_name="customer_appointment")
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    appointment_time = models.DateTimeField()
    payment_method = models.CharField(max_length=100, choices=PAYMENT_METHOD, default="online")
    status = models.CharField(max_length=100, choices=STATUS, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    booking_type = models.CharField(max_length=10, choices=BoOKING_TYPE, default="shop")
    extra_fee =  models.DecimalField(max_digits=6, decimal_places=2, default=0)
    address = models.CharField(max_length=255, blank=True, null=True)
    payment_status = models.CharField(max_length=255, choices=PAYMENT_STATUS, default="unpaid")
    
    def __str__(self):
        return f"{self.customer.full_name} with {self.barber.full_name} at - {self.appointment_time}"

    @property
    def is_valid(self):
        return((self.status=="pending" and self.payment_method=="cash")
        or self.status == "confirmed" or self.status=="pending")

class Billing(models.Model):
    STATUS = [
        ("pending", "Pending"),
        ("succeeded", "Succeeded"),
        ("failed", "Failed"),
    ]
    
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    customer = models.ForeignKey(CustomerProfile, on_delete=models.SET_NULL, 
        null=True, blank=True, related_name="customer_billing")
    stripe_payment_intent = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, 
        blank=True, null=True, related_name="payments")
    sub_total = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    billing_id = ShortUUIDField(length=6, max_length=10, alphabet="1234567890")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Billing for {self.customer.full_name} - Total: {self.total}"

