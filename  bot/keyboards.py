from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def dice_game_keyboard():
    keyboard = InlineKeyboardMarkup()
    new_game = InlineKeyboardButton(text="New Game", callback_data="new_game_button")
    keyboard.row(new_game)
    return keyboard
