from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
# Create your views here.


def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
    return render(request, "auth/login.html")


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("password_confirm")

        if confirm_password == password:
            print(f"{username} -> {email}")
        else:
            print("Password not matched")
    return render(request, "auth/register.html")
