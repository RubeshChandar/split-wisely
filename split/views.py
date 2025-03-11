from django.shortcuts import redirect, render
from django.urls import reverse
from django.http import HttpResponse
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from .forms import ExpenseForm
from .helperfun import equaliser
from .models import *
from .signals import post_expense_save

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


@login_required
def add_expense(request, slug):
    group = Group.objects.prefetch_related("members").get(slug=slug)
    failure_message = None

    expenseForm = ExpenseForm(request.POST or None, group=group)
    splits = {member: 0 for member in group.members.all()}

    if request.method == "POST":
        if expenseForm.is_valid():
            for split in splits:
                splits[split] = float(request.POST.get(split.username, 0))

            # Equalised amount : split total discrepancies
            splits = equaliser(splits, float(
                expenseForm.cleaned_data['amount']))

            if not splits:
                failure_message = "The difference between amount and sum of splits is too high please manually adjust this!"
            else:
                # Only save when split exists
                expense = expenseForm.save(group=group, user=request.user)

                # Sending a signal to store the split into db
                post_expense_save.send(
                    sender=Expense, instance=expense, split_created=True, splits=splits)

                return redirect("single-group", slug=slug)

    return render(request, "split/add-expense-form.html", {
        "form": expenseForm,
        "group": group,
        "fail_msg": failure_message
    })
