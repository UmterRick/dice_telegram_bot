from aiogram import types
from setup import bot_dispatcher, bot, logger, executor
from keyboards import dice_game_keyboard
from database.init_db import init_db
games_results = {}

async def init_bot():
    await init_db()

async def init_commands():
    command = types.BotCommand(command="play", description="start new game in dice")
    await bot.set_my_commands(commands=[command])


@bot_dispatcher.message_handler(commands="start", state='*')
async def start_bot(message: types.Message):
    print("User press START")

    await message.answer("Привіт друже", reply_markup=dice_game_keyboard())


@bot_dispatcher.message_handler(commands="play", state='*')
async def test_bot(message: types.Message):
    print("User press PLAY")
    bot_dice_msg = await bot.send_dice(message.chat.id)
    games_results[bot_dice_msg.chat.id] = bot_dice_msg.dice.value
    print(games_results)
    await bot.send_message(bot_dice_msg.chat.id, "Your Turn")


@bot_dispatcher.message_handler(content_types=["dice"])
async def reply_to_b_(message):
    print(message.__dict__)
    print(games_results)
    if message.dice.value > games_results[message.chat.id]:
        await message.answer("You WIN")
    elif message.dice.value == games_results[message.chat.id]:
        await message.answer("Draw")
    else:
        await message.answer("You LOSE, try again: /play")


@bot_dispatcher.callback_query_handler()
async def handle_keyboard(call: types.CallbackQuery):
    print(dir(call))
    print(call.__dict__.items())
    await call.answer("Callback notification", show_alert=False)
    await call.message.answer("You pressed keyboard button")

if __name__ == "__main__":
    logger.info("Start polling...")
    executor.start_polling(bot_dispatcher)
