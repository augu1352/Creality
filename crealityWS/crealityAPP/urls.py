from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("", views.get_newUserInfo, name="get_newUserInfo"),
    path("login/", views.login, name="login"),
    path("createuser/", views.createUser, name="createUser")
]
