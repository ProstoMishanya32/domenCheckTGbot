import aiogram
from aiogram import Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import dp, bot
from modules import sqlite_logic, config
from handlers import domen



async def start(message: types.Message, state: FSMContext):
    if message.chat.type == "private":
        await bot.send_message(message.from_user.id, config.text.welcome, parse_mode=types.ParseMode.HTML)
        await domen.Domen.message.set()

async def domen_start(message: types.Message, state: FSMContext):
    if message.chat.type == "private":
        await bot.send_message(message.from_user.id, config.text.add_domen, parse_mode=types.ParseMode.HTML)
        await domen.Domen.message.set()


def registry_handlers_user(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'], state = None)
    dp.register_message_handler(domen_start, commands=['add'], state = None)