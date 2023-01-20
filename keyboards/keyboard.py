from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardButton
from modules import config

button_admin_menu = ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True).add(KeyboardButton(
	config.buttons.add_domen)).insert(KeyboardButton(
	config.buttons.remove_domen)).add(KeyboardButton(
	config.buttons.list_domens)).insert(KeyboardButton(
	config.buttons.change_time)).add(KeyboardButton(
	config.buttons.add_admin)).insert(KeyboardButton(
	config.buttons.remove_admin)).add(KeyboardButton(
	config.buttons.exit))

button_admin_return = ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True).add(KeyboardButton(
	config.buttons.return_back))