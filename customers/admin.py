from django.contrib import admin
from customers import models
# Register your models here.

class CustomerAdmin(admin.ModelAdmin):
    list_display = ["full_name", "phone"]
    search_fields = ["CustomerProfile__user__username", "phone"]
admin.site.register(models.CustomerProfile, CustomerAdmin)

admin.site.register(models.CustomerNotifications)