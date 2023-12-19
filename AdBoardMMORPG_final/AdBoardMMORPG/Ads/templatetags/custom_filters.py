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


@register.filter(name="cap_case")
def cap_case(value: str):
    return value.capitalize()


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
   d = context['request'].GET.copy()
   for k, v in kwargs.items():
       d[k] = v
   return d.urlencode()

