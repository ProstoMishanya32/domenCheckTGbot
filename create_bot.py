from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import  MemoryStorage
from modules import config


storage = MemoryStorage()
bot = Bot(token = config.bot.token)
dp = Dispatcher(bot, storage = storage)