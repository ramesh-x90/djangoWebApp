import binascii
from datetime import datetime, timedelta
import os
from re import T
from django.db import models
from django.core.validators import RegexValidator


# Create your models here.
alphanumeric = RegexValidator(
    r"^[\w @\.\-,/]+$", message="Contains some prohibited symbols")


class Patient(models.Model):
    Username = models.CharField(max_length=20, validators=[alphanumeric])
    Email = models.EmailField(max_length=100, unique=True)
    Password = models.CharField(max_length=50, validators=[alphanumeric])
    BirthDate = models.DateField(blank=True, null=True)


class Doctor(models.Model):
    doctorname = models.CharField(max_length=20, validators=[alphanumeric])
    email = models.EmailField(max_length=100, validators=[
                              alphanumeric], unique=True)
    password = models.CharField(max_length=100, validators=[alphanumeric])
    hospitalname = models.CharField(max_length=50, validators=[alphanumeric])
    specialization = models.CharField(
        max_length=100, validators=[alphanumeric])
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
