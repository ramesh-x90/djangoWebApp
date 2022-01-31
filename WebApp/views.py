
# Create your views here.
from datetime import datetime, timedelta
from django.http import HttpRequest
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Patient, Doctor, PatientToken
from .serializers import PatientSerializer, DoctorSerializer, PatientLoginSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication


class DoctorsList(APIView):

    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        queryset = Doctor.objects.all()
        serializer_class = DoctorSerializer(queryset, many=True)
        return Response(serializer_class.data)


class PatientResister(APIView):

    permission_classes = [IsAuthenticated, ]
    
    def post(self, request):
        data = {}
        try:
            
            serialized_OBJ = PatientSerializer(data=request.data)

            if serialized_OBJ.is_valid(raise_exception=True):

                email = serialized_OBJ.validated_data.get('Email')
                serialized_OBJ.save()
                data["message"] = "Patient registered successfully"
                return Response(data, status=status.HTTP_200_OK)

        except Exception as e:
            data["error"] = e.__str__()
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


class PatientLogin(APIView):

    permission_classes = [IsAuthenticated, ]

    # authentication_classes = [user_auth]

    def post(self, request):

        data = {}

        try:
            serialized_OBJ = PatientLoginSerializer(data=request.data)

            if serialized_OBJ.is_valid(raise_exception=True):
                email = serialized_OBJ.validated_data.get('Email')
                pwd = serialized_OBJ.validated_data.get('Password')
                patient = Patient.objects.filter(Email=email)
                if patient.exists():
                    if patient.values('Password')[0]['Password'] == pwd:

                        token: PatientToken = None

                        while True:
                            try:
                                token, created = PatientToken.objects.update_or_create(
                                    user=patient.first())
                                break
                            except Exception as e:
                                print(e)

                        data['Token'] = token.key

                        return Response(
                            headers={
                                "Access-Control-Allow-Credentials" : "true",
                                "set-cookie" : f"Token={token.key};Domain=.healthcarewebapp.herokuapp.com;HttpOnly;secure;path=/"
                            },

                            data=data,

                            status=status.HTTP_200_OK)
                
                raise Exception('login failed' )

        except Exception as e:
            data['error'] = e.__str__()
            return Response( data , status=status.HTTP_400_BAD_REQUEST)
