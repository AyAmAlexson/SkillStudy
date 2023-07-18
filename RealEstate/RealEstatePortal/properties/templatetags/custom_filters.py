from django import template

register = template.Library()

CURRENCIES_SYMBOLS = {
   'eur': '€',
   'usd': '$',
}


# Регистрируем наш фильтр под именем currency, чтоб Django понимал,
# что это именно фильтр для шаблонов, а не простая функция.
@register.filter(name="currency")
def currency(value, code):
    prefix = CURRENCIES_SYMBOLS[code]
    return f'{prefix} {value}'

@register.filter()
def num_censor(value: str):

    value=value.replace("1","one")
    value=value.replace("2", "two")
    value=value.replace("3", "three")
    value=value.replace("3", "four")

    return value