from aiogram import executor, types
import datetime
from course_request import getCurrentCourse
from keyboards import mykb, mykb_adm, panel
from bot import dp

coeff = 1.06


def get_value(coeff): # the main function of currency bot which gets currency with request and changes it
    curreu = str(round(float(getCurrentCourse()) * coeff, 2))
    fin = "here should be your main message for user" + curreu
    return fin


print(get_value(coeff)) //

users_list_1hr = []
users_list_modified = []
users_counter = 0


@dp.message_handler(commands=['start', 'refresh'])
async def cmd_start(message: types.Message):
    print(message.from_user.username)
    await message.reply(get_value(coeff), reply_markup=mykb)

    def users_list_check(message: types.Message):
        global users_counter
        k = 0
        if message.from_user.username != 'admin_telegram_nickname' and message.from_user.username is not None:
            for i in range(0, users_counter):
                if message.from_user.username == users_list_1hr[i]:
                    k = k + 1

        if k == 0 and message.from_user.username != 'admin_telegram_nickname' and message.from_user.username is not None:
            users_list_1hr.append(message.from_user.username)
            users_list_modified.append("@" + message.from_user.username)
            users_counter = users_counter + 1

    users_list_check(message)

    print(message.from_user.username)
    if message.from_user.username == 'admin_telegram_nickname':
        await message.answer("Press for access to the admin panel:", reply_markup=mykb_adm)


@dp.callback_query_handler(text="refresh")
async def send_welcome(query: types.CallbackQuery):
    print(query.from_user.username)
    mykb.clean()
    if query.message.text != get_value(coeff):
        await query.message.edit_text(get_value(coeff), reply_markup=mykb)

    def users_list_check(query: types.CallbackQuery):
        global users_counter
        k = 0
        if query.from_user.username != 'admin_telegram_nickname' :
            for i in range(0, users_counter):
                if query.from_user.username == users_list_1hr[i]:
                    k = k + 1

        if k == 0 and query.from_user.username != 'admin_telegram_nickname' and query.from_user.username is not None:
            users_list_1hr.append(query.from_user.username)
            users_list_modified.append("@" + query.from_user.username)
            users_counter = users_counter + 1

    users_list_check(query)
    date = (datetime.datetime.now() + datetime.timedelta(hours=-1)).strftime("%d/%m/%Y, %H:%M")
    await query.answer("Exchange rate was refreshed " + date)


@dp.callback_query_handler(text="adm")
async def admin_kb(query: types.CallbackQuery):
    perc = round(((coeff - 1) * 100), 2)
    await query.message.answer("Current coefficient = " + str(perc) + "\n", reply_markup=panel)


@dp.callback_query_handler(text="edit")
async def edit(query: types.CallbackQuery):
    await query.message.answer("Input new coefficient:")


@dp.callback_query_handler(text="back")
async def back(query: types.CallbackQuery):
    await query.message.answer(get_value(coeff), reply_markup=mykb)
    if query.from_user.username == 'admin_telegram_nickname':
        await query.message.answer("Press for access to the admin panel:", reply_markup=mykb_adm)


@dp.callback_query_handler(text="get_list")
async def get_list(query: types.CallbackQuery):
    print('\n'.join(users_list_1hr))
    if query.from_user.username == 'admin_telegram_nickname':
        await query.message.answer(
            "Users (" + str(users_counter) + ") in the last hour:" + "\n" + '\n'.join(users_list_modified))


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
        await message.answer("Coefficient was refreshed " + date)
    else:
        await message.reply("Input error, please try again:")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
