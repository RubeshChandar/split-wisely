from django import template

register = template.Library()


@register.filter(name="abs")
def absolute(value):
    return abs(value)
