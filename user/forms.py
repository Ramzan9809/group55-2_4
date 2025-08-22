from django import forms


class RegisterForm(forms.Form):
    avatar = forms.ImageField(required=False)
    age = forms.IntegerField(min_value=0, max_value=100, required=False)
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(required=True)
    password_confirm = forms.CharField(required=True)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(required=True)