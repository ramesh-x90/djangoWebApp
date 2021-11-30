from django.contrib import admin
from .models import Patient , Doctor, PatientToken
from rest_framework.authtoken.admin import TokenAdmin

# Register your models here.
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(PatientToken)


TokenAdmin.raw_id_fields = ['user']