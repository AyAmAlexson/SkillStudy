import telebot
from config import TOKEN, keys
from utils import ConversionException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start','help'])
def help_command(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду в следующем формате: \n <количество валюты> \
<код валюты> \
<код валюты, в которую надо перевести> через пробел.\n\
Пример: 10 USD EUR\n\
Список доступных валют доступен по команде /values'
    bot.reply_to(message,text)

@bot.message_handler(commands=['values'])
def values_command(message: telebot.types.Message):
    text = 'Доступные валюты (коды):\n'
    for key in keys:
        text = text + key + " : " + keys[key] + "\n"
    bot.reply_to(message,text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) > 3:
            raise ConversionException('Слишком много параметров')
        elif len(values) < 3:
            raise ConversionException('Слишком мало параметров')
        amount, base, quote = values[0].upper(), values[1].upper(), values[2].upper()
        total_amount = CurrencyConverter.convert(amount, base, quote)
    except ConversionException as e:
        bot.reply_to(message, f'Ошибка ввода\n{e}')
    except Exception as e:
        bot.reply_to(message,f'Не удалось обработать команду\n{e}')
    else:
        text = f"{amount} {base} = {total_amount} {quote}"
        bot.send_message(message.chat.id, text)


bot.polling()