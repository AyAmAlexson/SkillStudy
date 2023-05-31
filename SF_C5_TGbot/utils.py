import json
import requests
from config import CurrencyAPIKEY, keys
class ConversionException(Exception):
    pass

class CurrencyConverter:
    @staticmethod
    def convert(amount: str, base: str, quote: str):

        if base not in keys.keys():
            raise ConversionException(f'Неверный ввод кода валюты {base}')
        if quote not in keys.keys():
            raise ConversionException(f'Неверный ввод кода валюты {quote}')


        try:
            amount = float(amount)
            if amount < 0:
                raise ConversionException('Отрицательное количество')
        except ValueError:
            raise ConversionException(f'Не удалось обработать количество {amount}')

        r = requests.get(
            f'https://api.currencyapi.com/v3/latest?apikey={CurrencyAPIKEY}&currencies={quote}&base_currency={base}')

        result = round(amount * json.loads(r.content)['data'][quote]['value'], 5)
        return result

