from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.RegisterView.as_view(), name= "token"),
    path ("login/", views.LoginView.as_view(), name= "login"),
    path ("info/", views.Info, name= "info"),
    path ("logout/", views.logout, name= "logout"),
    path ("token42/", views.get_42token, name= "token42"),
    path ("friends_info/", views.friends_info, name= "friends_info"),
]
