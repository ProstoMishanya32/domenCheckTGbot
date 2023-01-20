import aiogram
from aiogram import Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import dp, bot
from modules import sqlite_logic, config, json_logic
from handlers import domen, admin
from keyboards.keyboard import button_admin_menu, button_admin_return


async def start(message: types.Message, state: FSMContext):
    admins = await json_logic.get_admins()
    if message.chat.type == "private":
        if message.from_user.id in admins:
            await bot.send_message(message.from_user.id, config.text.welcome, parse_mode=types.ParseMode.HTML)
            await domen.Domen.message.set()

async def domen_start(message: types.Message, state: FSMContext):
    admins = await json_logic.get_admins()
    if message.chat.type == "private":
        if message.from_user.id in admins:
            await bot.send_message(message.from_user.id, config.text.add_domen, parse_mode=types.ParseMode.HTML )
            await domen.Domen.message.set()

async def admin_start_menu(message: types.Message, state: FSMContext):
    admins = await json_logic.get_admins()
    if message.chat.type == "private":
        if message.from_user.id in admins:
            await bot.send_message(message.from_user.id, config.text.admin_menu, parse_mode=types.ParseMode.HTML, reply_markup = button_admin_menu)
            await admin.Admin_Menu.message.set()

async def list_domens_command(message: types.Message, state: FSMContext):
    admins = await json_logic.get_admins()
    if message.chat.type == "private":
        if message.from_user.id in admins:
            await admin.list_domens_func(message)


def registry_handlers_user(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'], state = None)
    dp.register_message_handler(domen_start, commands=['add'], state = None)
    dp.register_message_handler(list_domens_command, commands=['list'], state=None)
    dp.register_message_handler(admin_start_menu, commands=['admin'], state=None)