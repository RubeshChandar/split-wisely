from django.shortcuts import render

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import LoginForm, SignupForm
# Create your views here.


def login(request):
    ctx = {
        "errorMessage": None,
        "form" : None,
        "is_login" : True,
    }
       
    if request.method == "POST":
        loginform = LoginForm(request.POST)
        if loginform.is_valid():
            email = loginform.cleaned_data['email']
            password = loginform.cleaned_data['password']
            
        else:
            ctx['form'] = loginform
            return render(request, "auth/auth-page.html", ctx)
    else:
        ctx['form'] = LoginForm()

    return render(request, "auth/auth-page.html", ctx)


def register(request):
    ctx = {
        "errorMessage": None,
        "form" : None,
        "is_login" : False
    }

    signupform = SignupForm()
    ctx["form"] = signupform

    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("password_confirm")

        if confirm_password == password:
            print(f"{username} -> {email}")
        else:
            ctx["errorMessage"] = "Password not matched"

    return render(request, "auth/auth-page.html", ctx)
