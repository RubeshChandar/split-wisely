from django import template

register = template.Library()


@register.filter(name="abs")
def absolute(value):
    return abs(value)


@register.filter(name='cus_date')
def custom_date_format(value):
    return value.strftime('%d <br> %b <br> <span style="color:red">%Y</span>')


@register.filter(name='check_replace_username_1')
def replace_username_with_you_1(value: str, user: str):
    if (value.capitalize() == user.capitalize()):
        return "<b style='color:red;'>You</b> owe"
    return f"<b>{value}</b> owes"


@register.filter(name='check_replace_username_2')
def replace_username_with_you_2(value: str, user: str):
    if (value.capitalize() == user.capitalize()):
        return "<b style='color:red;'>You</b>"
    return f"<b>{value}</b>"


@register.filter(name='check_replace_username_for_trans')
def replace_username_for_transaction(value, user: str):
    if (value.username.capitalize() == user.capitalize()):
        return "<b>You</b>"
    return value.username.capitalize()
