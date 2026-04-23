from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from customers.models import CustomerProfile

class CustomerProfileForm(ModelForm):
    class Meta:
        model = CustomerProfile
        exclude = ['user', "id", "is_verified"]
