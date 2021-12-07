from django import template

register = template.Library()


@register.simple_tag()
def percent(x, y, *args, **kwargs):
    return round(x * 100 / y)


@register.simple_tag()
def textSlice(text, *args, **kwargs):
    return ' '.join(text.split()[:5]) + '...'
