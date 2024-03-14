from urllib.parse import urlencode
from rest_framework import serializers, status
from rest_framework.views import APIView
from django.conf import settings
from django.shortcuts import redirect
from django.shortcuts import redirect
from rest_framework.response import Response
from .google import google_get_access_token, google_get_user_info, generate_tokens_for_user
from .models import User
from .serializers import UserSerializer



class GoogleLoginAPIView(APIView):
    class InputSerializer(serializers.Serializer):
        code = serializers.CharField(required=False)
        error = serializers.CharField(required=False)
    
    def get(self, request, *args, **kwargs):
        input_serializer = self.InputSerializer(data=request.GET)
        input_serializer.is_valid(raise_exception=True)

        code = input_serializer.validated_data.get('code')
        error = input_serializer.validated_data.get('error')
        login_url = f'{settings.BASE_FRONTEND_URL}'

        if error or not code:
            params = urlencode({'error': error})
            return redirect(f'{login_url}?{params}')

        redirect_uri = f'{settings.BASE_FRONTEND_URL}/google'
        access_token = google_get_access_token(code=code, redirect_uri=redirect_uri)

        user_data = google_get_user_info(access_token=access_token)

        try:
            user = User.objects.get(email=user_data['email'])
            access_token, refresh_token = generate_tokens_for_user(user)
            context = {
                'user': UserSerializer(user).data,
                'access_token': str(access_token),
                'refresh_token': str(refresh_token),
            }
            return Response(context, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            first_name = user_data.get('given_name', '')
            last_name = user_data.get('family_name', '')
            user = User.objects.create(
                email=user_data['email'],
                first_name=first_name,
                last_name=last_name
            )

            access_token, refresh_token = generate_tokens_for_user(user)
            context = {
                'user': UserSerializer(user).data,
                'access_token': str(access_token),
                'refresh_token': str(refresh_token)
            }
            return Response(context, status=status.HTTP_200_OK)


# from django.http import JsonResponse
# from rest_framework.permissions import AllowAny
# from google.oauth2 import id_token
# from google.auth.transport import requests
# from rest_framework.views import APIView
# from .serializers import SocialSerializer, TokenValidateSerializer
# import os
# from django.contrib.auth import authenticate
# import uuid
# from rest_framework.response import Response
# from rest_framework import status

# def my_random_string(string_length=10):
#     """Returns a random string of length string_length."""
#     random = str(uuid.uuid4())  # Convert UUID format to a Python string.
#     random = random.lower()  # Make all characters uppercase.
#     random = random.replace("-", "")  # Remove the UUID '-'.
#     #usage  = '%s-%s'%('TR',my_random_string(6))
#     return random[0:string_length]  


# class SocialSignView(APIView):
#     permission_classes = (AllowAny,)
#     serializer_class = SocialSerializer

#     def validate_user(token):
#         try:
#             # Specify the CLIENT_ID of the app that accesses the backend:
#             idinfo = id_token.verify_oauth2_token(token, requests.Request(), os.environ['CLIENT_ID'])

#             # Or, if multiple clients access the backend server:
#             # idinfo = id_token.verify_oauth2_token(token, requests.Request())
#             # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
#             #     raise ValueError('Could not verify audience.')

#             # If auth request is from a G Suite domain:
#             # if idinfo['hd'] != GSUITE_DOMAIN_NAME:
#             #     raise ValueError('Wrong hosted domain.')

#             # ID token is valid. Get the user's Google Account ID from the decoded token.
#             userid = idinfo['sub']
#             print("fdfd", userid)
#             print("fdwwe", idinfo)
#             return userid
#         except Exception as e:
#             return 'token is invalid ppp,' + e

#     # Create your views here.
#     def post (self, request, *args, **kwargs):

#         serializer = TokenValidateSerializer(data=request.data)
#         if serializer.is_valid():
#             try:
#                 user_data = self.validate_user(serializer.data['access_token'])
#                 try:
#                     user = User.objects.get(email=serializer.data['email'].replace(" ", "").lower())

#                 except User.DoesNotExist:
#                     user = User.objects.create(
#                         username=serializer.data['given_name'],
#                         email=serializer.data['email'],
#                         first_name=serializer.data['given_name'],
#                         last_name=serializer.data['family_name'],
#                     )
#                 password = my_random_string(10)
#                 log_user = authenticate(username=user.username, password=password)
#                 return Response(content, status=status.HTTP_200_OK)
                
#             except Exception as e:
#                 return Response({'message': 'Something went wrong!' + e})
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)