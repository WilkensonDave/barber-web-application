from django.urls import path
from customers import views


urlpatterns = [
    path("customer_profile/", views.CustomerProfileView.as_view(), name="customer_profile"),
    path("dashboard/", views.CustomerDashBoard.as_view(), name="customer-dashboard"),
    path("cancel-appointment/<str:appointment_id>/", views.CustomerCancelAppointment.as_view(), name="customer-cancel-appointment"),
    path("all-notifications/", views.AllNotifications.as_view(), name="customer-all-notifications"),
    path("notification-seen/<str:pk>/", views.NotificationSeeen.as_view(), name="customer-notification-seen"),
    path("customer-reactivate-appointment/<str:appointment_id>/", views.CustomerReactivateAppointment.as_view(), 
        name="customer-reactivate-appointment"),
    path("customer-appointment-details/<str:pk>/", views.CustomerAppointmentDetails.as_view(), name="customer-appointment-details"),
    path("customer-appointments/", views.CustomerAppointments.as_view(), name="customer-appointments")
]
