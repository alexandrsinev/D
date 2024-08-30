from django.db import models

from dentistry.models import Doctors
from users.models import Users

NULLABLE = {'blank': True, 'null': True}


class Appointment(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    doctor = models.ForeignKey(Doctors, on_delete=models.CASCADE)
    date = models.DateField(**NULLABLE)
    time = models.TimeField(**NULLABLE)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, **NULLABLE)

    def __str__(self):
        return f"{self.name} - {self.doctor} - {self.date} {self.time}"

    @staticmethod
    def get_booked_slots(doctor, date):
        booked_slots = Appointment.objects.filter(doctor=doctor, date=date).values_list('time', flat=True)
        return list(booked_slots)
