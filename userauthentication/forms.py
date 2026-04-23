from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauthentication import models

class UserRegisterForm(UserCreationForm):
    full_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':"Full Name"}))
    email = forms.EmailField(widget=forms.TextInput(attrs={"placeholder":"example@gmail.com"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Enter Your password here..."}))
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Enter username"}))
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={
        "placeholder":"Confirm your password"
    }))
    class Meta:
        model = models.User
        fields = ["full_name", "email", "username", "password1"]
    
        
    # def __init__(self, *args, **kwargs):
    #     super(UserCreationForm, self).__init__(*args, **kwargs)
    
    #     for name, field in self.fields.items():
    #         field.widget.attrs.update({"class":"form-control"})

class UserLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder":"example@gmail.com"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Enter your password here..."}))