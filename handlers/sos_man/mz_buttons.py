from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import sdb


async def button_one():
    user = await sdb.select_question_man()
    markup = InlineKeyboardMarkup(row_width=2)
    for n in user:                                                                                       #type: ignore
        markup.insert(InlineKeyboardButton(text=f"{n[0]}", callback_data=f"{n[1]}"))                     #type: ignore
    return markup
