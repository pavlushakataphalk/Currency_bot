from aiogram import executor, types
import datetime
from course_request import getCurrentCourse
from keyboards import mykb, mykb_adm, panel
from bot import dp

coeff = 1.06


def get_value(coeff):
    curreu = str(round(float(getCurrentCourse()) * coeff, 2))
    fin = "@computer_craft выдаст наличные евро, с вас перевод на карту сбербанка или другого российского банка. Курс обмена евро - " + curreu + " руб.\n" + "\n" + "Возможен обмен в обратную сторону. Курс уточняйте.\n" + "\n" + "Покупаем криптовалюту. Курс уточняйте."
    return fin


print(get_value(coeff))

users_list_1hr = []
users_list_modified = []
users_counter = 0
start = datetime.datetime.now()


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
                    k = k + 1

        if k == 0 and message.from_user.username != 'pashaborsch' and message.from_user.username != 'Computer_craft' and message.from_user.username is not None:
            users_list_1hr.append(message.from_user.username)
            users_list_modified.append("@" + message.from_user.username)
            users_counter = users_counter + 1

    users_list_check(message)

    print(message.from_user.username)
    if message.from_user.username == 'pashaborsch' or message.from_user.username == 'Computer_craft':
        await message.answer("Нажмите для доступа к админской панели:", reply_markup=mykb_adm)


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
            users_list_1hr.append(query.from_user.username)
            users_list_modified.append("@" + query.from_user.username)
            users_counter = users_counter + 1

    users_list_check(query)
    date = (datetime.datetime.now() + datetime.timedelta(hours=-1)).strftime("%d/%m/%Y, %H:%M")
    await query.answer("Курс обновлен " + date)


@dp.callback_query_handler(text="adm")
async def admin_kb(query: types.CallbackQuery):
    perc = round(((coeff - 1) * 100), 2)
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
        await query.message.answer(
            "Пользователи (" + str(users_counter) + ") за последний час:" + "\n" + '\n'.join(users_list_modified))


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
        coeff = float(message.text) / 100 + 1
        date = (datetime.datetime.now() + datetime.timedelta(hours=-1)).strftime("%d/%m/%Y, %H:%M")
        await message.answer("Коэффициент обновлен " + date)
    else:
        await message.reply("Ошибка ввода, попробуйте еще раз:")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
