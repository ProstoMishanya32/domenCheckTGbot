import aiogram
from create_bot import dp, bot
from aiogram import executor
import asyncio
from handlers import user, domen
from modules import sqlite_logic, check_site

async def on_startup(_):
    print(f"Бот успешно запустился\n{'*' * 50}")
    sqlite_logic.start()
    asyncio.create_task(check_site.startup())


user.registry_handlers_user(dp)
domen.registry_handlers_domen(dp)


if __name__  == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
