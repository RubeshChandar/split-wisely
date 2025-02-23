from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from .models import *

User = get_user_model()


@login_required
def home(request):
    user = request.user
    groupBalances = GroupBalance.objects.filter(user=user)
    total = groupBalances.aggregate(total=Sum('balance'))['total'] or 0

    return render(request, "split/index.html",
                  {"username": user.username, "amount": total, "groupBalances": groupBalances})
