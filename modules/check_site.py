import requests
from bs4 import BeautifulSoup
import lxml
from modules import sqlite_logic, config, json_logic
import aiogram
from aiogram import Dispatcher, types
from create_bot import dp, bot
import asyncio

HEADERS = {
    'User-Agent': ('Mozilla/5.0 (Windows NT 6.0; rv:14.0) Gecko/20100101 '
                   'Firefox/14.0.1'),
    'Accept':
    'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language':
    'ru-ru,ru;q=0.8,en-us;q=0.5,en;q=0.3',
    'Accept-Encoding':
    'gzip, deflate',
    'Connection':
    'keep-alive',
    'DNT':
    '1'
}


def check_site(url, params = HEADERS):
	try:
		response = requests.get(url, headers=HEADERS)
		return  response
	except requests.exceptions.ConnectionError: #Не подключился
		response = False
		return response

async def check_steam(url, message, params = HEADERS, ):
	try:
		sqlite_logic.add_url(url) #Добавление в БД новую запись, если существует - игнор
		if "http:/" in url or "https:/" in url: #Повторная проверка
			url_check = f"https://steamcommunity.com/linkfilter/?url={url}" # Данный URL отображает заблокирован ль сайт/домен
		elif ".com" in url or ".ru" and "http:/" not in url or "https:/" not in url : #Если в ссылке есть домены
			url_check = f"https://steamcommunity.com/linkfilter/?url=http://%22{url}%22"
		else: #Если в ссылке нету
			url_check = f"https://steamcommunity.com/linkfilter/?url=http://%22{url+'.com'}%22"
		response = requests.get(url_check, params = params) # Подключение к Steam
		soup = BeautifulSoup(response.text, 'lxml').find('h1') #Поиск заголовка
		if "Link Blocked!" == soup.text : # Заблокирована ль ссылка
			sqlite_logic.update_steam(url, 1)  # Steam Заблокировкал Статус 1 в БД
			await check_google(url, message)
		else:
			sqlite_logic.update_steam(url, 0) # Блокировки в Steam нет
			await check_google(url, message)
	except Exception as i:
		print(i)

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"


async def check_google(url, message):
	try:
		if "http:/" in url or "https:/" in url:  # Повторная проверка
			url_check = url
		elif ".com" in url or ".ru" and "http:/" not in url or "https:/" not in url:  # Если в ссылке есть домены
			url_check = f"https://{url}"
		else:  # Если в ссылке нету
			url_check = f"https://{url + '.com'}"

		query = f"site:{url_check}"
		query = query.replace(' ', '+')
		URL = f"https://google.com/search?q={query}"
		headers = {"user-agent" : USER_AGENT}
		resp = requests.get(URL, headers=headers)

		if resp.status_code == 200:
			soup = BeautifulSoup(resp.content, "html.parser")
			if "ничего не найдено." in soup.text: # Банальная проверка
				sqlite_logic.update_google(url, 1) # Заблокирован
			else:
				sqlite_logic.update_google(url, 0) #Бана нет
		else:
			sqlite_logic.update_google(url, 0) #На случай если блоканет запрос

		status, steam, google = sqlite_logic.get_data(url)
		#TODO Дичайшик колхоз, в будущем исправить
		if status[0] == None:
			status = 'Сайт активен ✅ '
		else:
			status = 'Сайт не активен ❌'
		if steam[0] == 1:
			steam = 'Блокировка в Steam ❌'
		else:
			steam = 'Не заблокирован  в Steam ✅'
		if google[0] == 1:
			google = "Блокировка в Google ❌"
		else:
			google = "Не заблокирован в Google ✅"
		if message == None:
			admins = await json_logic.get_admins()
			for i in admins:
				await bot.send_message(i, f"Сайт - <b>{url}</b> На данный момент: <i>\n{status}\n{steam}\n{google}\n</i>", parse_mode=types.ParseMode.HTML)
		else:
			await bot.send_message(message.from_user.id, f"Сайт - <b>{url}</b> На данный момент: <i>\n{status}\n{steam}\n{google}\n</i>",   parse_mode=types.ParseMode.HTML)
	except Exception as i:
		print(i)


async def startup():
	while True:
		time = json_logic.get_time()
		await asyncio.sleep(time)
		url = sqlite_logic.get_url()
		for i in url:
			url = i[0]
			await check_steam(url, None)