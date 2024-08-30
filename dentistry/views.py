from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView

from config import settings
from dentistry.forms import DoctorsModeratorForm, ServicesModeratorForm, FeedbackForm
from dentistry.models import Doctors, Services, Feedback


class IndexView(View):
    model = Doctors

    def get(self, request):
        form = FeedbackForm()
        return render(request, 'dentistry/base.html', {'form': form})

    def post(self, request):
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            next_url = request.POST.get('next', '/')
            return redirect(next_url)
        else:
            return render(request, 'dentistry/index.html', {'form': form})


class AboutView(View):

    def get(self, request):
        return render(request, 'dentistry/about.html')


class ServiceListView(ListView):
    model = Services

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        return queryset


class ServiceCreateView(CreateView):
    model = Services
    form_class = ServicesModeratorForm
    template_name = 'dentistry/services_form.html'
    success_url = reverse_lazy('dentistry:services')

    def form_valid(self, form):
        if form.is_valid():
            new_object = form.save()
            new_object.save()

        return super().form_valid(form)


# Контроллер для редактирования услуги
class ServiceUpdateView(UpdateView):
    model = Services
    form_class = ServicesModeratorForm
    success_url = reverse_lazy('dentistry:services')


# Контроллер для удаления услуги
class ServiceDeleteView(DeleteView):
    model = Services
    success_url = reverse_lazy('dentistry:services')


class DoctorsListView(ListView):
    model = Doctors
    template_name = 'dentistry/doctors_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        specialization_id = self.kwargs.get('specialization_id')
        if specialization_id:
            queryset = queryset.filter(specialization_id=specialization_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        specialization_id = self.kwargs.get('specialization_id')
        if specialization_id:
            service = Services.objects.get(id=specialization_id)
            context['service_name'] = service.service_name
            context['specialization_id'] = service.id
        return context


class DoctorCreateView(CreateView):
    model = Doctors
    form_class = DoctorsModeratorForm
    success_url = reverse_lazy('dentistry:doctors_list')

    def form_valid(self, form):
        specialization_id = self.kwargs.get('specialization_id')
        if specialization_id is None:
            raise ValueError("Specialization ID is required")

        # Добавляем specialization_id в данные формы
        form.instance.specialization_id = specialization_id
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        specialization_id = self.kwargs.get('specialization_id')
        if specialization_id:
            service = Services.objects.get(id=specialization_id)
            context['specialization_id'] = service.id
        return context

    def get_success_url(self):
        specialization_id = self.kwargs['specialization_id']
        return reverse('dentistry:doctors_list', kwargs={'specialization_id': specialization_id})


# Контроллер для редактирования врача
class DoctorUpdateView(UpdateView):
    model = Doctors
    form_class = DoctorsModeratorForm
    success_url = reverse_lazy('dentistry:doctors_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        specialization_id = self.kwargs.get('specialization_id')
        if specialization_id:
            service = Services.objects.get(id=specialization_id)
            context['specialization_id'] = service.id
        return context

    def get_success_url(self):
        specialization_id = self.kwargs['specialization_id']
        return reverse('dentistry:doctors_list', kwargs={'specialization_id': specialization_id})


# Контроллер для удаления врача
class DoctorDeleteView(DeleteView):
    model = Doctors
    success_url = reverse_lazy('dentistry:doctors_list')

    def get_success_url(self):
        specialization_id = self.kwargs['specialization_id']
        return reverse('dentistry:doctors_list', kwargs={'specialization_id': specialization_id})


class FeedbackListView(ListView):
    model = Feedback


class FeedbackDetailView(DetailView):
    model = Feedback


class ContactsView(View):

    def get(self, request):
        return render(request, 'dentistry/contact.html')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['YANDEX_MAPS_API_KEY'] = settings.YANDEX_MAPS_API_KEY
        return context
