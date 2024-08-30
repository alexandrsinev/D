from django import forms
from django.forms import BooleanField

from dentistry.models import Feedback
from blog.models import Articles
from dentistry.models import Doctors, Services


class StileFormMixin():
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class FeedbackForm(StileFormMixin, forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'phone', 'message']


class DoctorsModeratorForm(StileFormMixin, forms.ModelForm):
    class Meta:
        model = Doctors
        fields = ('doctors_name', 'description_doctor', 'specialization', 'photo',)


class ServicesModeratorForm(StileFormMixin, forms.ModelForm):
    class Meta:
        model = Services
        fields = ('service_name', 'description', 'photo',)


class ArticlesModeratorForm(StileFormMixin, forms.ModelForm):
    class Meta:
        model = Articles
        fields = ('title', 'contents', 'preview',)
