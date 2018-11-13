from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail
from .forms import *
import psycopg2

# Create your views here.
#index page
def index(request):
    return render(request, "index.html")
    # return HttpResponse("HELLO WORLD")


def login(request):
    return render(request, "login.html")


def createUser(request):

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]

            print(username, email)


    form = CreateUserForm()
    return render(request, "createUser.html", {"form": form})


# def userdb(request):
#     username = request.POST("username")
#     email = request.POST("email")
#     password = request.POST("password")
#
#     conn = psycopg2.connect(host="localhost", database="crealityDB", user="postgres", password="postgres")
#     cur = conn.cursor()
#     cur.execute("INSERT INTO users VALUES (username, email, password)")



#form username handler

# def get_newUserInfo(request):
#     if request.method == "POST":
#         form = CreatUserForm(request.POST)
#         if form.is_valid():
#             # username = form.cleaned_data['username']
#             # email = form.cleaned_data['email']
#             # password = form.cleaned_data['password']
#             # recipients = ["august12.feb2004@gmail.com"]
#             # send_email("Created User", f"You created user: {username} with email: {email} and password: {password}", email, recipients)
#             return HttpResponseRedirect("/thanks/")
#     else:
#         form = CreatUserForm()
#
#     return render(request, 'index.html', {'formHere' : form,})
