from django import template
import time

register = template.Library()
@register.tag
@register.filter
def bust_cache(value):
    return f"{value}?{str(int(time.time()))}"



