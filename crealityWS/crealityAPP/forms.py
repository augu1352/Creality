from django import forms


class CreateUserForm(forms.Form):
    username = forms.CharField(label="Desired Username")
    email = forms.EmailField(label="Valid Email Address")
    password = forms.CharField(widget=forms.PasswordInput())
