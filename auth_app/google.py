import requests
from django.conf import settings
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


GOOGLE_ID_TOKEN_INFO_URL = 'https://www.googlesapi.com/oauth2/v3/tokeninfo'
GOOGLE_ACCESS_TOKEN_OBTAIN_URL = 'https://oauth2.googleapis.com/token'
GOOGLE_USER_INFO_URL = 'https://www.googleapis.com/oauth/v3/userinfo'

def generate_tokens_for_user(user):
    '''
    generate access and refresh tokens for the given user
    '''
    serialzer = TokenObtainPairSerializer()

    token_data = serialzer.get_token(user)
    access_token = token_data.access_token
    refresh_token = token_data

    return access_token, refresh_token

def google_get_access_token(code, redirect_uri):
    data = {
        'code': code,
        'client_id': settings.CLIENT_ID,
        'client_secret': settings.CLIENT_SECRET,
        'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code'
    }

    response = requests.post(GOOGLE_ACCESS_TOKEN_OBTAIN_URL, data=data)

    if not response.ok:
        print(response.content)
        raise ValidationError('Failed to obtain access token from Google.')

    access_token = response.json()['access_token']
    return access_token

def google_get_user_info(access_token):
    response = requests.get(
        GOOGLE_USER_INFO_URL, 
        params={'access_token': access_token}
    )

    if not response.ok:
        raise ValidationError('Failed to obtain user info from Google')
    
    return response.json()

