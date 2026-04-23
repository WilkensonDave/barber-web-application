from django.db import models
from userauthentication.models import User
import uuid
from django.dispatch import receiver
from django.utils import timezone
from django.core.exceptions import ValidationError

NOTIFICATION_TYPE = (
    ("new appointment", "new appointment"),
    ("appointment cancelled", "appointment cancelled")
)
# Create your models here.
class BarberProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name="barber_profile")
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    shop_name = models.CharField(max_length=200)
    address = models.CharField(max_length=300) 
    phone = models.CharField(max_length=100)       
    id_document = models.FileField(upload_to="barber_documents/")
    headline = models.CharField(max_length=300, blank=True, null=True)
    biodata = models.TextField(null=True, blank=True)
    profile_image = models.ImageField(upload_to="barberprofiles/", null=True, blank=True, default="images/userdefault.png")
    social_twitter = models.CharField(max_length=2000, null=True, blank=True)
    social_linkedin = models.CharField(max_length=2000, null=True, blank=True)
    social_youtube = models.CharField(max_length=2000, null=True, blank=True)
    social_instagram = models.CharField(max_length=2000, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.full_name)
    
    class Meta:
        ordering = ["created", "full_name"]
    
    @property
    def profileImage(self):
        try:
            url = self.profile_image.url
        except:
            url = ""
        return url
    @property
    def num_appointment_completed(self):
        return self.barber_appointment.filter(status="completed").count()
    
class Notifications(models.Model):
    barber = models.ForeignKey(BarberProfile, on_delete=models.CASCADE, null=True, blank=True, related_name="barber_notifications")
    appointment = models.ForeignKey("projectapp.Appointment", on_delete=models.CASCADE, null=True, blank=True,
        related_name="barber_appointment_notification")
    type = models.CharField(max_length=100, choices=NOTIFICATION_TYPE)
    seen = models.BooleanField(default=False)
    date = models.DateField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Notifications"
         
    def __str__(self):
        return f"Barber {self.barber.full_name} Notification"


class Availability(models.Model):
    DAYS =[
        (0, "Monday"),
        (1, "Tuesday"),
        (2, "Wednesday"),
        (3, "Thursday"),
        (4, "Friday"),
        (5, "Saturday"),
        (6, "Sunday"),
    ]

    barber = models.ForeignKey(BarberProfile, on_delete=models.CASCADE, related_name="availabilities")
    day_of_week = models.IntegerField(choices=DAYS)
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    class Meta:
        unique_together = ("barber", "day_of_week")
    
    
class UnavailableDate(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    barber = models.ForeignKey(BarberProfile, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now, null=True, blank=True)
    reason = models.CharField(max_length=100, blank=True)