from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
mykb = InlineKeyboardMarkup(row_width=1)
mybt = InlineKeyboardButton(text="Refresh exchange rate", callback_data="refresh")
mykb.add(mybt)


mykb_adm = InlineKeyboardMarkup(row_width=1)
bt_adm = InlineKeyboardButton(text="Admin panel", callback_data="adm")
mykb_adm.add(bt_adm)


panel = InlineKeyboardMarkup(row_width=1)
panel_bt1 = InlineKeyboardButton(text="Modify coefficient", callback_data="edit")
panel_bt2 = InlineKeyboardButton(text="Close panel", callback_data="back")
panel_bt3 = InlineKeyboardButton(text="Get users list", callback_data="get_list")
panel.add(panel_bt1, panel_bt2, panel_bt3)
