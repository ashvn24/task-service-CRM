from django.urls import path
from .views import AppointmentsListCreate

urlpatterns = [
    path('appointments/', AppointmentsListCreate.as_view(), name='appointments-list-create'),
]
