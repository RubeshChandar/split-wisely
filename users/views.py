from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout, get_user_model
from .forms import LoginForm, SignupForm
# Create your views here.


def signin(request):

    if request.user.is_authenticated:
        return redirect("home")

    loginform = LoginForm(request.POST or None)

    next_url = request.POST.get('next') or request.GET.get('next') or "home"

    if request.method == "POST" and loginform.is_valid():
        user = loginform.userlogin()
        if user:
            login(request, user)
            return redirect(next_url)

    return render(request, "auth/auth-page.html", {
        "form": loginform,
        "is_login": True,
    })


def register(request):

    if request.user.is_authenticated:
        return redirect("home")

    signupform = SignupForm(request.POST or None)

    if request.method == "POST" and signupform.is_valid():
        user = signupform.signup()
        re_url = reverse("login")+f"?info=success&user={user.username}"
        return redirect(re_url)

    return render(request, "auth/auth-page.html", {
        "form": signupform,
        "is_login": False,
    })


def check_username(request):
    username = request.POST.get('username').replace(' ', '')

    if username == "" or len(username) < 4:
        return HttpResponse("<span class='mi'>Please type in a valid username<span>")
    if get_user_model().objects.filter(username__iexact=username).exists():
        return HttpResponse(f"<span class='in_use'>{username}</span> already exists")
    return HttpResponse(f"<span class='avail'>{username}</span> is available to use")


def signout(request):
    logout(request)
    return redirect("login")
