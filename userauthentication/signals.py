from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import User
from customers.models import CustomerProfile
from barbers.models import BarberProfile
from django.core.mail import send_mail
from django.conf import settings


def createProfile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type =="barber":
            BarberProfile.objects.create(user=instance)
        
        elif instance.user_type == "customer":
            CustomerProfile.objects.create(user=instance)


def delete_barberprofile(sender, instance, **kwargs):
    try:
        user = instance.user
        user.delete()
    except:
        pass

def delete_customerprofile(sender, instance, **kwargs):
    try:
        user = instance.user
        user.delete()
    except:
        pass

post_save.connect(createProfile, sender=User)
post_delete.connect(delete_barberprofile, sender=BarberProfile)
post_delete.connect(delete_customerprofile, sender=CustomerProfile)