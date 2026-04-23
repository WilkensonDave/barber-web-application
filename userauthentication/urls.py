from django.urls import path
from userauthentication.views import BarberRegisterView, CustomerRegisterView, CustomLoginView, CustomLogoutView
from . import views

urlpatterns = [
    path("register_barber/", BarberRegisterView.as_view(), name="barber_registration"),
    path("register_user/", CustomerRegisterView.as_view(), name="customer_registration"),
    path("login/", CustomLoginView.as_view(), name="user_login"),
    path("logout/", CustomLogoutView.as_view(), name='logout')
]
