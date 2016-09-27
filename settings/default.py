from uuid import uuid4
from os import environ

SECRET_KEY = uuid4().hex

# Grab OAuth parameters from environment
MEDIUM_CLIENT_ID = environ['MEDIUM_CLIENT_ID']
MEDIUM_CLIENT_SECRET = environ['MEDIUM_CLIENT_SECRET']
MEDIUM_REDIRECT_URI = environ['MEDIUM_REDIRECT_URI']

MEDIUM_SCOPE = 'basicProfile,publishPost'
MEDIUM_AUTHORIZATION_URL = 'https://medium.com/m/oauth/authorize'
MEDIUM_TOKEN_URL = '/v1/tokens'
