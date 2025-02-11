from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

User = get_user_model()


@login_required
def home(request):
    user = request.user
    if user in User.objects.all():
        print("In the records")
    return render(request, "split/index.html", {"username": user.username, "amount": "£800"})
