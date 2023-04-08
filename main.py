import requests
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bs4 import BeautifulSoup
import datetime

EURO_RUB = 'https://www.google.com/search?q=euro+to+ruble&newwindow=1&sxsrf=APwXEde8pFrfqho1nOYcU2NFF-_YaVBCCg%3A1680350839745&ei=dx4oZP_5LLKB9u8P_v-OwAs&ved=0ahUKEwi_kZrX0oj-AhWygP0HHf6_A7gQ4dUDCA8&uact=5&oq=euro+to+ruble&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQAzIMCAAQigUQQxBGEIICMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEOgoIABBHENYEELADOgoIABCKBRCwAxBDOgQIIxAnOgoILhDHARDRAxAnOgsILhCABBDHARDRAzoHCAAQigUQQzoHCC4QigUQQzoQCC4QigUQxwEQ0QMQ1AIQQzoHCAAQgAQQCjoKCAAQgAQQFBCHAjoPCAAQgAQQFBCHAhBGEIICSgQIQRgAUIEIWLIeYL4iaAFwAXgAgAH0AYgBrAySAQU1LjcuMZgBAKABAcgBCsABAQ&sclient=gws-wiz-serp'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}


def get_value():
    full_page = requests.get(EURO_RUB, headers=headers)
    soup = BeautifulSoup(full_page.content, 'html.parser')
    convert = soup.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": 2})
    print(convert[0].text)
    curreu = str(round(float(convert[0].text.replace(',', '.'))*1.05, 2))
    currdin = str(round(float(convert[0].text.replace(',', '.'))*1.05/117, 2))
    fin = "Актуальный курс Евро (EUR):\n" + curreu + "\n" + "Актуальный курс Сербского Динара(RSD):\n"+ currdin
    return fin


get_value()

API_TOKEN = '5653760842:AAHlXeWckFJj_OVHixjSt1ySw9ps6yPYH_g'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


mykb = InlineKeyboardMarkup(row_width=1)
mybt = InlineKeyboardButton(text="Обновить курс", callback_data="refresh")
mykb.add(mybt)

@dp.message_handler(commands=['start','refresh'])
async def cmd_start(message: types.Message):
    await message.reply(get_value(), reply_markup=mykb)

@dp.callback_query_handler(text="refresh")
async def send_welcome(query: types.CallbackQuery):
    if query.message.text != get_value():
     await query.message.edit_text(get_value(), reply_markup=mykb)

    date = (datetime.datetime.now()+datetime.timedelta(hours=-1)).strftime("%d/%m/%Y, %H:%M")
    await query.answer("Курс обновлен " + date)
    await query.message.edit_text(get_value(), reply_markup=mykb)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
