import requests
from django.contrib.auth.models import Group, Permission
from users.models import User
from common_files.common_functions import get_host
from django.conf import settings
from rest_framework.response import Response
from rest_framework import generics, permissions
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status

import base64


# generating token with requested user to access API's


class GetToken(generics.CreateAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'username': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='User Name'
            ),
            'password': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='Password'
            )
        }
    ))
    def post(self, request, *args, **kwargs):
        print(request.data)
        # is_admin = request.data['is_admin']
        # is_console = request.data['is_console']
        # username = base64.b64decode(request.data['username']).decode()
        # password = base64.b64decode(request.data['password']).decode()

        username = request.data['username']
        password = request.data['password']

        data = {
            'grant_type': settings.GRANT_TYPE_PASSWORD,
            'username': username,
            'password': password,
            'client_id': settings.CLIENT_ID
        }
        token_url = 'http://{}/o/token/'.format(get_host(request))
        access_token_response = requests.post(token_url, data=data,
                                              verify=False,
                                              allow_redirects=False,
                                              auth=(settings.CLIENT_ID,
                                                    settings.CLIENT_SECRET))
        data = access_token_response.json()

        if data.get("error", "") != 'invalid_grant':
            data["id"] = request.user.id
            data["username"] = request.user.username
            data["is_staff"] = request.user.is_staff
            data["is_active"] = request.user.is_active
            data["is_superuser"] = request.user.is_superuser

        return Response(data)


# generate new token with expire token
class RefreshToken(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'token': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='Token'
            ),
        }
    ))
    def post(self, request, *args, **kwargs):
        data = {'grant_type': settings.GRANT_TYPE_REFRESH_TOKEN,
                'refresh_token': request.data['token'],
                'client_id': settings.CLIENT_ID,
                'client_secret': settings.CLIENT_SECRET
                }

        token_url = 'http://{}/o/token/'.format(get_host(request))
        refresh_token_response = requests.post(token_url, data=data, verify=False, allow_redirects=False,
                                               auth=(settings.CLIENT_ID, settings.CLIENT_SECRET))

        return Response(refresh_token_response.json())
