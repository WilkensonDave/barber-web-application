from django.urls import path
from barbers import views

urlpatterns = [
    path("barber_profile/", views.BarberProfileView.as_view(), name="barber_profile"),
    path("create-service/", views.CreateServiceView.as_view(), name="create-service"),
    path("dashboard/", views.BarberDashBoard.as_view(), name="barber-dashboard"),
    path("allservices/", views.AllServices.as_view(), name="all-services"),
    path("accept-appointment/<str:pk>/", views.AcceptAppointment.as_view(), name="accept-appointment"),
    path("cancel-appointment/<str:pk>/", views.CancelAppointment.as_view(), name="cancel-appointment"),
    path("mark-appointments-completed/<str:pk>/", views.MarkAppointmentCompleted.as_view(), name="mark-appointment-completed"),
    path("notification-seen/<str:pk>/", views.NotificationSeeen.as_view(), name="notification-seen"),
    path("all-notifications/", views.AllNotifications.as_view(), name="all-notifications"),
    path("barber-details/<str:pk>/", views.BarberDetails.as_view(), name="barber-details"),
    path("appointments/", views.BarberAppointments.as_view(), name="barber-appointments"),
    path("create-timeslots/", views.CreateTimeSlots.as_view(), name="create-timeslots"),
    path("barber-schedule/", views.BarberSchedule.as_view(), name="barber-schedule"),
    path("update-schedule/<str:pk>", views.UpdateSchedule.as_view(), name="update-schedule"),
    path("appointment-details/<str:pk>/", views.BarberAppointmentDetails.as_view(), name="barber-appointment-details"),
    path("activateappointment/<str:pk>/", views.ActivateAppointment.as_view(), name="activate-appointment")
]
