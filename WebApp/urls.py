from django.urls import include, path
from rest_framework import routers
from . import views


urlpatterns = [
    path('DoctorsList/', views.DoctorsList.as_view()),
    path('Patient/Register/', views.PatientResister.as_view()),
    path('Patient/Login/', views.PatientLogin.as_view()),
]