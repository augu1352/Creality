from django import forms


class CreateUserForm(forms.Form):
    username = forms.CharField(label="Username")
    email = forms.EmailField(label="Email Address")
    password = forms.CharField(widget=forms.PasswordInput())


class LoginUserForm(forms.Form):
    username = forms.CharField(label="Username")
    password = forms.CharField(widget=forms.PasswordInput())


class UploadImageForm(forms.Form):
    image = forms.ImageField(label="Upload Image")
