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
from dotenv import load_dotenv

# Carica le variabili d'ambiente dal file .env
load_dotenv()

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
    try:
        code = request.GET.get('code')
        if not code:
            return JsonResponse({'error': 'Nessun codice fornito'}, status=400)
            
        # Ottieni le credenziali dal file .env
        # Nota: Rimuovi gli apici singoli e gli spazi dai valori
        client_id = os.getenv('CLIENT_ID', '').strip().strip("'")
        client_secret = os.getenv('CLIENT_SECRET', '').strip().strip("'")
        
        if not client_id or not client_secret:
            print("Credenziali non trovate nel file .env, uso valori hardcoded")
            client_id = "u-s4t2ud-a8a7afc615b7c393b1a141953798a4f72bfd49e80f8464df3f2ac1838557eefe"
            client_secret = "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"
        
        # Configura i dati per la richiesta a 42
        data = {
            'grant_type': 'authorization_code',
            'client_id': client_id,
            'client_secret': client_secret,
            'code': code,
            'redirect_uri': 'https://localhost:8443/spa-manager.html',
        }
        
        # Debug per la richiesta
        print(f"Configurazione client 42 - ID: {client_id}")
        print(f"Client Secret: {client_secret[:10]}... (primi 10 caratteri)")
        print(f"Codice ricevuto dalla 42: {code}")
        print("URI di redirect: https://localhost:8443/spa-manager.html")
        
        # Prova a ottenere il token da 42
        print("Invio richiesta a 42 API per token...")
        try:
            # Usa form data invece di JSON
            response = requests.post(
                'https://api.intra.42.fr/oauth/token', 
                data=data
            )
            print(f"Risposta da 42 API: Status {response.status_code}")
            print(f"Corpo risposta: {response.text}")
        except Exception as e:
            print(f"Errore nella richiesta a 42 API: {str(e)}")
            return JsonResponse({'error': f"Errore di connessione a 42 API: {str(e)}"}, status=500)
        
        if response.status_code != 200:
            return JsonResponse({'error': f"Errore nella risposta da 42 API: {response.text}"}, status=400)
        
        # Estrai il token dalla risposta
        try:    
            token_data = response.json()
            access_token = token_data.get('access_token')
            if not access_token:
                return JsonResponse({'error': 'Token non trovato nella risposta di 42'}, status=400)
                
            print(f"Token ottenuto da 42: {access_token[:10]}...")
        except Exception as e:
            print(f"Errore nel parsing del JSON dalla risposta di 42: {str(e)}")
            return JsonResponse({'error': f"Errore nel formato della risposta di 42: {str(e)}"}, status=400)
        
        # Ottieni i dati dell'utente
        try:
            print("Richiesta dati utente a 42 API...")
            response2 = requests.get(
                'https://api.intra.42.fr/v2/me', 
                headers={'Authorization': f'Bearer {access_token}'}
            )
            print(f"Risposta dati utente: Status {response2.status_code}")
            
            if response2.status_code != 200:
                print(f"Errore nella risposta dati utente: {response2.text}")
                return JsonResponse({'error': f"Errore nel recupero dati utente da 42: {response2.text}"}, status=400)
                
            user_data = response2.json()
            username = f"{user_data.get('login')}#42"
            print(f"Username 42: {username}")
        except Exception as e:
            print(f"Errore nel recupero dati utente: {str(e)}")
            return JsonResponse({'error': f"Errore nel recupero dati utente: {str(e)}"}, status=500)
        
        # Gestisci l'utente (nuovo o esistente)
        try:
            if not User.objects.filter(username=username).exists():
                print(f"Creazione nuovo utente: {username}")
                # Genera una password casuale per l'utente
                random_password = get_random_string(length=40)
                serializer = UserSerializer42(data={'username': username, 'password': random_password})
                
                if serializer.is_valid(raise_exception=True):
                    user = serializer.save()
                    response_data = {
                        "user": serializer.data
                    }
                    token, created = CustomToken.objects.get_or_create(user=user)
                    print(f"Nuovo utente creato con ID: {user.id}")
            else:
                print(f"Utente esistente trovato: {username}")
                user = User.objects.get(username=username)
                response_data = {
                    "user": UserSerializer42(user).data
                }
                token, created = CustomToken.objects.get_or_create(user=user)
                
            # Aggiorna lo stato dell'utente e salva
            user.status = True
            user.save()
            
            print(f"Token restituito all'utente: {token.key[:10]}...")
            return JsonResponse({'token': token.key, 'user': response_data})
        
        except Exception as e:
            print(f"Errore nella gestione dell'utente: {str(e)}")
            return JsonResponse({'error': f"Errore nella gestione dell'utente: {str(e)}"}, status=500)
        
    except Exception as e:
        print(f"Errore generale durante il login con 42: {str(e)}")
        return JsonResponse({'error': f"Errore generale: {str(e)}"}, status=500)
        