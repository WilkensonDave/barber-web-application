from django.contrib import admin
from projectapp import models
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ["name"]


admin.site.register(models.Category,CategoryAdmin)
admin.site.register(models.Service)
admin.site.register(models.Appointment)
admin.site.register(models.Billing)

