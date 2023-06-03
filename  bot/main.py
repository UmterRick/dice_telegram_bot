import asyncio
import datetime

from aiogram import types
from setup import bot_dispatcher, bot, logger, executor
from keyboards import dice_game_keyboard, dice_try_again, dice_game_keyboard_reply
from database.init_db import init_db, get_conn

games = {}


async def init_bot(*args, **kwargs):
    print(args, kwargs)
    await init_db()


async def init_commands():
    command = types.BotCommand(command="play", description="start new game in dice")
    await bot.set_my_commands(commands=[command])


@bot_dispatcher.message_handler(commands="start", state='*')
async def start_bot(message: types.Message):
    print("User press START")

    await message.answer(f"Привіт друже (Your Id is {message.chat.id})", reply_markup=dice_game_keyboard_reply())


@bot_dispatcher.message_handler(commands="play", state='*')
async def test_bot(message: types.Message):
    bot_dice_msg = await bot.send_dice(message.chat.id)

    conn = await get_conn()
    cursor = await conn.cursor()
    await cursor.execute(f"""
    INSERT INTO games_results (chat_id, user_score, bot_score, game_type, timestamp) 
    VALUES (%s, %s, %s, %s, %s) RETURNING game_id
    """, (bot_dice_msg.chat.id, 0, bot_dice_msg.dice.value, "DICE", datetime.datetime.now().timestamp()))
    game_id = await cursor.fetchone()
    games[bot_dice_msg.chat.id] = game_id[0]
    await bot.send_message(bot_dice_msg.chat.id, "Your Turn")


@bot_dispatcher.message_handler(content_types=["dice"])
async def reply_to_b_(message):
    conn = await get_conn()
    cursor = await conn.cursor()

    await cursor.execute("""
    UPDATE games_results SET user_score = %s WHERE game_id = %s RETURNING bot_score
    """, (message.dice.value, games[message.chat.id]))
    bot_score = await cursor.fetchone()

    if message.dice.value > bot_score[0]:
        await message.answer("You WIN", reply_markup=dice_try_again())
    elif message.dice.value == bot_score[0]:
        await message.answer("Draw", reply_markup=dice_try_again())
    else:
        await message.answer("You LOSE, try again", reply_markup=dice_try_again())


@bot_dispatcher.callback_query_handler(lambda c: c.data in ["new_dice_game_button", "again_dice_game_button"])
async def handle_keyboard(call: types.CallbackQuery):
    bot_dice_msg = await bot.send_dice(call.message.chat.id)

    conn = await get_conn()
    cursor = await conn.cursor()
    await cursor.execute(f"""
        INSERT INTO games_results (chat_id, user_score, bot_score, game_type, timestamp) 
        VALUES (%s, %s, %s, %s, %s) RETURNING game_id
        """, (bot_dice_msg.chat.id, 0, bot_dice_msg.dice.value, "DICE", datetime.datetime.now().timestamp()))
    game_id = await cursor.fetchone()
    games[bot_dice_msg.chat.id] = game_id[0]
    await bot.send_message(bot_dice_msg.chat.id, "Your Turn")


@bot_dispatcher.callback_query_handler(lambda c: c.data == "new_darts_game_button")
async def handle_keyboard(call: types.CallbackQuery):
    await call.answer("Callback notification", show_alert=False)
    await call.message.answer("You pressed DARTS button")


if __name__ == "__main__":
    logger.info("Start polling...")
    executor.on_startup(init_bot)
    executor.start_polling(bot_dispatcher)
