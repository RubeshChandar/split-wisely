from django.db import connection
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, Q
from django.views import View
from django.contrib import messages

from .forms import ExpenseForm, SettlementForm
from .helperfun import equaliser, get_or_make_calc
from .signals import post_expense_save
from .models import *

User = get_user_model()


@login_required
def home(request):
    user = request.user
    groupBalances = user.user_group_balance.select_related("group")

    total = groupBalances.aggregate(total=Sum('balance'))['total'] or 0
    return render(request, "split/index.html",
                  {"username": user.username, "amount": total, "groupBalances": groupBalances})


@login_required
def singleGroupView(request, slug):
    group = Group.objects\
        .prefetch_related("group_expenses")\
        .get(slug=slug)

    if not group.members.filter(id=request.user.id).exists():
        return redirect("/forbidden")

    expenses = group.group_expenses.all()

    user_splits = {
        split.expense_id: split.amount
        for split in Split.objects.filter(expense__group=group, user=request.user)
    }

    for expense in expenses:
        split_amount = user_splits.get(expense.id, 0)
        expense.isSettlement = False
        # Check if the user split is 0 but even if it is zero he might have lent money,
        # but if the user didn't pay it then he wasn't probably involved with this split so returning 0
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

    settlements = Settlement.objects.filter(group=group)\
        .select_related("paid_to", "paid_by")

    for settlement in settlements:
        settlement.isSettlement = True

    transactions = sorted(
        list(expenses) + list(settlements),
        key=lambda trans: trans.created_at,
        reverse=True
    )

    return render(request, "split/single-group.html", {
        "group": group,
        "transactions": transactions,
        "gb": group.group_balances.get(user=request.user)
    })


@login_required
def add_expense(request, slug):
    group = Group.objects.prefetch_related("members").get(slug=slug)
    failure_message = None
    # initial = {"amount": 200, "description": "ASDA", "paid_by": 1}
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


@login_required
def members_split(request, slug):
    return render(request, "split/partials/members-split.html", {
        "transactions": get_or_make_calc(slug)
    })


class SettlementView(LoginRequiredMixin, View):

    def get(self, request, slug):
        group = Group.objects.get(slug=slug)
        settlementForm = SettlementForm(group=group, user=request.user)

        return render(request, "split/include/settle.html", {
            "group": group,
            "form": settlementForm,
        })

    def post(self, request, slug):
        group = Group.objects.get(slug=slug)
        transactions = get_or_make_calc(slug)
        user = request.user

        settlementForm = SettlementForm(request.POST or None,
                                        group=group, user=user)

        if settlementForm.is_valid():
            paid_to = str(settlementForm.cleaned_data.get("paid_to"))
            acquired_amt = settlementForm.cleaned_data.get("amount")
            owed_amount = transactions.get((str(user), str(paid_to)), 0)

            if acquired_amt > owed_amount:
                messages.add_message(
                    request, messages.WARNING, "The entered amount is greater than owed amount")

            else:
                settlementForm.save(group=group, user=request.user)
                messages.add_message(request, messages.SUCCESS,
                                     f"Successfully added a settlement of {acquired_amt} to {paid_to} !!!")
                response = HttpResponse("", content_type="text/html")
                # Triggers JS event
                response["HX-Trigger"] = "settlementSuccess"
                return response

        return render(request, "split/include/settle.html", {
            "group": group,
            "form": settlementForm,
        })


@login_required
def check_settle_amount(request, slug):
    pay_to_id = request.GET.get("paid_to")
    transactions = get_or_make_calc(slug)

    if pay_to_id == "":
        return render(request, "split/partials/max-settle.html", {"exists": False})

    user = get_object_or_404(User.objects.only("username"), pk=pay_to_id)
    user = user.username.capitalize()

    amount = transactions.get(
        (str(request.user.username).capitalize(), user), 0)
    return render(request, "split/partials/max-settle.html", {"exists": True, "pt": user, "amt": amount})


@login_required
def delete_transaction(request, pk, trans_type):
    if trans_type == "settlement":
        transaction = get_object_or_404(Settlement, pk=pk)
        transaction.isSettlement = True
    else:
        transaction = get_object_or_404(Expense, pk=pk)
        transaction.isSettlement = False

    if request.method == "POST":

        if trans_type == "expense" or \
                (trans_type == "settlement" and request.user == transaction.paid_by):
            transaction.delete()
            messages.add_message(
                request, messages.SUCCESS, f"{trans_type.capitalize()} deleted successfully")
        else:
            messages.add_message(
                request, messages.WARNING, f"Couldn't delete this {trans_type} as it wasn't made by you!")

        response = HttpResponse(status=204)
        response["HX-Trigger"] = "transactionDeleted"
        return response

    return render(request, "split/partials/trans-delete.html", {"transaction": transaction})


@login_required
def get_shares(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    shares = expense.splits.prefetch_related("user")
    return render(request, "split/partials/view-shares.html", {
        "expense": expense,
        "shares": shares
    })


@login_required
def manage_members(request, slug, pk=None, action=None):
    group = Group.objects.get(slug=slug)

    if request.method == "POST":
        if action == "add":
            group.members.add(pk)
        if action == "remove":
            if pk != group.created_by_id:
                group.members.remove(pk)
            else:
                messages.add_message(
                    request, messages.WARNING, "Admin can't be removed")

        return HttpResponse(status=200, headers={"HX-Refresh": "true"})
    return render(request, "split/manage-members.html", {"group": group})


def search_user(request, slug):
    term = request.GET.get("term")

    if term == "":
        return render(request, "split/partials/users-list.html")

    group_members = Group.objects.get(
        slug=slug).members.values_list("id", flat=True)

    users = User.objects.exclude(id__in=group_members) \
        .filter(Q(username__icontains=term) | Q(email__icontains=term))[:5]

    return render(request, "split/partials/users-list.html", {"users": users, "slug": slug})


@login_required
def create_grp(request):
    grp_name = request.POST.get("new_group_name", None)
    group, created = Group.objects.get_or_create(
        name=grp_name, created_by=request.user)

    if not created:
        messages.add_message(request, messages.WARNING,
                             "You tried to create a group with the same name")

    group.members.add(request.user)
    return redirect("single-group", slug=group.slug)


@login_required
def delete_grp(request, slug):
    group = Group.objects.get(slug=slug)

    if group.created_by != request.user:
        messages.add_message(request, messages.WARNING,
                             f"Group can't be deleted as you are not the admin for {group.name} group!!")
        return redirect("single-group", slug=slug)

    group.delete()
    messages.add_message(request, messages.SUCCESS,
                         f"{group.name} deleted successfully")
    return redirect("home")
