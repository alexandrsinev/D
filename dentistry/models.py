from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Services(models.Model):
    service_name = models.CharField(max_length=250, verbose_name='Вид лечения')
    description = models.TextField(verbose_name='Описание')
    photo = models.ImageField(upload_to='service_photo/', verbose_name='Фото вида лечения', **NULLABLE)

    def __str__(self):
        return f'{self.service_name}'

    class Meta:
        verbose_name = 'Вид лечения'
        verbose_name_plural = 'Виды лечения'


class Doctors(models.Model):
    doctors_name = models.CharField(max_length=250, verbose_name='Имя врача')
    specialization = models.ForeignKey(Services, on_delete=models.CASCADE, verbose_name='Специализация')
    description_doctor = models.TextField(verbose_name='Описание', **NULLABLE)
    photo = models.ImageField(upload_to='doctors_photo/', verbose_name='Фото врача', **NULLABLE)

    def __str__(self):
        return f'{self.doctors_name}'

    class Meta:
        verbose_name = 'Врач'
        verbose_name_plural = 'Врачи'
