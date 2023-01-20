import aiogram
from aiogram import Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import dp, bot
from modules import sqlite_logic, config, json_logic
from handlers import domen
from keyboards.keyboard import button_admin_menu, button_admin_return

class Admin_Menu(StatesGroup):
	message = State()


async def admin_menu(message: types.Message, state: FSMContext): #Админ панель
    admins = await json_logic.get_admins()
    if message.chat.type == "private": #Проверка, является ль диалог ЛС
        if message.from_user.id in admins: #Проверка, является ль пользователь Админом
            if message.text == config.buttons.add_domen:
                await bot.send_message(message.from_user.id, config.text.add_domen, parse_mode=types.ParseMode.HTML)
                await domen.Domen.message.set()
            elif message.text == config.buttons.remove_domen:
                await list_domens_func(message)
                await bot.send_message(message.from_user.id, config.text.remove_domen, parse_mode=types.ParseMode.HTML, reply_markup = button_admin_return)
                await Delete_domen.message.set()
            elif message.text == config.buttons.list_domens:
                await list_domens_func(message)
            elif message.text == config.buttons.change_time:
                await get_time_func(message)
                await bot.send_message(message.from_user.id, config.text.time_count, parse_mode=types.ParseMode.HTML,  reply_markup=button_admin_return)
                await Change_time.message.set()
            elif message.text == config.buttons.add_admin:
                await bot.send_message(message.from_user.id, config.text.add_admin, parse_mode=types.ParseMode.HTML,  reply_markup=button_admin_return)
                await Add_admin.message.set()
            elif message.text == config.buttons.remove_admin:
                await see_admin(message)
                await bot.send_message(message.from_user.id, config.text.remove_admin, parse_mode=types.ParseMode.HTML,  reply_markup=button_admin_return)
                await Remove_admin.message.set()
            elif message.text == config.buttons.exit:
                await bot.send_message(message.from_user.id, config.text.succesfully, parse_mode=types.ParseMode.HTML)
                await state.finish()

class Delete_domen(StatesGroup):
	message = State()

async def delete_domen(message: types.Message, state: FSMContext):
    if message.text == config.buttons.return_back:
        await bot.send_message(message.from_user.id, config.text.admin_menu, parse_mode=types.ParseMode.HTML, reply_markup=button_admin_menu)
        await Admin_Menu.message.set()
    else:
        try:
            int(message.text)
            result  = sqlite_logic.delete_domen(message.text)
            if result:
                await bot.send_message(message.from_user.id, config.text.succesfully, parse_mode=types.ParseMode.HTML, reply_markup = button_admin_menu)
                await Admin_Menu.message.set()
            else:
                await bot.send_message(message.from_user.id, config.text.error_sqlite, parse_mode=types.ParseMode.HTML, reply_markup = button_admin_menu)

        except ValueError:
            await bot.send_message(message.from_user.id, config.text.error_int, parse_mode=types.ParseMode.HTML)

class Change_time(StatesGroup):
	message = State()
async def сhange_time(message: types.Message, state: FSMContext):
    if message.text == config.buttons.return_back:
        await bot.send_message(message.from_user.id, config.text.admin_menu, parse_mode=types.ParseMode.HTML, reply_markup=button_admin_menu)
        await Admin_Menu.message.set()
    else:
        try:
            int(message.text)
            result = json_logic.change_time(int(message.text))
            if result:
                await bot.send_message(message.from_user.id, config.text.succesfully, parse_mode=types.ParseMode.HTML, reply_markup = button_admin_menu)
                await Admin_Menu.message.set()
            else:
                await bot.send_message(message.from_user.id, config.text.error_sqlite, parse_mode=types.ParseMode.HTML, reply_markup = button_admin_menu)

        except ValueError:
            await bot.send_message(message.from_user.id, config.text.error_int, parse_mode=types.ParseMode.HTML)

class Add_admin(StatesGroup):
	message = State()

async def add_admin(message: types.Message, state: FSMContext):
    try:
        if message.text == config.buttons.return_back:
            await bot.send_message(message.from_user.id, config.text.admin_menu, parse_mode=types.ParseMode.HTML,      reply_markup=button_admin_menu)
            await Admin_Menu.message.set()
        else:
            user_id = message['forward_from']['id']
            if message['forward_from']['last_name'] == None:
                nickname = message['forward_from']['first_name']
            else:
                nickname = f"{message['forward_from']['first_name']} {message['forward_from']['last_name']}"
            await json_logic.add_admin(user_id, nickname)
            await bot.send_message(message.from_user.id, config.text.succesfully, parse_mode=types.ParseMode.HTML, reply_markup = button_admin_menu)
            await Admin_Menu.message.set()
    except Exception as i:
        print(i)
    except TypeError:
        await bot.send_message(message.from_user.id, config.text.error_admin, parse_mode=types.ParseMode.HTML)
        await Add_admin.message.set()


class Remove_admin(StatesGroup):
    message = State()
async def remove_admin(message: types.Message, state: FSMContext):
    if message.text == config.buttons.return_back:
        await bot.send_message(message.from_user.id, config.text.admin_menu, parse_mode=types.ParseMode.HTML,  reply_markup=button_admin_menu)
        await Admin_Menu.message.set()
    else:
        remove = await json_logic.remove_admin(message.text)
        if remove == True:
            await bot.send_message(message.from_user.id, config.text.succesfully, reply_markup = button_admin_menu)
            await Admin_Menu.message.set()
        else:
            await bot.send_message(message.from_user.id, config.text.not_finden)





async def get_time_func(message):
    time = json_logic.get_time()
    await bot.send_message(message.from_user.id, config.text.time_get.format(time_count = int(time/60)), parse_mode=types.ParseMode.HTML)

async def list_domens_func(message):
    domens = sqlite_logic.get_domens()
    text = ''
    if domens:
        for character in domens:
            text += f"<b>{character[0]} - {character[1]}  </b>\n"
    await bot.send_message(message.from_user.id, f"ID - Домен/Ссылка\n{text}", parse_mode=types.ParseMode.HTML)


async def see_admin(message):
    admins = await json_logic.see_admins()
    text = ''
    if admins:
        for character in admins:
            text += f"<b> #{character['position']}  {character['nickname']} || {character['user_id']}</b>\n"
        await bot.send_message(message.from_user.id, text, parse_mode=types.ParseMode.HTML)



def registry_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(admin_menu, state = Admin_Menu.message)
    dp.register_message_handler(delete_domen, state=Delete_domen.message)
    dp.register_message_handler(сhange_time , state=Change_time.message)
    dp.register_message_handler(add_admin, state=Add_admin.message)
    dp.register_message_handler(remove_admin, state=Remove_admin.message)