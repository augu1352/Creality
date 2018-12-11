from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.core.mail import send_mail
from .forms import *
import psycopg2

# Create your views here.
#index page
def index(request):
    return render(request, "index.html")
    # return HttpResponse("HELLO WORLD")


def update_session_timestamp(request):
    conn = psycopg2.connect(dbname="crealitydb", user="postgres", password="120204Aj", host="localhost")
    cur = conn.cursor()

    session_id = request.COOKIE["session_id"]

    cur.callproc("fn_update_session_timestamp", (session_id))


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

            cur.callproc("fn_checkpassword", (username, password))
            fetched = cur.fetchone()
            if "True" in str(fetched):
                # context = RequestContext(request)
                # response = HttpResponse()
                # response.set_cookie("username", username)

                # session_id
                #
                # request.COOKIES["session_id"] = session_id
                # request.COOKIES["last_connection"] = datetime.datetime.now()
                # response = HttpResponse()
                # response = render(request, "login.html", {"form": form})
                print(username)
                # response = render(request, "login.html", {"form": form})
                response = HttpResponseRedirect("/creality/")
                cur.callproc("fn_createsessionid", (username))
                fetched = fetchone()
                print(fetched)
                # response.set_cookie("session_id", session_id)
                # request.COOKIES["username"] = username
                print("debug")
                print(request.COOKIES)
                return response
                # return HttpResponseRedirect("/creality/")

            else:
                message = "Wrong Password!"
                return render(request, "login.html", {"form": form, "message": message})


            conn.commit()
            cur.close()
            conn.close()

            return HttpResponseRedirect("/creality/")

    form = LoginUserForm()
    return render(request, "login.html", {"form": form})



def creality(request):
    response = render(request, "creality.html")
    conn = psycopg2.connect(dbname="crealitydb", user="postgres", password="120204Aj", host="localhost")
    cur = conn.cursor()
    cur.close()
    conn.close()
    # response.set_cookie("testCookie", "1234")
    print(request.COOKIES)
    return response
