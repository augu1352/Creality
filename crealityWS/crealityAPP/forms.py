from django import forms


class CreatUserForm(forms.Form):
    username = forms.CharField(label='username', max_lenth=50)
    email = forms.EmailField()
    password = forms.PasswordInput()
