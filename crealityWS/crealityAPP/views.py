from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.core.mail import send_mail
from .forms import *
import psycopg2

# Create your views here.
#index page
def index(request):
    response = HttpResponseRedirect("/creality/")

    conn = psycopg2.connect(dbname="crealitydb", user="postgres", password="120204Aj", host="localhost")
    cur = conn.cursor()

    if "session_id" in request.COOKIES:
        cur.callproc("fn_check_sessionid", [request.COOKIES["session_id"]])
        fetched = cur.fetchone()
        # print(fetched)
        if "True" in str(fetched):
            return response
        else:
            return render(request, "index.html")
    else:
        return render(request, "index.html")

    conn.commit()
    cur.close()
    conn.close()

    # return HttpResponse("HELLO WORLD")


def update_session_timestamp(request):
    conn = psycopg2.connect(dbname="crealitydb", user="postgres", password="120204Aj", host="localhost")
    cur = conn.cursor()

    if "session_id" in request.COOKIES:
        session_id = request.COOKIES["session_id"]

        cur.callproc("fn_update_session_timestamp", [session_id])

    conn.commit()
    cur.close()
    conn.close()


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

                print(username)
                response = HttpResponseRedirect("/creality/")
                cur.execute("BEGIN")
                cur.callproc("fn_createsessionid", [username])
                fetched = cur.fetchone()
                cur.execute("COMMIT")
                session_id = list(fetched)[0]
                print(session_id)

                response.set_cookie("session_id", session_id)
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

    if "session_id" in request.COOKIES:
        cur.callproc("fn_check_sessionid", [request.COOKIES["session_id"]])
        fetched = cur.fetchone()
        if "True" in str(fetched):
            return response
        else:
            return HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect("/")

    cur.close()
    conn.close()

    print(request.COOKIES)
