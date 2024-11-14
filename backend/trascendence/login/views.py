from django.shortcuts import render
from rest_framework import generics, status
from .models import User, CustomToken, CustomTokenAuthentication
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, UserSerializer42
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.http import JsonResponse, HttpResponse
from rest_framework.parsers import JSONParser
from rest_framework.authtoken.models import Token
from rest_framework.settings import api_settings
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework import authentication
from rest_framework import exceptions
import requests
import os
from requests.auth import HTTPBasicAuth
from django.utils.crypto import get_random_string

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"response": "successful"})
        else:
            return Response({"response": "failed"})


class LoginView(APIView):
    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        if not username or not password:
            return Response({"detail": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST) 
        if '#' in username:  
            return Response({"detail": "Invalid username"}, status=status.HTTP_400_BAD_REQUEST)
        authenticate_user = authenticate(username=username, password=password)
        if authenticate_user is not None:
            user = User.objects.get(username=username)
            serializer = UserSerializer(user)

            response_data = {
                "user": serializer.data
            }

            token, created = CustomToken.objects.get_or_create(user=user)
            user.status = True
            user.save()
            response = Response({"response": "successful", "token": token.key, "user": response_data})
            return response
        return Response({"detail": "Invalid credentials"})


@api_view(['POST'])  
@authentication_classes([SessionAuthentication, CustomTokenAuthentication])
@permission_classes([IsAuthenticated])
def Info(request):
	user = request.user
	serializer = UserSerializer(user)
	token = CustomToken.objects.get(user=user)
	return Response({"user": serializer.data,"token" : token.key})

@api_view(['GET'])  
@authentication_classes([SessionAuthentication, CustomTokenAuthentication])
@permission_classes([IsAuthenticated])
def friends_info(request):
    user = request.user
    pal = request.data['friend']
    if not pal:
        return Response({"error": "Friend username is required"}, status=400)
    friends = user.friendlist.all()
    if not friends.filter(username=pal).exists():
        return Response({"error": "You are not friends with this user"}, status=400)
    pal_info = User.objects.get(username=pal)
    pal_serializer = FriendSerializer(pal_info)
    return Response({"pal": pal_serializer.data}, status=200)

@api_view(['POST'])
@authentication_classes([SessionAuthentication, CustomTokenAuthentication])
@permission_classes([IsAuthenticated])
def logout(request):
    user = request.user
    user.status = False
    user.save()
    return Response({"detail": "You are logged out"})



@api_view(['GET'])
def get_42token(request):
    data = {
        'grant_type': 'authorization_code',
        'client_id': os.getenv('CLIENT_ID'),
        'client_secret': os.getenv('CLIENT_SECRET'),
        'code': request.GET.get('code'),
        'redirect_uri': 'https://localhost:8443/spa-manager.html',
    }
    response = requests.post('https://api.intra.42.fr/oauth/token', json=data)
    token_data = response.json()
    if response.status_code == 200:
        response2 = requests.get('https://api.intra.42.fr/v2/me', headers={'Authorization': 'Bearer ' + token_data['access_token']})
        username = response2.json()['login'] + '#42'
        token42 = token_data['access_token']
        if not User.objects.filter(username=username).exists():
            serializer = UserSerializer42(data={'username': username, 'password': get_random_string(length=40)})
            if serializer.is_valid(raise_exception=True):
                user = serializer.save()
                response_data = {
                    "user": serializer.data
                }
                token, created = CustomToken.objects.get_or_create(user=User.objects.get(username=username))
        else:
            user = User.objects.get(username=username)
            response_data = {
                "user": UserSerializer42(user).data
            }
            token, created = CustomToken.objects.get_or_create(user=user, defaults={'key': token42})
        user.status = True
        user.save()    
        return JsonResponse({'token': token.key, 'user': response_data})
    else:
        return JsonResponse({'error': 'Failed to get access token'}, status=400)
        