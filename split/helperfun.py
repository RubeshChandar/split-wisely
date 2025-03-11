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
