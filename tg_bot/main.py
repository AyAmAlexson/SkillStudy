import random
import time
import requests
from deep_translator import GoogleTranslator

from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor


from config import tg_bot_token
from utils import BotStates

bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.answer("Привет, я Канарейка!")
    await message.answer("Вот, что я умею: ")
    await print_bot_menu(message)


@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    await state.reset_state()
    await message.reply("Доступны команды: ", reply = False)
    await print_bot_menu(message)


@dp.message_handler(commands=['password'])
async def password_command(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    await state.set_state(BotStates.all()[5])
    await message.reply("Введите желаемую длину пароля от 4 до 32 символов", reply=False)


@dp.message_handler(commands=['guessing_game_me'])
async def guessing_game_me_command(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    await state.set_state(BotStates.all()[2])
    await message.reply("--- Отлично! Сейчас я загадаю число, а ты будешь угадывать ---", reply=False)
    await message.answer("Выбери уровень сложности:")
    await message.answer("1 - Простой")
    await message.answer("2 - Средний")
    await message.answer("3 - Сложный")


@dp.message_handler(commands=['guessing_game_you'])
async def guessing_game_you_command(message: types.Message):

    global mini
    global maxi
    global guess
    mini = 0
    maxi = 1000
    guess = int((maxi + mini) // 2 + random.randint(-((maxi - mini) // 4), (maxi - mini) // 4))
    await message.reply("--- Отлично! Загадай число от 0 до 1000, а я буду угадывать---", reply=False)
    await message.reply("Готов?", reply=False)
    time.sleep(1)
    await message.reply("Начинаю угадывать", reply=False)
    time.sleep(1)
    await message.reply(f"Это число {guess}?", reply=False)
    time.sleep(1)
    await message.answer("1 - мое число больше")
    await message.answer("2 - мое число меньше")
    await message.answer("3 - БИНГО!!!")
    state = dp.current_state(user=message.from_user.id)
    await state.set_state(BotStates.all()[4])


@dp.message_handler(commands=['i_am_bored'])
async def bored_command(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    await state.set_state(BotStates.all()[0])
    await message.reply("Отлично, сейчас придумаем, чем тебе заняться", reply=False)
    await message.answer("Сколько вас человек?")


@dp.message_handler(state=BotStates.PASSWORD_STATE)
async def get_password(message: types.Message):
    pass_length = message.text
    try:
        pass_length = int(pass_length)
        if pass_length > 32 or pass_length < 4:
            await message.reply("Недопустимый размер пароля")
        else:
            a = "abcdefghijklmnopqrstuvwxyz" * (pass_length // 4)
            b = "ABCDEFGHIJKLMNOPQRSTUVWXYZ" * (pass_length // 4)
            c = "0123456789" * (pass_length // 4)
            d = "!@#$%^&*" * (pass_length // 4)
            fullstack = a + b + c + d

            await message.answer("Создаю сильный пароль, в котором будет хотя бы 1 строчная буква, 1 прописная, "
                                 "1 цифра и 1 специальный символ.")

            password_list = random.sample(fullstack, pass_length - 4)
            password_list.append(random.sample(a, 1)[0])
            password_list.append(random.sample(b, 1)[0])
            password_list.append(random.sample(c, 1)[0])
            password_list.append(random.sample(d, 1)[0])
            random.shuffle(password_list)

            password = "".join(password_list)

            await message.answer("Ваш пароль:\n")
            await message.answer(password)
            time.sleep(3)
            await message.answer("Что будем делать дальше?")
            await print_bot_menu(message)
            state = dp.current_state(user=message.from_user.id)
            await state.reset_state()

    except Exception as ex2:
        print(ex2)
        await message.answer("Необходимо ввести число от 4 до 32")



global the_number


maximum = 10
mini = 0
maxi = 1000
guess = 500


@dp.message_handler(state=BotStates.GAMEME_STATE)
async def game_guessing_bot(message: types.Message):
    global maximum
    global the_number
    lvl = message.text
    try:
        lvl = int(lvl)
        if lvl > 3 or lvl < 1:
            await message.reply("Введи цифру от 1 до 3")
        else:
            if lvl == 1:
                maximum = 10

            elif lvl == 2:
                maximum = 100

            else:
                maximum = 1000

            the_number = random.randint(0, maximum)
            await message.reply(f'Я загадала число от 0 до {maximum}. Угадывай:')
            state = dp.current_state(user=message.from_user.id)
            await state.set_state(BotStates.all()[1])
    except Exception as ex2:
        print(ex2)
        await message.answer("Необходимо ввести число от 1 до 3")


@dp.message_handler(state=BotStates.GAMEME_GUESSING_STATE)
async def game_guessing_bot_guessing(message: types.Message):
    global the_number
    global maximum
    guess = message.text

    try:
        guess = int(guess)
        if guess < the_number:
            await message.answer("Мое число больше. Следующая попытка:")
        elif guess > the_number:
            await message.answer("Мое число меньше. Следующая попытка:")
        else:
            await message.answer(f"БИНГО!!! Я загадала именно {guess}!!!")
            state = dp.current_state(user=message.from_user.id)
            await state.reset_state()
            time.sleep(3)
            await message.answer("Что будем делать дальше?")
            await print_bot_menu(message)

    except Exception as ex2:
        print(ex2)
        await message.answer(f"Необходимо ввести число от 0 до {maximum}")


@dp.message_handler(state=BotStates.GAMEYOU_STATE)
async def game_guessing_user(message: types.Message):
    global mini
    global maxi
    global guess
    ans = message.text
    try:
        ans = int(ans)
        if ans > 3 or ans < 1:
            await message.reply("Введи цифру от 1 до 3")
        else:
            if ans == 1:
                mini = guess + 1
                if maxi == mini:
                    guess = mini
                    await message.answer(f"Я знаю!!! {guess}!!! Отличное число!")
                    state = dp.current_state(user=message.from_user.id)
                    await state.reset_state()
                    time.sleep(5)
                    await message.answer("Что будем делать дальше?")
                    await print_bot_menu(message)
                else:
                    guess = int((maxi + mini) // 2 + random.randint(-((maxi - mini) // 4), (maxi - mini) // 4))
                    await message.answer(f'Это число {guess}?')
                    await message.answer("1 - мое число больше")
                    await message.answer("2 - мое число меньше")
                    await message.answer("3 - БИНГО!!!")
            elif ans == 2:
                maxi = guess - 1
                if maxi == mini:
                    guess = maxi
                    await message.answer(f"Я знаю!!! {guess}!!! Замечательное число!")
                    state = dp.current_state(user=message.from_user.id)
                    await state.reset_state()
                    time.sleep(5)
                    await message.answer("Что будем делать дальше?")
                    await print_bot_menu(message)
                else:
                    guess = int((maxi + mini) // 2 + random.randint(-((maxi - mini) // 4), (maxi - mini) // 4))
                    await message.answer(f'Это число {guess}?')
                    await message.answer("1 - мое число больше")
                    await message.answer("2 - мое число меньше")
                    await message.answer("3 - БИНГО!!!")
            else:
                await message.answer(f"Отлично!!! {guess}!!! Это было очень не просто!")
                state = dp.current_state(user=message.from_user.id)
                await state.reset_state()
                time.sleep(3)
                await message.answer("Что будем делать дальше?")
                await print_bot_menu(message)

    except Exception as ex2:
        print(ex2)
        await message.answer(f"Необходимо ввести число от 1 до 3")
        state = dp.current_state(user=message.from_user.id)
        await state.reset_state()
        time.sleep(5)
        await message.answer("Что будем делать дальше?")
        await print_bot_menu(message)


@dp.message_handler(state=BotStates.BORED_STATE)
async def bored_assist(message: types.Message):

    participants = message.text
    try:
        participants = int(participants)
        if participants >=1 and participants <= 5:
            url = "http://www.boredapi.com/api/activity?participants=" + str(participants)

            activity = requests.get(url).json()

            if int(participants) == 1:
                activity_ru = GoogleTranslator(source='auto', target='ru').translate(
                    activity["activity"]).lower()
                await message.answer(f'Мое предложение: {activity_ru}')
            else:
                activity_ru = GoogleTranslator(source='auto', target='ru').translate("Try "+activity["activity"])
                await message.answer(f'Мое предложение для {str(participants)} участников: {activity_ru}')
            state = dp.current_state(user=message.from_user.id)
            await state.reset_state()
            time.sleep(2)
            await message.answer("Что будем делать дальше?")
            await print_bot_menu(message)
        elif participants>5:
            await message.answer(f'Многовато участников... даже не знаю. Давай попробуем меньше?')
        else:
            await message.answer("Тук-тук! Есть там кто-то??? Люююдиии!")


    except Exception as ex2:
        print(ex2)
        await message.answer(f"Необходимо ввести число")


async def print_bot_menu(message: types.Message):

    await message.answer("/password - сгенерировать пароль")
    await message.answer("/guessing_game_me - я загадаю число, а ты будешь угадывать")
    await message.answer("/guessing_game_you - ты загадаешь число, а я буду угадывать")
    await message.answer("/i_am_bored - (beta) я подскажу, чем заняться, если скучно")
    await message.answer("/help - еще раз расскажу, что я умею")


if __name__ == "__main__":
    executor.start_polling(dp)
