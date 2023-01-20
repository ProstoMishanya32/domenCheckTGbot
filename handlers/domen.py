import aiogram
from aiogram import Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import dp, bot
from modules import sqlite_logic, config, check_site

class Domen(StatesGroup):
	message = State()

async def message_start(message: types.Message, state: FSMContext):
    await state.finish()
    if "http:/" in message.text or "https:/" in message.text:
        url = message.text
    else:
        if ".com" in message.text or ".ru" in message.text:
            url = f"https://{message.text}"
        else:
            url = f"https://{message.text}.com"
    print(url)
    response = check_site.check_site(url)  # Проверка на статус сайт
    if response != False:
        if response.status_code == 200:
            await check_site.check_steam(message.text, message) # Начало проверки
        else:
            sqlite_logic.update_notactive(message.text, message) #Добавление в базу данных со статусом NOTACTIVE
    else:
        await bot.send_message(message.from_user.id, config.text.errorconection, parse_mode=types.ParseMode.HTML)
def registry_handlers_domen(dp: Dispatcher):
    dp.register_message_handler(message_start, state = Domen.message)
