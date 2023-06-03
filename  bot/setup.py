from aiogram import Bot, Dispatcher
from aiogram.utils.executor import Executor
import logging
from config import TOKEN

bot = Bot(token=TOKEN)
bot_dispatcher = Dispatcher(bot=bot)


def conf_logger():
    l = logging.getLogger('bot')

    # Create handlers
    c_handler = logging.StreamHandler()
    f_handler = logging.FileHandler('bot.log')
    c_handler.setLevel(logging.WARNING)
    f_handler.setLevel(logging.ERROR)

    # Create formatters and add it to handlers
    c_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)

    # Add handlers to the logger
    l.addHandler(c_handler)
    l.addHandler(f_handler)

    return l


logger = conf_logger()

executor = Executor(bot_dispatcher, skip_updates=True)
