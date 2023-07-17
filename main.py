from requests import get
from time import time
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from selenium import webdriver
import datetime

from selenium.webdriver.common.by import By

#from apscheduler.schedulers.asyncio import AsyncIOScheduler

EURO_RUB = 'https://www.vbr.ru/banki/bks-bank/kurs-valut/eur/?utm_referrer=https%3A%2F%2Fwww.google.com%2F'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}

coeff = 1.06
rate = 0


def getCurrentCourse():
    params = {
        "symbol": "EUR_RUB__TOD",
        "classcode": "CETS",
        "resolution": 60,
        "from": round(time() - 72 * 3600),
        "to": round(time())
    }
    response = get("https://api.bcs.ru/udfdatafeed/v1/history", params)
    data = response.json()
    if response:
        result = data.get("c")[-1] if data.get("c") else None
    else:
        result = None
    return result


def get_value(coeff):
    curreu = str(round(float(getCurrentCourse())*coeff, 2))
    fin = "@computer_craft выдаст наличные евро, с вас перевод на карту сбербанка или другого российского банка. Курс обмена евро - " + curreu + " руб.\n" + "\n" + "Возможен обмен в обратную сторону. Курс уточняйте.\n" + "\n" + "Покупаем криптовалюту. Курс уточняйте."
    return fin



print(get_value(coeff))

API_TOKEN = '5653760842:AAHlXeWckFJj_OVHixjSt1ySw9ps6yPYH_g'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

users_list_1hr = []
users_list_modified = []
users_counter = 0
start = datetime.datetime.now()


async def send_list_m(message):
    await bot.send_message("Пользователи (" + str(users_counter) + ") за последний час:" + "\n" + '\n'.join(users_list_modified), chat_id='772007607')


async def schedule_refresher_m(message):
    global users_counter, users_list_1hr
    await send_list_m(message)
    users_list_1hr.clear()
    users_counter = 0


async def auto_sender_m(message: types.Message):
    global start
    start = datetime.datetime.now()
    time_difference = datetime.datetime.now() - start
    if time_difference.total_seconds() >= 10:
        await schedule_refresher_m(message)
        start = datetime.datetime.now()


async def send_list_q(query):
    await bot.send_message("Пользователи (" + str(users_counter) + ") за последний час:" + "\n" + '\n'.join(users_list_1hr), chat_id='772007607')


async def schedule_refresher_q(query):
    global users_counter, users_list_1hr
    await send_list_q(query)
    users_list_1hr.clear()
    users_counter = 0


async def auto_sender_q(query: types.CallbackQuery):
    global start
    start = datetime.datetime.now()
    time_difference = datetime.datetime.now() - start
    if time_difference.total_seconds() >= 3600:
        await schedule_refresher_q(query)
        start = datetime.datetime.now()


mykb = InlineKeyboardMarkup(row_width=1)
mybt = InlineKeyboardButton(text="Обновить курс", callback_data="refresh")
mykb.add(mybt)


mykb_adm = InlineKeyboardMarkup(row_width=1)
bt_adm = InlineKeyboardButton(text="Админская панель", callback_data="adm")
mykb_adm.add(bt_adm)


panel = InlineKeyboardMarkup(row_width=1)
panel_bt1 = InlineKeyboardButton(text="Изменить коэффициент", callback_data="edit")
panel_bt2 = InlineKeyboardButton(text="Назад", callback_data="back")
panel_bt3 = InlineKeyboardButton(text="Список пользователей за последний час", callback_data="get_list")
panel.add(panel_bt1, panel_bt2, panel_bt3)


@dp.message_handler(commands=['start', 'refresh'])
async def cmd_start(message: types.Message):
    print(message.from_user.username)
    await message.reply(get_value(coeff), reply_markup=mykb)
    def users_list_check(message: types.Message):
        global users_counter
        k = 0
        if message.from_user.username != 'pashaborsch' and message.from_user.username != 'Computer_craft' and message.from_user.username is not None:
            for i in range(0, users_counter):
                if message.from_user.username == users_list_1hr[i]:
                    k = k+1

        if k == 0 and message.from_user.username != 'pashaborsch' and message.from_user.username != 'Computer_craft' and message.from_user.username is not None:
            username_modified = "@" + message.from_user.username
            users_list_1hr.append(message.from_user.username)
            users_list_modified.append(username_modified)
            users_counter = users_counter + 1

        print('\n'.join(str(k)))
        print('\n'.join(str(users_counter)))

    users_list_check(message)

    print(message.from_user.username)
    if message.from_user.username == 'pashaborsch' or message.from_user.username == 'Computer_craft':
        await message.answer("Нажмите для доступа к админской панели:", reply_markup=mykb_adm)

    await auto_sender_m(message)


@dp.callback_query_handler(text="refresh")
async def send_welcome(query: types.CallbackQuery):
    print(query.from_user.username)
    mykb.clean()
    if query.message.text != get_value(coeff):
        await query.message.edit_text(get_value(coeff), reply_markup=mykb)

    def users_list_check(query: types.CallbackQuery):
        global users_counter
        k = 0
        if query.from_user.username != 'pashaborsch' or query.from_user.username != 'Computer_craft':
            for i in range(0, users_counter):
                if query.from_user.username == users_list_1hr[i]:
                    k = k + 1

        if k == 0 and query.from_user.username != 'pashaborsch' and query.from_user.username != 'Computer_craft' and query.from_user.username is not None:
            username_modified = "@" + query.from_user.username
            users_list_1hr.append(query.from_user.username)
            users_list_modified.append(username_modified)
            users_counter = users_counter + 1

        print('\n'.join(str(k)))
        print('\n'.join(str(users_counter)))

    users_list_check(query)
    date = (datetime.datetime.now() + datetime.timedelta(hours=-1)).strftime("%d/%m/%Y, %H:%M")
    await query.answer("Курс обновлен " + date)
    await auto_sender_q(query)


@dp.callback_query_handler(text="adm")
async def admin_kb(query: types.CallbackQuery):
    perc = round(((coeff-1)*100), 2)
    await query.message.answer("Текущий коэффициент = " + str(perc) + "\n", reply_markup=panel)


@dp.callback_query_handler(text="edit")
async def edit(query: types.CallbackQuery):
    await query.message.answer("Введите новый коэффициент:")


@dp.callback_query_handler(text="back")
async def back(query: types.CallbackQuery):
        await query.message.answer(get_value(coeff), reply_markup=mykb)
        print(query.from_user.username)
        if query.from_user.username == 'pashaborsch' or query.from_user.username == 'Computer_craft':
            await query.message.answer("Нажмите для доступа к админской панели:", reply_markup=mykb_adm)


@dp.callback_query_handler(text="get_list")
async def get_list(query: types.CallbackQuery):
    print('\n'.join(users_list_1hr))
    if query.from_user.username == 'pashaborsch' or query.from_user.username == 'Computer_craft':
        await query.message.answer("Пользователи (" + str(users_counter) +") за последний час:" + "\n" + '\n'.join(users_list_1hr))


@dp.message_handler()
async def coeff_handler(message: types.Message):
    def check():
        try:
            float(message.text)
            return True
        except ValueError:
            return False

    if check():
        global coeff
        coeff = float(message.text)/100+1
        date = (datetime.datetime.now() + datetime.timedelta(hours=-1)).strftime("%d/%m/%Y, %H:%M")
        await message.answer("Коэффициент обновлен " + date)
    else:
        await message.reply("Ошибка ввода, попробуйте еще раз:")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
