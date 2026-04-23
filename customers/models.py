from django.db import models
from userauthentication.models import User
import uuid
from django.dispatch import receiver
# Create your models here.

NOTIFICATION_TYPE = (
    ("appointment scheduled", "appointment scheduled"),
    ("appointment cancelled", "appointment cancelled")
)

class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name="customer_profile")
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=100)
    id_document = models.FileField(upload_to="customer_documents/", null=True, blank=True)
    about = models.CharField(max_length=300, blank=True, null=True)
    profile_image = models.ImageField(upload_to="customersprofiles/", null=True, blank=True, default="images/userdefault.png")
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

class CustomerNotifications(models.Model):
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, null=True, blank=True, related_name="customer_notifications")
    appointment = models.ForeignKey("projectapp.Appointment", on_delete=models.CASCADE, null=True, blank=True,
        related_name="customer_appointment_notification")
    type = models.CharField(max_length=100, choices=NOTIFICATION_TYPE)
    seen = models.BooleanField(default=False)
    date = models.DateField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Notifications"
         
    def __str__(self):
        return f"Barber {self.customer.full_name} Notification"