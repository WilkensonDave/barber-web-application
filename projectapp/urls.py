from django.urls import path
from projectapp.views import HomePage, BookAppointmentView, CheckoutView, ReScheduleAppointment, AllBarbersServices, Allberbers

urlpatterns = [
    path("", HomePage.as_view(), name="home"),
    path("book-appointment/<str:service_id>/", BookAppointmentView.as_view(), name="book-appointment"),
    path("checkout/<str:appointment_id>/", CheckoutView.as_view(), name="checkout"),
    path("reschedule/<str:appointment_id>", ReScheduleAppointment.as_view(), name="reschedule_appointment"),
    path("all-barber-services/", AllBarbersServices.as_view(), name="all-barbers-services"),
    path("allbarbers/", Allberbers.as_view(), name="allbarbers")
]
