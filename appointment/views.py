from datetime import datetime, timedelta

from django.shortcuts import render
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
import json

from django.shortcuts import render, redirect
from django.views.generic import ListView

from dentistry.models import Doctors, Services
from .forms import AppointmentForm
from .models import Appointment


def create_appointment(request, doctor_id):
    doctor = Doctors.objects.get(id=doctor_id)
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user = request.user
            appointment.full_clean()
            appointment.save()
            return redirect('dentistry:services')
    else:
        initial_data = {'doctor': doctor}
        if request.user.is_authenticated:
            initial_data['name'] = request.user.first_name + ' ' + request.user.last_name
            initial_data['phone'] = request.user.phone
        form = AppointmentForm(initial=initial_data)
    return render(request, 'appointment/create_appointment.html', {'form': form})


class AppointmentList(ListView):
    model = Appointment
    template_name = 'appointment/appointment_list.html'
    context_object_name = 'appointments'

    def get_queryset(self):
        doctor_id = self.kwargs['doctor_id']
        date = self.request.GET.get('date')
        if date:
            date = datetime.strptime(date, '%Y-%m-%d').date()
        else:
            date = datetime.now().date()
        return Appointment.objects.filter(doctor__id=doctor_id, date=date)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['doctor'] = Doctors.objects.get(id=self.kwargs['doctor_id'])
        context['date'] = self.request.GET.get('date', datetime.now().date().strftime('%Y-%m-%d'))
        return context
