from django import forms

from appointment.models import Appointment
from dentistry.forms import StileFormMixin


class AppointmentForm(StileFormMixin, forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'name', 'phone', 'date', 'time']

    def __init__(self, *args, **kwargs):
        super(AppointmentForm, self).__init__(*args, **kwargs)
        self.fields['date'].widget = forms.DateInput(attrs={'type': 'date'})
        time_slots = [(f"{hour:02d}:00", f"{hour:02d}:00") for hour in range(9, 18)]
        date = kwargs.get('instance').date if kwargs.get('instance') else None

        if date:
            # Получение занятых слотов для выбранной даты
            occupied_slots = Appointment.objects.filter(date=date).values_list('time', flat=True)
            # Исключение занятых слотов из списка доступных
            available_slots = [(slot[0], slot[1]) for slot in time_slots if slot[0] not in occupied_slots]
        else:
            available_slots = time_slots
        self.fields['time'] = forms.ChoiceField(choices=available_slots)

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        time = cleaned_data.get('time')

        if date and time:
            existing_appointments = Appointment.objects.filter(date=date, time=time)
            if self.instance.pk:
                existing_appointments = existing_appointments.exclude(pk=self.instance.pk)
            if existing_appointments.exists():
                raise forms.ValidationError("Это время занято")

        return cleaned_data
