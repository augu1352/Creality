from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.core.mail import send_mail
from .forms import *
import psycopg2
import io
from PIL import Image
import re
import base64


def index(request):
    response = HttpResponseRedirect("/creality/")

    conn = psycopg2.connect(
        dbname="crealitydb", user="postgres", password="postgres", host="localhost")
    cur = conn.cursor()

    if "session_id" in request.COOKIES:
        cur.callproc("fn_check_sessionid", [request.COOKIES["session_id"]])
        fetched = cur.fetchone()
        if "True" in str(fetched):
            return response
        else:
            return render(request, "index.html")
    else:
        return render(request, "index.html")

    conn.commit()
    cur.close()
    conn.close()


def update_session_timestamp(request):
    conn = psycopg2.connect(
        dbname="crealitydb", user="postgres", password="postgres", host="localhost")
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

            conn = psycopg2.connect(
                dbname="crealitydb", user="postgres", password="postgres", host="localhost")
            cur = conn.cursor()

            cur.execute("INSERT INTO users(user_username, user_email, user_password) VALUES(%s, %s, %s)",
                        (username, email, password))

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

            conn = psycopg2.connect(
                dbname="crealitydb", user="postgres", password="postgres", host="localhost")
            cur = conn.cursor()

            cur.callproc("fn_checkpassword", (username, password))
            fetched = cur.fetchone()
            if "True" in str(fetched):
                response = HttpResponseRedirect("/creality/")
                cur.execute("BEGIN")
                cur.callproc("fn_createsessionid", [username])
                fetched = cur.fetchone()
                cur.execute("COMMIT")
                session_id = list(fetched)[0]

                response.set_cookie("session_id", session_id)
                return response
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
    conn = psycopg2.connect(
        dbname="crealitydb", user="postgres", password="postgres", host="localhost")
    cur = conn.cursor()

    if "session_id" in request.COOKIES:
        cur.callproc("fn_check_sessionid", [request.COOKIES["session_id"]])
        fetched = cur.fetchone()
        if "True" in str(fetched):
            pass
        else:
            return HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect("/")

    conn.commit()
    cur.close()
    conn.close()

    template = "creality.html"
    context = {}

    response = render(request, template, context)
    return response


def uploadImage(request):
    conn = psycopg2.connect(
        dbname="crealitydb", user="postgres", password="postgres", host="localhost")
    cur = conn.cursor()

    if "session_id" in request.COOKIES:
        cur.callproc("fn_check_sessionid", [request.COOKIES["session_id"]])
        fetched = cur.fetchone()
        if "True" in str(fetched):
            pass
        else:
            return HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect("/")

    model = "Upload Images"
    if request.method == "POST":
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            if request.FILES["image"]:
                imageField = request.FILES["image"]
                stream = imageField.open()

                image = Image.open(stream)

                if "session_id" in request.COOKIES:
                    cur.callproc("fn_check_sessionid", [request.COOKIES["session_id"]])
                    fetched = cur.fetchone()
                    if "True" in str(fetched):
                        session_id = request.COOKIES["session_id"]
                    else:
                        return HttpResponseRedirect("/")
                else:
                    return HttpResponseRedirect("/")

                print(image)
                cur.execute("BEGIN")
                cur.callproc("fn_save_bin_image", ((base64.b64encode(image.tobytes())), session_id, image.mode, f"{image.size[0]}x{image.size[1]}", image.format))
                cur.execute("COMMIT")
                stream.close()


                # cur.execute("SELECT binary_data FROM public.images;")
            else:
                print("file not in memory  debug")

    cur.close()
    conn.close()

    form = UploadImageForm()
    template = "uploadImage.html"
    context = {"model": model, "form": form}

    response = render(request, template, context)
    return response


def viewImage(request):
    conn = psycopg2.connect(
        dbname="crealitydb", user="postgres", password="postgres", host="localhost")
    cur = conn.cursor()

    if "session_id" in request.COOKIES:
        cur.callproc("fn_check_sessionid", [request.COOKIES["session_id"]])
        fetched = cur.fetchone()
        if "True" in str(fetched):
            session_id = request.COOKIES["session_id"]
        else:
            return HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect("/")


    images = []
    lst = [item[0] for i in images]

    cur.callproc("fn_get_bin_images", [session_id])
    fetched = list(cur.fetchall())
    # print(f"DEBUG | {fetched[]}")

    for i in list(fetched):
        imgSize = re.split("x", i[2])
        for n in imgSize:
            imgSize[imgSize.index(n)] = int(n)
        imgSize = tuple(imgSize)
        print(imgSize)
        # print(i[0])
        # print(base64.b64decode(i[0]))
        image = base64.b64decode(i[0])
        images.append([image, i[3]])
    # print(images)

    cur.close()
    conn.close()

    template = "viewImage.html"
    context = {"image": lst, "image_type": lst[1]}

    response = render(request, template, context)
    return response
