from aiogram.types import ReplyKeyboardMarkup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

savol_ck = ReplyKeyboardMarkup(resize_keyboard=True)
savol_ck.insert('Dasturiy yordam')
savol_ck.insert('Texnik yordam')
savol_ck.add('🏡  Bosh sahifa')

yes_no = InlineKeyboardMarkup(
    row_width=2,
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="✅ Ha",
                callback_data="yes"
            ),
            InlineKeyboardButton(
                text="♻️ Yo'q qayta",
                callback_data="no_again"
            )
        ]
    ]
)
