from django.urls import path

from appointment.apps import AppointmentConfig
from . import views
from .views import AppointmentList

app_name = AppointmentConfig.name

urlpatterns = [
    path('create_appointment/<int:doctor_id>/', views.create_appointment, name='create_appointment'),
    path('appointment_list/<int:doctor_id>/', AppointmentList.as_view(), name='appointment_list'),
]
