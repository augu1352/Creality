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


def createUser(request):

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            conn = psycopg2.connect(dbname="crealitydb", user="postgres", password="120204Aj", host="localhost")
            cur = conn.cursor()

            cur.execute("INSERT INTO users(user_username, user_email, user_password) VALUES(%s, %s, %s)", (username, email, password))

            conn.commit()
            cur.close()
            conn.close()

            return HttpResponseRedirect("/login/")

    form = CreateUserForm()
    return render(request, "createUser.html", {"form": form})



def loginUser(request):
    if request.method == "POST":
        form = LoginUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            conn = psycopg2.connect(dbname="crealitydb", user="postgres", password="120204Aj", host="localhost")
            cur = conn.cursor()

            cur.execute("SELECT user_password FROM users;")
            fetched = cur.fetchall()
            print(fetched)

            # cur.execute("SELECT * FROM users;")
            # fetched = cur.fetchall()
            # # if "silas" in fetched
            # print(fetched)
            # index = [x[1] for x in fetched].index(username)
            #
            # # if fetched[index]
            # print(fetched[index])

            conn.commit()
            cur.close()
            conn.close()

    form = LoginUserForm()
    return render(request, "login.html", {"form": form})

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
