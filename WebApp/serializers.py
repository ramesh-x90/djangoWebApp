from rest_framework import serializers
from  .models import Patient , Doctor


class PatientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Patient
        fields = ['Username' , 'Email' , 'Password' , 'BirthDate']

        extra_kwargs = {
            'Password' : {"write_only": True},
            'BirthDate' : {'required' : False},

        }


class PatientLoginSerializer(serializers.ModelSerializer):

    class Meta:
        model = Patient
        fields = [ 'Email' , 'Password' ]

        extra_kwargs = {
            'Password' : {"write_only": True},
            'Email' : {"validators": []},

        }


class DoctorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Doctor
        fields = [
            'doctorname' , 
            'email'  , 
            'hospitalname' ,
            'specialization' , 
            'charge',
            'starttime',
            'endtime'
        ]