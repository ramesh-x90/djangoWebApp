import binascii
from datetime import datetime, timedelta
import os
from re import T
from django.db import models

# Create your models here.


class Patient(models.Model):
    Username = models.CharField(max_length=20)
    Email = models.EmailField(max_length=100)
    Password = models.CharField(max_length=50)
    BirthDate = models.DateField(blank=True, null=True)


class Doctor(models.Model):
    doctorname = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
    hospitalname = models.CharField(max_length=50)
    specialization = models.CharField(max_length=100)
    charge = models.PositiveIntegerField()
    starttime = models.TimeField(auto_now=False, auto_now_add=False)
    endtime = models.TimeField(auto_now=False, auto_now_add=False)

    def __str__(self) -> str:
        return self.doctorname


class PatientToken(models.Model):
    key = models.CharField(unique=True, max_length=100)
    user = models.OneToOneField(
        Patient,
        on_delete=models.CASCADE,
    )
    exdate = models.DateTimeField(
        auto_now_add=True
    )

    def save(self, *args, **kwargs):
        self.key = self.generate_key()
        return super(PatientToken, self).save(*args, **kwargs)

    def generate_key(self):
        return binascii.hexlify(os.urandom(50)).decode()

    def __str__(self):
        return self.key
