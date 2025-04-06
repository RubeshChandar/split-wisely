import networkx as nx
from django.core.cache import cache
from split.models import GroupBalance


def equaliser(splits, amount):
    sum_of_splits = sum(splits.values())

    # If already balanced, return as is
    if amount == sum_of_splits:
        return splits

    # Calculate excess amount
    excess_amount = abs(amount - sum_of_splits)

    if excess_amount > 1:
        return False

    # Identify non-zero contributors
    non_zero_keys = [key for key, value in splits.items() if value != 0]

    # If all are zero, distribute equally among all users
    if not non_zero_keys:
        num_people = len(splits)
        base_amount = round(excess_amount / num_people, 2)
        total_distributed = base_amount * num_people

        # Adjust last person to ensure sum is exactly equal to amount
        adjustment = amount - (sum_of_splits + total_distributed)
        first_key = next(iter(splits))

        return {
            key: round(value + base_amount +
                       (adjustment if key == first_key else 0), 2)
            for key, value in splits.items()
        }

    # Distribute excess amount among non-zero contributors
    num_people = len(non_zero_keys)
    base_amount = round(excess_amount / num_people, 2)
    total_distributed = base_amount * num_people

    # Adjust last person to ensure exact total
    adjustment = amount - (sum_of_splits + total_distributed)

    for i, key in enumerate(non_zero_keys):
        splits[key] += base_amount + (adjustment if i == 0 else 0)

    return splits


def cash_flow_finder(balances):
    G = nx.DiGraph()

    # We need to add users as nodes with demand to 0 to not move any money
    # and also convert the balance to int as only networkx works only with int
    for user, balance in balances.items():
        G.add_node(user, demand=int(balance*100))

    users = list(balances.keys())

    # Our primary objective is to minimize the total amount of money transferred to settle the debts.
    # We're not trying to optimize for any other cost associated with the transactions themselves.
    # And that's why the weight is set to 0
    for i in range(len(users)):
        for j in range(i+1, len(users)):
            G.add_edge(users[i], users[j], weight=0)
            G.add_edge(users[j], users[i], weight=0)

    flow_dict = nx.min_cost_flow(G)
    transactions = []

    for sender, receivers in flow_dict.items():
        for receiver, amount in receivers.items():
            if amount > 0:
                transactions.append((sender, receiver, amount/100))

    return transactions


def get_or_make_calc(slug):
    cache_keyword = f"members-split-for-{slug}"
    transactions = cache.get(cache_keyword)

    if not transactions:
        gb = GroupBalance.objects.prefetch_related("user")\
            .filter(group__slug=slug)

        balance = {
            str(g.user.username).capitalize(): float(g.balance)
            for g in gb
        }

        print(balance)
        print(cash_flow_finder(balance))

        # transactions = cash_flow_finder(balance)
        transactions = {(payer, receiver): amount
                        for payer, receiver, amount in cash_flow_finder(balance)}
        cache.set(cache_keyword, transactions, timeout=0)
        print("calculation made!")

    return transactions
