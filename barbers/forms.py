from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from barbers.models import BarberProfile, Availability
from projectapp.models import Service
from django import forms
from django.core.exceptions import ValidationError

class BarberProfileForm(ModelForm):
    class Meta:
        model = BarberProfile
        exclude = ['user', "id", "is_verified"]

class ServiceForm(ModelForm):
    class Meta:
        model = Service
        exclude = ["id", "owner", ""]

class  timeSlotsForm(forms.ModelForm):
    def __init__(self, *args, barber=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.barber = barber
        
    class Meta:
        model = Availability
        exclude = ["barber"]
        widgets = {
            "start_time":forms.TimeInput(attrs={"type":"time"}),
            "end_time":forms.TimeInput(attrs={"type":"time"}),
        }
    
    
    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get("start_time")
        end = cleaned_data.get("end_time")
        barber = self.barber
        day = cleaned_data.get("day_of_week")
        
        
        if start and end and start >= end:
            raise forms.ValidationError("End time must be after the start time")
        
        
        if barber and day is not None:
            exists = Availability.objects.filter(
                barber=barber, day_of_week=day
            )
            
            if self.instance.pk:
                exists.exclude(pk=self.instance.pk)
            
            if exists.exists():
                raise forms.ValidationError("You have already created a schedule for this day.")
        return cleaned_data
        
        
                
