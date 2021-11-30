from WebApp.models import patientToken
from rest_framework.authentication import TokenAuthentication



class user_auth(TokenAuthentication):
    model = patientToken
