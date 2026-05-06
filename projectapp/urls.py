from django.urls import path
from projectapp import views

urlpatterns = [
    path("", views.HomePage.as_view(), name="home"),
    path("book-appointment/<str:service_id>/", views.BookAppointmentView.as_view(), name="book-appointment"),
    path("checkout/<str:billing_id>/", views.Checkout.as_view(), name="checkout"),
    path("reschedule/<str:appointment_id>", views.ReScheduleAppointment.as_view(), name="reschedule_appointment"),
    path("all-barber-services/", views.AllBarbersServices.as_view(), name="all-barbers-services"),
    path("allbarbers/", views.Allberbers.as_view(), name="allbarbers"),
    path("payment_status/<billing_id>/", views.PaymentStatus.as_view(), name="payment_status"),
    path("stripe_payment/<billing_id>/", views.Stripe_payment.as_view(), name="stripe_payment"),
    path("stripe_payment_verify/<billing_id>/", views.stripe_payment_verify.as_view(), name="stripe_payment_verify")
]

