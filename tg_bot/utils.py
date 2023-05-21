from aiogram.utils.helper import Helper, HelperMode, ListItem

class BotStates(Helper):
    mode = HelperMode.snake_case

    BORED_STATE = ListItem() #0
    PASSWORD_STATE = ListItem() #5
    GAMEME_STATE = ListItem() #2
    GAMEME_GUESSING_STATE = ListItem() #1
    GAMEYOU_STATE = ListItem() #4
    GAMEYOU_GUESSING_STATE = ListItem() #3
