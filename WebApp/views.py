
# Create your views here.
import datetime
from datetime import timedelta
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
        try:
            data = {}
            serialized_OBJ = PatientSerializer(data=request.data)

            if serialized_OBJ.is_valid(raise_exception=True):

                email = serialized_OBJ.validated_data.get('Email')
                if Patient.objects.filter(Email=email).exists():
                    return Response({'error': 'email already exists'}, status=status.HTTP_400_BAD_REQUEST)
                serialized_OBJ.save()
                data["message"] = "Patient registered successfully"
                return Response(data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(f'error: {e}', status=status.HTTP_400_BAD_REQUEST)


class PatientLogin(APIView):

    permission_classes = [IsAuthenticated, ]

    # authentication_classes = [user_auth]

    def post(self, request):

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

                        return Response(
                            headers={
                                "Set-Cookie": f"Token={token.key};Domain=.healthcarewebappsltcpro.herokuapp.com;HttpOnly;Expires={datetime.now()+timedelta(days=10)}"
                            },
                            data={
                                'Token': token.key
                            },
                            status=status.HTTP_200_OK)

                return Response('login failed', status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(f'error: {e}', status=status.HTTP_400_BAD_REQUEST)
