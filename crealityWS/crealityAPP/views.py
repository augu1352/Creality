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
        response = render(request, "login.html", {"form": form})
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
                response.set_cookie("username", username)
                # request.COOKIES["username"] = username
                print("debug")
                print(request.COOKIES)
                return HttpResponseRedirect("/creality/")
            else:
                message = "Wrong Password!"
                return render(request, "login.html", {"form": form, "message": message})
                # print("messageStart")
                # messages = messages.error(request, "Wrong Password!")
                # print("messageStop")

            # cur.execute("SELECT user_username FROM users;")
            # fetched = cur.fetchall()
            # print("debug")
            # print(fetched)
            # if fetched.__contains__(username):
            #     cur.execute("SELECT user_password FROM user WHERE user_username=\"%s\"", (username))
            #     fetchedpw = fetchall()
            #     print(fetchedpw)
            #     print("debug")
            # print(fetched)

            # cur.execute("SELECT * FROM users;")
            # fetched = cur.fetchall()
            # # if "silas" in fetched
            # print("debug")
            # print(fetched)
            # index = [x[1] for x in fetched].index(username)
            # user = list(fetched[index])
            #
            # if user[3] == password:
            #     print("right password")
            #     return HttpResponseRedirect("/creality/")
            # else:
            #     print("wrong password")
            #
            #
            #
            # # if fetched[index]
            # print("debug")
            # print(user)

            conn.commit()
            cur.close()
            conn.close()

    form = LoginUserForm()
    return render(request, "login.html", {"form": form})



def creality(request):
    conn = psycopg2.connect(dbname="crealitydb", user="postgres", password="120204Aj", host="localhost")
    cur = conn.cursor()
    cur.close()
    conn.close()
    print(request.COOKIES)
    if "username" in request.COOKIES:
        cur.callproc()
        cookie_uname = request.COOKIES["username"]
        print(cookie_uname)
    elif "username" not in request.COOKIES:
        print("no 'username' in COOKIES")
    else:
        print("cookies don't work")
    return render(request, "creality.html")



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
