from django import template

register = template.Library()


@register.filter
def to_percentage(value, base=5):
    try:
        return int(float(value) / base * 100)
    except (ValueError, TypeError):
        return 0
