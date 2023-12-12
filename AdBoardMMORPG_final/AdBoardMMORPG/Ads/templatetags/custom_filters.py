from django import template


register = template.Library()


@register.filter(name="hide_pass")
def hide_pass(value: str):
    return '*' * len(value)


@register.filter(name="to_int")
def to_int(value):
    return int(value)


@register.filter(name='get')
def get(dictionary, key):
    return dictionary.get(key, None)

