from loader import db
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# async def answer_questions_button(gender):
#     user = await db.select_question_id(gender=gender)
#     markup = InlineKeyboardMarkup(row_width=3)
#     for n in user:
#         markup.insert(InlineKeyboardButton(text=f"{n[1]}", callback_data=f"{n[0]}"))
#     return markup


async def answer_questions_two(back_button=False):
    markup = InlineKeyboardMarkup(row_width=2)

    markup.insert(InlineKeyboardButton(text='👤 Admin javobi', callback_data='admin_answer'))    # type: ignore
    markup.add(InlineKeyboardButton(text='ℹ Bot javobi', callback_data='bot_answer'))             # type: ignore
    markup.insert(InlineKeyboardButton(text='❌ O\'chirish!', callback_data='delete_answer'))    # type: ignore

    # if not back_button:
    #     markup.insert(InlineKeyboardButton(text='◀ Ortga', callback_data='back_answer_false'))
    # else:
    #     markup.insert(InlineKeyboardButton(text='◀ Ortga', callback_data='back_answer_true'))
    return markup



def unblock_inline_btn(user):
    bot_answer_keyboard = InlineKeyboardMarkup()
    
    if user['status'] == 'unblock':
        bot_answer_keyboard.insert(InlineKeyboardButton(text='Bloklash', 
                                                        callback_data=f'block_user_{user["telegram_id"]}'))   # type: ignore
    else:
        bot_answer_keyboard.insert(InlineKeyboardButton(text='Blokdan chiqarish', 
                                                        callback_data=f'unblock_user_{user["telegram_id"]}')) # type: ignore 

    return bot_answer_keyboard


bot_answer_keyboard = InlineKeyboardMarkup(row_width=2)
bot_answer_keyboard.insert(InlineKeyboardButton(text='♻ Bot javobini o‘zgartirish', 
                                                callback_data='edit_bot_answer'))      # type: ignore
bot_answer_keyboard.insert(InlineKeyboardButton(text='📤 Yuborish', 
                                                callback_data='send_answer'))          # type: ignore
bot_answer_keyboard.add(InlineKeyboardButton(text='◀ Ortga', 
                                             callback_data='back_bot_answer'))         # type: ignore

check_bot_answer = InlineKeyboardMarkup(row_width=2)
check_bot_answer.insert(InlineKeyboardButton(text='💾 Saqlash', 
                                             callback_data='check_bot'))               # type: ignore
check_bot_answer.insert(InlineKeyboardButton(text='♻ Qayta kiritish', 
                                             callback_data='again_bot'))               # type: ignore
#check_bot_answer.add(InlineKeyboardButton(text='◀ Ortga', callback_data='back_check'))

admin_yes_no = InlineKeyboardMarkup(row_width=2)
admin_yes_no.insert(InlineKeyboardButton(text='✅  Qoldirish', 
                                         callback_data='admin_yes'))                   # type: ignore
admin_yes_no.insert(InlineKeyboardButton(text='❌  O\'chirish', 
                                         callback_data='admin_check_delete'))          # type: ignore
admin_yes_no.insert(InlineKeyboardButton(text='◀ Ortga', 
                                         callback_data='admin_no_again'))              # type: ignore


def create_user_yes_no(confirmtxt, reentertxt):
    user_yes_no = InlineKeyboardMarkup(row_width=2)
    user_yes_no.insert(InlineKeyboardButton(text=confirmtxt, 
                                            callback_data='user_yes'))                 # type: ignore
    user_yes_no.insert(InlineKeyboardButton(text=reentertxt, 
                                            callback_data='user_no_again'))            # type: ignore

    return user_yes_no

def create_user_check_ikeys (yestxt, notxt):
    user_check_ikeys = InlineKeyboardMarkup(row_width=2)
    user_check_ikeys.insert(InlineKeyboardButton(text=yestxt, 
                                                 callback_data='user_check_yes'))      #type: ignore
    user_check_ikeys.insert(InlineKeyboardButton(text=notxt, 
                                                 callback_data='user_check_no'))       #type: ignore

    return user_check_ikeys
