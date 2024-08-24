from django.contrib import admin

from dentistry.models import Doctors, Services


@admin.register(Doctors)
class DoctorsAdmin(admin.ModelAdmin):
    list_display = ('doctors_name', 'specialization',)


@admin.register(Services)
class ServicesAdmin(admin.ModelAdmin):
    list_display = ('service_name',)
