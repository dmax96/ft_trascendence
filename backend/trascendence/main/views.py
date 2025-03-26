from django.shortcuts import render, redirect
from rest_framework import generics, status
from .models import User, CustomToken, CustomTokenAuthentication
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
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
from datetime import datetime
from django.utils import timezone


@api_view(["POST"])
@authentication_classes([SessionAuthentication, CustomTokenAuthentication])
@permission_classes([IsAuthenticated])
def Change_Player(request):
    user = request.user
    user.player = request.data["player"]
    if not user.player:
        return Response(
            {"error": "Player name cannot be empty"}, status=status.HTTP_400_BAD_REQUEST
        )
    user.save()
    return Response({"player": user.player}, status=status.HTTP_200_OK)


@api_view(["POST"])
@authentication_classes([SessionAuthentication, CustomTokenAuthentication])
@permission_classes([IsAuthenticated])
def WinLose_pong(request):
    user = request.user
    user.player2 = request.data["player2"]
    win = request.data["win"]
    score = request.data["score"]
    scoreplayer2 = request.data["scoreplayer2"]
    if win not in ["true", "false"]:
        return Response({"error": "Invalid win value."}, status=status.HTTP_400_BAD_REQUEST)
    date = datetime.now().strftime('%d/%m/')
    if win == "true":
        user.wins_pong += 1
    else:
        user.loses_pong += 1
    user.matchistory_pong.append(
            {
                "win": win,
                "score": score,
                "scoreplayer2": scoreplayer2,
                "player2": user.player2,
                "date" : date,
            }
        )
    if len(user.matchistory_pong) > 5:
        user.matchistory_pong = user.matchistory_pong[-5:]
    user.winrate_pong = user.wins_pong / (user.wins_pong + user.loses_pong) * 100
    user.save()
    return Response(
        {
            "pong": {
                    "wins": user.wins_pong,
                    "loses": user.loses_pong,
                    "winrate": user.winrate_pong,
                    "matchHistory": user.matchistory_pong,
                }
            },
        status=status.HTTP_200_OK,
        )


@api_view(["POST"])
@authentication_classes([SessionAuthentication, CustomTokenAuthentication])
@permission_classes([IsAuthenticated])
def WinLose_tictac(request):
        user = request.user
        player2 = request.data["player2"]
        win = request.data["win"]
        if not player2 or not win:
            return Response({"error": "Both player2 and win fields are required."}, status=status.HTTP_400_BAD_REQUEST)        
        date = datetime.now().strftime('%d/%m')
        if win == "true":
            user.wins_tictactoe += 1
            game_result = "win"
        elif win == "false":
            user.loses_tictactoe += 1
            game_result = "lose"
        else:
            user.draw_tictactoe += 1
            game_result = "draw"
            
        # Aggiungi la nuova partita
        user.matchistory_tictactoe.append({ "win": game_result, "player2": player2, "date": date})
        
        # Mantieni solo le ultime 5 partite
        if len(user.matchistory_tictactoe) > 5:
            user.matchistory_tictactoe = user.matchistory_tictactoe[-5:]
            
        # Calcola il winrate considerando solo vittorie e sconfitte (non i pareggi)
        if user.wins_tictactoe + user.loses_tictactoe != 0:
            user.winrate_tictactoe = (
                user.wins_tictactoe / (user.wins_tictactoe + user.loses_tictactoe) * 100
            )
        user.save()
        return Response(
            {
                "tictactoe": {
                    "wins": user.wins_tictactoe,
                    "loses": user.loses_tictactoe,
                    "winrate": user.winrate_tictactoe,
                    "draws": user.draw_tictactoe,
                    "win": game_result,
                    "matchHistory": user.matchistory_tictactoe,
                }
            },
            status=status.HTTP_200_OK,
        )


@api_view(["POST"])
@authentication_classes([SessionAuthentication, CustomTokenAuthentication])
@permission_classes([IsAuthenticated])
def update_profile_image(request):
    user = request.user
    user.profile_image = request.data["profile_path"]
    user.save()
    return JsonResponse({"response": "successful"})


@api_view(["POST"])
@authentication_classes([SessionAuthentication, CustomTokenAuthentication])
@permission_classes([IsAuthenticated])
def language(request):
    user = request.user
    user.language = request.data["language"]
    if not user.language:
        return JsonResponse({"error": "Language cannot be empty"}, status=status.HTTP_400_BAD_REQUEST)
    user.save()
    return JsonResponse({"response": "successful"})



@api_view(["POST"])
@authentication_classes([SessionAuthentication, CustomTokenAuthentication])
@permission_classes([IsAuthenticated])
def add_friend(request):
    user = request.user
    friend_username = request.data["friend_username"]
    if not friend_username:
        return JsonResponse({'error': "friend_username is required"}, status=status.HTTP_400_BAD_REQUEST)
    if friend_username == user.username:
        return JsonResponse(
            {"error": "You cannot add yourself as a friend"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        new_friend = User.objects.get(username=friend_username)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)
    if new_friend in user.get_friends():
        return JsonResponse(
            {"error": "You are already friends with this user"}, status=status.HTTP_400_BAD_REQUEST)
    if user.get_friends().count() >= 10:
        return JsonResponse(
            {"error": "You cannot have more than 10 friends"}, status=status.HTTP_400_BAD_REQUEST)
    user.add_friend(new_friend)
    return JsonResponse({"response": "successful friend added"}, status=200)


@api_view(["GET"])
@authentication_classes([SessionAuthentication, CustomTokenAuthentication])
@permission_classes([IsAuthenticated])
def get_friends(request):
    user = request.user
    friends = user.get_friends()
    friends_list = [
        {"username": friend.username, "status": friend.status} for friend in friends
    ]
    return JsonResponse({"friends": friends_list}, status=200)

