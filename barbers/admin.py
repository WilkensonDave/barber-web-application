from django.contrib import admin
from barbers import models
# Register your models here.

class BarberAdmin(admin.ModelAdmin):
    list_display = ["full_name", "address", "phone"]
    search_fields = ["BarberProfile__user__username", "address", "phone"]


admin.site.register(models.Notifications)
admin.site.register(models.BarberProfile, BarberAdmin)
admin.site.register(models.UnavailableDate)
admin.site.register(models.Availability)