from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
from rest_framework.authentication import TokenAuthentication
from django.conf import settings
from django.utils.crypto import get_random_string

class User (AbstractUser):
    username = models.CharField(max_length=250, unique=True)
    password = models.CharField(max_length=250)
    wins_pong = models.IntegerField(default=0)
    loses_pong = models.IntegerField(default=0)
    winrate_pong = models.FloatField(default=0)
    wins_tictactoe = models.IntegerField(default=0)
    loses_tictactoe = models.IntegerField(default=0)
    draw_tictactoe = models.IntegerField(default=0)
    winrate_tictactoe = models.FloatField(default=0)
    profile_image = models.CharField(max_length=500, default='media/silvietto.jpeg')
    player = models.CharField(max_length=250, blank=True)
    player2 = models.CharField(max_length=250, blank=True)
    language = models.CharField(max_length=10, default="EN")
    score = models.IntegerField(default=0)
    status = models.BooleanField(default=False)
    scoreplayer2 = models.IntegerField(default=0)
    matchistory_pong = models.JSONField(default=list)
    matchistory_tictactoe = models.JSONField(default=list)
    friendlist = models.ManyToManyField('self', blank=True)


    def save(self, *args, **kwargs):
        if not self.player:
            self.player = self.username
        super().save(*args, **kwargs)

    def add_friend(self, new_friend):
        self.friendlist.add(new_friend)

    def remove_friend(self, friend):
        self.friendlist.remove(friend)

    def get_friends(self):
        return self.friendlist.all()

class CustomToken(models.Model):
    key = models.CharField("Key", max_length=128, db_index=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='custom_auth_token',
        on_delete=models.CASCADE, verbose_name="User"
    )
    created = models.DateTimeField("Created", auto_now_add=True)

    class Meta:
        unique_together = (('user',),)
        verbose_name = 'Custom Token'
        verbose_name_plural = 'Custom Tokens'
    
    def save(self, *args, **kwargs):
        if not self.key:
            self.key = get_random_string(length=128)
        super().save(*args, **kwargs)


class CustomTokenAuthentication(TokenAuthentication):
    def get_model(self):
        return CustomToken
