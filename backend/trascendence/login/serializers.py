from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
from django import forms
from rest_framework.serializers import ModelSerializer

class FriendListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'status', 'player', 'profile_image', 'matchistory_pong', 'matchistory_tictactoe', 'wins_pong', 'loses_pong', 'winrate_pong', 'wins_tictactoe', 'loses_tictactoe', 'winrate_tictactoe']


class UserSerializer(serializers.ModelSerializer):
    friendlist = FriendListSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = [
            "username",
            "profile_image",
            "player",
            "password",
            "friendlist",
            "wins_pong",
            "loses_pong",
            "winrate_pong",
            "wins_tictactoe",
            "loses_tictactoe",
            "winrate_tictactoe",
            "matchistory_pong",
            "matchistory_tictactoe",
            "language",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password should be at least 8 characters long.")
        return value

    def validate(self, data):
        if '#' in data.get('username', '') or '#' in data.get('password', ''):
            raise serializers.ValidationError("Username and password should not contain '#'.")
        return data
    

class UserSerializer42(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
