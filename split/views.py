from django.shortcuts import redirect, render
from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .forms import ExpenseForm
from .helperfun import equaliser
from .models import *
from .signals import post_expense_save

User = get_user_model()


@login_required
def home(request):
    user = request.user
    groupBalances = user.user_group_balance.prefetch_related("group").all()
    total = groupBalances.aggregate(total=Sum('balance'))['total'] or 0
    return render(request, "split/index.html",
                  {"username": user.username, "amount": total, "groupBalances": groupBalances})


@login_required
def singleGroupView(request, slug):
    group = Group.objects\
        .prefetch_related("group_expenses")\
        .get(slug=slug)
    print(group.members.all())
    if not group.members.filter(id=request.user.id).exists():
        return redirect("/forbidden")

    expenses = group.group_expenses.all()

    user_splits = {
        split.expense_id: split.amount
        for split in Split.objects.filter(expense__group=group, user=request.user)
    }

    for expense in expenses:

        split_amount = user_splits.get(expense.id, 0)

        # Check if the user split is 0 but even if it is zero he might have lent money,
        # but if the user didn;t pay it then he wasn't probably involved with this split so returning 0
        if split_amount == 0 and expense.paid_by_id != request.user.id:
            expense.lent_or_borrowed = 0
            continue

        # If the user hasn't paid any money but has a split share then he owes the entire money hence
        # -ve for the view logic
        elif expense.paid_by_id != request.user.id:
            expense.lent_or_borrowed = -split_amount
            continue

        # Here the user defintely gave money so we are calculating how much he lent,
        # by just subtracting his share from the total expense amount
        else:
            expense.lent_or_borrowed = expense.amount - split_amount

    return render(request, "split/single-group.html", {"group": group, "expenses": expenses})


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
