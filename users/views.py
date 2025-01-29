from django.shortcuts import render, HttpResponse, redirect

from django.contrib.auth import authenticate, login, logout, get_user_model
from .forms import LoginForm, SignupForm
# Create your views here.


def signin(request):

    if request.user.is_authenticated:
        return redirect("home")

    loginform = LoginForm(request.POST or None)

    next_url = request.POST.get('next') or request.GET.get('next') or "home"
    print(next_url)

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
    ctx = {
        "form": None,
        "is_login": False
    }

    signupform = SignupForm()
    ctx["form"] = signupform

    if request.method == "POST":
        signupform = SignupForm(request.POST or None)
        if signupform.is_valid():
            print(signupform.cleaned_data['username'])
        else:
            ctx["form"] = signupform

    return render(request, "auth/auth-page.html", ctx)


def check_username(request):
    username = request.POST.get('username')
    if username == "" or len(username) < 5:
        return HttpResponse("<span class='mi'>Please type in a valid username<span>")
    if get_user_model().objects.filter(username__iexact=username).exists():
        return HttpResponse(f"<span class='in_use'>{username}</span> already exists")
    return HttpResponse(f"<span class='avail'>{username}</span> is available to use")


def signout(request):
    logout(request)
    return redirect("login")
