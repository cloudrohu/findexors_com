from django import template
import re

register = template.Library()

@register.filter
def whatsapp_number(number):
    """
    Clean number and ensure country code (91)
    """
    if not number:
        return ""

    # Remove spaces, +, -
    num = re.sub(r"[^\d]", "", number)

    # If already starts with 91 and length > 10
    if num.startswith("91") and len(num) > 10:
        return num

    # Else assume Indian number
    return "91" + num
