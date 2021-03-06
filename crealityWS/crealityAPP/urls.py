from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.loginUser, name="login"),
    path("createuser/", views.createUser, name="createUser"),
    path("creality/", views.creality, name="creality"),
    path("creality/upload_image/", views.uploadImage, name="uploadImage"),
    path("creality/view_image/", views.viewImage, name="viewImage"),
]
