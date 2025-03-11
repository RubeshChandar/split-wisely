from django import template

register = template.Library()


@register.filter(name="abs")
def absolute(value):
    return abs(value)


@register.filter(name='cus_date')
def custom_date_format(value):
    return value.strftime('%d <br> %b <br> <span style="color:red">%Y</span>')
