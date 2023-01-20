import aiogram
from aiogram import Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import dp, bot
from modules import sqlite_logic, config
from handlers import domen
from keyboards.keyboard import button_admin_menu

class Admin_Menu(StatesGroup):
	message = State()


async def start(message: types.Message, state: FSMContext):
    if message.chat.type == "private":
        await bot.send_message(message.from_user.id, config.text.welcome, parse_mode=types.ParseMode.HTML)
        await domen.Domen.message.set()

async def domen_start(message: types.Message, state: FSMContext):
    if message.chat.type == "private":
        await bot.send_message(message.from_user.id, config.text.add_domen, parse_mode=types.ParseMode.HTML)
        await domen.Domen.message.set()

async def admin_start_menu(message: types.Message, state: FSMContext):
    if message.chat.type == "private":
        if message.from_user.id in config.bot.admin_list:
            await bot.send_message(message.from_user.id, config.text.admin_menu, parse_mode=types.ParseMode.HTML, reply_markup = button_admin_menu)
            await Admin_Menu.message.set()

async def list_domens_command(message: types.Message, state: FSMContext):
    if message.chat.type == "private":
        if message.from_user.id in config.bot.admin_list:
            await list_domens_func(message)

async def admin_menu(message: types.Message, state: FSMContext): #Админ панель
    if message.chat.type == "private": #Проверка, является ль диалог ЛС
        if message.from_user.id in config.bot.admin_list: #Проверка, является ль пользователь Админом
            if message.text == config.buttons.add_domen:
                await bot.send_message(message.from_user.id, config.text.add_domen, parse_mode=types.ParseMode.HTML)
                await domen.Domen.message.set()
            elif message.text == config.buttons.remove_domen:
                await list_domens_func(message)
                await bot.send_message(message.from_user.id, config.text.remove_domen, parse_mode=types.ParseMode.HTML)





async def list_domens_func(message):
    domens = sqlite_logic.get_domens()
    text = ''
    if domens:
        for character in domens:
            text += f"<b>{character[0]} - {character[1]}  </b>\n"
    await bot.send_message(message.from_user.id, f"ID - Домен/Ссылка\n{text}", parse_mode=types.ParseMode.HTML)



def registry_handlers_user(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'], state = None)
    dp.register_message_handler(domen_start, commands=['add'], state = None)
    dp.register_message_handler(list_domens_func, commands=['list'], state=None)
    dp.register_message_handler(admin_start_menu, commands=['admin'], state=None)
    dp.register_message_handler(admin_menu, state = Admin_Menu)