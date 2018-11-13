from django import forms


def createUserForm(forms.Form):
    username = forms.Charfield(label="Desired Username")
    email = forms.Emailfield(label="Valid Email Address")
    password = forms.CharField(widget=PasswordInput())
    
