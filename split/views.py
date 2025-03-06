from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ExpenseForm
from .models import *

User = get_user_model()


@login_required
def home(request):
    user = request.user
    # groupBalances = GroupBalance.objects.filter(
    #     user=user).select_related("group")
    groupBalances = user.groupbalances.all().select_related("group")
    total = groupBalances.aggregate(total=Sum('balance'))['total'] or 0

    return render(request, "split/index.html",
                  {"username": user.username, "amount": total, "groupBalances": groupBalances})


@login_required
def singleGroupView(request, slug):
    group = Group.objects.get(slug=slug)
    return render(request, "split/single-group.html", {"group": group})


# @login_required
# def add_expense(request, slug):
#     group = get_object_or_404(Group, slug=slug)
#     expenseForm = ExpenseForm(request.POST or None, group=group)

#     if request.method == "POST":
#         if expenseForm.is_valid():
#             expenseForm.save(group=group, user=request.user)

#             # redirect login for htmx
#             redirect_url = reverse("single-group", kwargs={"slug": group.slug})
#             response = HttpResponse()
#             response['HX-Redirect'] = redirect_url
#             return response

#     return render(request, "split/add-expense-form.html", {"form": expenseForm, "group": group})


# Test
@login_required
def add_expense(request, slug):
    group = Group.objects.prefetch_related("members").get(slug=slug)
    expenseForm = ExpenseForm(request.POST or None, group=group)

    if request.method == "POST":
        if expenseForm.is_valid():
            if request.POST.get('rubesh_split', False):
                print("In here")
            else:
                print("No value")

    return render(request, "split/add-expense-form.html", {"form": expenseForm, "group": group})
