from django.urls import path
from django.views.decorators.cache import cache_page

from dentistry.apps import DentistryConfig
from dentistry.views import IndexView, AboutView, ServiceListView, ServiceCreateView, DoctorsListView, DoctorCreateView, \
    ServiceUpdateView, ServiceDeleteView, DoctorUpdateView, DoctorDeleteView

app_name = DentistryConfig.name

urlpatterns = [
    path('', cache_page(60)(IndexView.as_view()), name='base'),
    path('about/', cache_page(60)(AboutView.as_view()), name='about'),
    path('services_list/', cache_page(60)(ServiceListView.as_view()), name='services'),
    path('service_create/', ServiceCreateView.as_view(), name='services_create'),
    path('service_update/<int:pk>', ServiceUpdateView.as_view(), name='services_update'),
    path('service_delete/<int:pk>', ServiceDeleteView.as_view(), name='service_delete'),
    path('doctors_list/<int:specialization_id>/', cache_page(60)(DoctorsListView.as_view()), name='doctors_list'),
    path('doctors_create/<int:specialization_id>/', DoctorCreateView.as_view(), name='doctors_create'),
    path('doctors_update/<int:specialization_id>/<int:pk>', DoctorUpdateView.as_view(), name='doctor_update'),
    path('doctors_delete/<int:specialization_id>/<int:pk>', DoctorDeleteView.as_view(), name='doctor_delete'),
]
