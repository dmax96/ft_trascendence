from django.urls import path
from . import views

urlpatterns = [
    path("nick/", views.Change_Player, name="change_player"),
    path("pong_result/", views.WinLose_pong, name="win_lose_pong"),
    path("tictactoe_result/", views.WinLose_tictac, name="win_lose_tictac"),
    path("profile_image/", views.update_profile_image, name="profile_image"),
    path("add_friends/", views.add_friend, name="add_friend"),
    path("language/", views.language, name="change_language"),
    path("get_friends/", views.get_friends, name="get_friends"),
]
