from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from aiogram.types.reply_keyboard import KeyboardButton
def dice_game_keyboard_reply():
    keyboard = ReplyKeyboardMarkup()
    new_game_1 = KeyboardButton(text="New DICE Game", callback_data="new_dice_game_button")
    new_game_2 = KeyboardButton(text="New DARTS Game", callback_data="new_darts_game_button")

    keyboard.row(new_game_1)
    keyboard.row(new_game_2)
    return keyboard

def dice_game_keyboard():
    keyboard = InlineKeyboardMarkup()
    new_game_1 = InlineKeyboardButton(text="New DICE Game", callback_data="new_dice_game_button")
    new_game_2 = InlineKeyboardButton(text="New DARTS Game", callback_data="new_darts_game_button")

    keyboard.row(new_game_1)
    keyboard.row(new_game_2)
    return keyboard

def dice_try_again():
    keyboard = InlineKeyboardMarkup()
    new_try = InlineKeyboardButton(text="Try Again", callback_data="again_dice_game_button")

    keyboard.row(new_try)
    return keyboard