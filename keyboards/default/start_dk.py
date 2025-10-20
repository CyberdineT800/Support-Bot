#import profile

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from data.translation import get_text

async def create_main_keyboard(language):
    menuAsosiy=ReplyKeyboardMarkup(

        keyboard=[
            [
                #KeyboardButton(text=get_text(language, 'offer')),
                KeyboardButton(text=get_text(language, 'problem'))
            ],
            [
                KeyboardButton(text=get_text(language, 'menu'))
            ],

        ],
        resize_keyboard=True,
    )
    
    return menuAsosiy


# main_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
# # main_keyboard.row("🎧")
# main_keyboard.row("📊Ko'p beriladigan savollar⁉️")
# main_keyboard.row("Arizalar", "Profil")

# support_keys = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
# support_keys.row('Dasturiy yordam', 'Texnik yordam')

# bosh_menyu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
# bosh_menyu.row('🏡  Bosh sahifa')
