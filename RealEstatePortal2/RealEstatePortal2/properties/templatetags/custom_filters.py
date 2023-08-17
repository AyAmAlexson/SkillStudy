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

@register.filter(name="hide_pass")
def hide_pass(value: str):
    return '*' * len(value)


@register.filter(name="cap_case")
def cap_case(value: str):
    return value.capitalize()

@register.filter()
def num_censor(value: str):

    value=find_last_level(value,value)
    value = value.replace("/"," ")
    value = value.capitalize()
    return value

def find_last_level(s:str, prev_s:str):
    if (s.find("/") == -1):
        return prev_s
    else:
        prev_s=find_last_level(s[s.find("/")+1:],s)
        return prev_s

@register.filter()
def minus_ref(value:str):
    value=str(value)
    value = value[value.find("-")+2:]

    return value

@register.filter()
def ql_link(value):
    return f'https://www.quicklets.com.mt/property-detail/{value-199}'


