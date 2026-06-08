from django import template

register = template.Library()

@register.filter
def indian_price(value):
    try:
        value = int(value)
        return "{:,}".format(value)
    except:
        return value