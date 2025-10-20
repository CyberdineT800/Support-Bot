import json
import time
import logging

from aiogram import types
from aiogram.types import ContentType
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import CallbackQuery, ChatMemberUpdated, Message, ReplyKeyboardRemove

from utils.misc import subscription
from keyboards.default.bottons import *
from states.sos_states import Man_Woman_State
from filters.blockeds import BlockedUserFilter
from keyboards.default.start_dk import create_main_keyboard
from handlers.users.help import create_personal_infos, is_contact, is_registered

from data.posts import *
from loader import dp, bot, db
from data.config import SUPER_ADMINS
from data.config import CHANNELS
from states.users import PersonalData, Application

from data.cases import get_cases
from data.categories import get_category
from data.translation import get_text, load_language_config, get_values_for_key


languages_texts = ["O'zbek tili", "Ўзбек тили", "Русский язык"]
select_lang = "Тилни танланг:\nTilni tanlang:\nВыбор языка:"


@dp.message_handler(BlockedUserFilter(), commands=['start'], state="*")
async def bot_start(message: types.Message, state: FSMContext):
    data = await db.select_user(telegram_id=message.from_user.id)

    if data is not None and message.from_user.id not in SUPER_ADMINS:
        await state.update_data({"language": data['language']})              #type: ignore
        selected_language = data.get('language', 'uz_latin')                 #type: ignore
        
        await PersonalData.start.set()
        await message.answer(get_text(selected_language, 'welcome'), 
                             reply_markup=start_menu(get_text(selected_language, 'online_txt'), get_text(selected_language, 'expert_txt'),
                                                     get_text(selected_language, 'examples_txt'), get_text(selected_language, 'faq_txt'),
                                                     get_text(selected_language, 'info_txt'), get_text(selected_language, 'contact_txt'),
                                                     is_reg=is_registered(data), problem_txt=get_text(selected_language, 'problem_txt'),
                                                     profile_txt=get_text(selected_language, 'profile')))
        
    elif message.from_user.id not in SUPER_ADMINS:
        # await PersonalData.language.set()
        # await message.answer(select_lang, reply_markup=languages_btns)

        data = await db.select_user(telegram_id=message.from_user.id)              
        datas = await state.get_data()
        selected_language = datas.get("language", "uz_latin") 

        if not data:
            await state.update_data({"telegram_id": message.from_user.id,
                                     "username": message.from_user.username,
                                     "telegram_name": message.from_user.full_name,
                                     "status": "unblock",
                                     "name": 'none',
                                     "phone":'none',
                                     "region": 'none',
                                     "city": 'none',
                                     "language": 'uz_latin',
                                     "status": 'unblock'}) 
            
            datas = await state.get_data()
            datas = filter_datas(datas)

            selected_language = datas.get("language", "uz_latin")
            await db.add_user(**datas)
            data = await db.select_user(telegram_id=message.from_user.id)

        await PersonalData.start.set()
        await message.answer(get_text(selected_language, 'welcome'), 
                             reply_markup=start_menu(get_text(selected_language, 'online_txt'), get_text(selected_language, 'expert_txt'),
                                                     get_text(selected_language, 'examples_txt'), get_text(selected_language, 'faq_txt'),
                                                     get_text(selected_language, 'info_txt'), get_text(selected_language, 'contact_txt'),
                                                     is_reg=is_registered(data), problem_txt=get_text(selected_language, 'problem_txt'),
                                                     profile_txt=get_text(selected_language, 'profile')))


def filter_datas(datas):
    res = {}
    for key in ['telegram_id', 'telegram_name', 'username', 'name', 'phone', 'region', 'city', 'language', 'status']:
        res[key] = datas.get(key, 'none')
    return res


@dp.message_handler(BlockedUserFilter(), text=get_values_for_key('contact_txt'), state=PersonalData.start)
async def get_contacts(message: types.Message, state: FSMContext):
    datas = await state.get_data()
    selected_language = datas.get("language", "uz_latin")
    parts = SOCIAL_ACCS_POST.split('/')
    await bot.copy_message(message.from_user.id,
                           f"@{parts[-2]}" if not parts[-2].isdigit() else parts[-2],
                           parts[-1],
                           protect_content=True)


@dp.message_handler(BlockedUserFilter(), text=get_values_for_key('info_txt'), state=PersonalData.start)
@dp.message_handler(BlockedUserFilter(), text=get_values_for_key('info_txt'), state=PersonalData.online)
async def get_infos(message: types.Message, state: FSMContext):
    datas = await state.get_data()
    selected_language = datas.get("language", "uz_latin")
    parts = INFOS_POST.split('/')
    await bot.copy_message(message.from_user.id,
                           f"@{parts[-2]}" if not parts[-2].isdigit() else parts[-2],
                           parts[-1],
                           protect_content=True)


@dp.message_handler(BlockedUserFilter(), text=get_values_for_key('faq_txt'), state=PersonalData.start)
async def get_faqs(message: types.Message, state: FSMContext):
    datas = await state.get_data()
    selected_language = datas.get("language", "uz_latin")
    parts = FAQ_POST.split('/')
    await bot.copy_message(message.from_user.id,
                           f"@{parts[-2]}" if not parts[-2].isdigit() else parts[-2],
                           parts[-1],
                           protect_content=True)


@dp.message_handler(BlockedUserFilter(), text=get_values_for_key('examples_txt'), state=PersonalData.start)
async def get_examples(message: types.Message, state: FSMContext):
    datas = await state.get_data()
    selected_language = datas.get("language", "uz_latin")
    parts = EXAMPLES_POST.split('/')
    await bot.copy_message(message.from_user.id,
                           f"@{parts[-2]}" if not parts[-2].isdigit() else parts[-2],
                           parts[-1],
                           protect_content=True)


@dp.message_handler(BlockedUserFilter(), text=get_values_for_key('expert_txt'), state=PersonalData.start)
async def start_expert(message: types.Message, state: FSMContext):
    datas = await state.get_data()
    selected_language = datas.get("language", "uz_latin")
    
    data = await db.select_user(telegram_id=message.from_user.id)
    if is_registered(data):
        await message.answer(get_text(selected_language, 'operator_txt'))
    else:
        await state.update_data({
            "from_expert_txt": True
        })
        await PersonalData.registration.set()
        await message.answer(get_text(selected_language, 'reg_note_txt'), 
                             reply_markup=create_btn_with_back(get_text(selected_language, 'register'), 
                                                               get_text(selected_language, 'back')))
        

# @dp.message_handler(BlockedUserFilter(), text=languages_texts, state=PersonalData.language)
# async def update_language(message: types.Message, state: FSMContext):
#         user_language = message.text 

#         if user_language == "O'zbek tili":
#             await state.update_data(
#                             {"language": "uz_latin"}
#                         )
#             await message.answer("O`zbek tili tanlandi.")
#         elif user_language == "\u040E\u0437\u0431\u0435\u043A \u0442\u0438\u043B\u0438":
#             await state.update_data(
#                             {"language": "uz_kirill"}
#                         )
#             await message.answer("Ўзбек тили танланди.")
#         elif user_language == "\u0420\u0443\u0441\u0441\u043a\u0438\u0439 \u044f\u0437\u044b\u043a":
#             await state.update_data(
#                             {"language": "ru"}
#                         )
#             await message.answer("Русский язык выбран.")
         
#         await state.update_data({"telegram_id": message.from_user.id,
#                                  "username": message.from_user.username,
#                                  "telegram_name": message.from_user.full_name,
#                                  "status": "unblock",
#                                  "name": 'none',
#                                  "phone":'none',
#                                  "region": 'none',
#                                  "city": 'none',
#                                  "status": 'unblock'})        
                               
#         data = await db.select_user(telegram_id=message.from_user.id)
#         datas = await state.get_data()
#         selected_language = datas.get("language", "uz_latin") 

#         if data:
#             await db.add_user(**datas)
        
#         await PersonalData.registration.set()
#         await message.answer(get_text(selected_language, 'reg_note_txt'), 
#                              reply_markup=create_btn_with_back(get_text(selected_language, 'register'), 
#                                                                get_text(selected_language, 'back')))
 

@dp.message_handler(BlockedUserFilter(), text=get_values_for_key('online_txt'), state=PersonalData.start)
async def start_online(message: types.Message, state: FSMContext):
    data = await db.select_user(telegram_id=message.from_user.id)
    datas = await state.get_data()
    selected_language = datas.get("language", "uz_latin")

    if is_registered(data):
        await PersonalData.online.set()
        await message.answer(get_text(selected_language, 'select_any_button'), 
                             reply_markup=online_menu(get_text(selected_language, 'from_website_txt'),
                                                      get_text(selected_language, 'info_txt'),
                                                      get_text(selected_language, 'home')))
    else:
        await state.update_data({
            "from_online_txt": True
        })
        await PersonalData.registration.set()
        await message.answer(get_text(selected_language, 'reg_note_txt'), 
                             reply_markup=create_btn_with_back(get_text(selected_language, 'register'), 
                                                               get_text(selected_language, 'back')))


@dp.message_handler(BlockedUserFilter(), text=get_values_for_key("back"), state=PersonalData.online)
@dp.message_handler(BlockedUserFilter(), text=get_values_for_key("back"), state=PersonalData.registration)
async def back_2_start(message: types.Message, state: FSMContext):
    datas = await state.get_data()
    selected_language = datas.get("language", "uz_latin")

    await PersonalData.start.set()
    await message.answer(get_text(selected_language, 'select_any_button'), 
                         reply_markup=start_menu(get_text(selected_language, 'online_txt'), get_text(selected_language, 'expert_txt'),
                                                 get_text(selected_language, 'examples_txt'), get_text(selected_language, 'faq_txt'),
                                                 get_text(selected_language, 'info_txt'), get_text(selected_language, 'contact_txt'),
                                                 is_reg=is_registered(datas), problem_txt=get_text(selected_language, 'problem_txt'),
                                                 profile_txt=get_text(selected_language, 'profile')))



@dp.message_handler(BlockedUserFilter(), text=get_values_for_key('from_website_txt'), state=PersonalData.online)
async def from_website(message: types.Message, state: FSMContext):
    datas = await state.get_data()
    selected_language = datas.get("language", "uz_latin")
    parts = DOWNLOAD_FROM_WEBSITE_POST.split('/')
    await bot.copy_message(message.from_user.id,
                           f"@{parts[-2]}" if not parts[-2].isdigit() else parts[-2],
                           parts[-1],
                           protect_content=True)


@dp.message_handler(BlockedUserFilter(), text=get_values_for_key("register"), state=PersonalData.registration)
async def start_register(message: types.Message, state: FSMContext):
    datas = await state.get_data()
    selected_language = datas.get("language", "uz_latin")
    parts = REG_POST.split('/')
    await bot.copy_message(message.from_user.id,
                           f"@{parts[-2]}" if not parts[-2].isdigit() else parts[-2],
                           parts[-1],
                           protect_content=True)

    await PersonalData.name.set()
    await message.answer(get_text(selected_language, "fullname"), reply_markup=create_back_btn(selected_language))


@dp.message_handler(BlockedUserFilter(), text=get_values_for_key("back"), state=PersonalData.name)
async def back_2_reg(message: types.Message, state: FSMContext):
    datas = await state.get_data()
    selected_language = datas.get("language", "uz_latin")

    await PersonalData.registration.set()
    await message.answer(get_text(selected_language, 'reg_note_txt'), 
                         reply_markup=create_btn_with_back(get_text(selected_language, 'register'), 
                                                           get_text(selected_language, 'back')))


@dp.message_handler(BlockedUserFilter(), state=PersonalData.name)
async def read_name(message: types.Message, state: FSMContext):
    datas = await state.get_data()
    selected_language = datas.get("language", "uz_latin")

    name = message.text
    await state.update_data(
        {"name": name}
    )

    await PersonalData.region.set()
    await message.answer(get_text(selected_language, 'select_any_button'), reply_markup=ReplyKeyboardRemove(selective=False))
    await message.answer(get_text(selected_language, 'region'), reply_markup=create_region_btns(selected_language))


@dp.callback_query_handler(BlockedUserFilter(), Text(startswith='region'), state=PersonalData.region)
async def select_region(call: CallbackQuery, state: FSMContext):
    datas = await state.get_data()
    selected_language = datas.get("language", "uz_latin")

    key = call.data.replace('region_', '').strip()
    
    if key == 'back':
        await PersonalData.name.set()
        await call.message.answer(get_text(selected_language, "fullname"), 
                                  reply_markup=create_back_btn(selected_language))
        
        await call.message.delete()
    else:
        region = get_text(selected_language, 'regions')[key]
        await state.update_data({'region': region,
                                 'region_key': key})
        await PersonalData.city.set()
        
        await call.message.edit_text(text=get_text(selected_language, 'city'), reply_markup=create_city_btns(selected_language, key))
    


@dp.callback_query_handler(BlockedUserFilter(), Text(startswith='city'), state=PersonalData.city)
async def select_city(call: CallbackQuery, state: FSMContext):
    datas = await state.get_data()
    selected_language = datas.get("language", "uz_latin")

    key = call.data.replace('city_', '').strip()
    
    if key == 'back':
        await PersonalData.region.set()
        await call.message.edit_text(text=get_text(selected_language, 'region'), reply_markup=create_region_btns(selected_language))
    else:
        city = get_text(selected_language, 'districts')[datas['region_key']][key]
        await state.update_data({'city': city,
                                 'city_key': key})
        
        await PersonalData.phone.set()
        await call.message.answer(get_text(selected_language, "contact"),
                                  reply_markup=create_contact_us_btns(get_text(selected_language, "send_contact"),
                                                                      get_text(selected_language, "back")))
        await call.message.delete()
    

@dp.message_handler(BlockedUserFilter(), text=get_values_for_key("back"), state=PersonalData.phone)
async def back_2_regions(message: types.Message, state: FSMContext):
    datas = await state.get_data()
    selected_language = datas.get("language", "uz_latin")

    await PersonalData.region.set()
    await message.answer(get_text(selected_language, 'region'), 
                         reply_markup=create_region_btns(selected_language))
    

@dp.message_handler(BlockedUserFilter(), content_types=ContentType.CONTACT, state=PersonalData.phone)
@dp.message_handler(BlockedUserFilter(), content_types=ContentType.TEXT, state=PersonalData.phone)
async def read_phone(message: types.Message, state: FSMContext):
    datas = await state.get_data()
    selected_language = datas.get("language", "uz_latin")

    if message.content_type == 'contact' or is_contact(message.text):
        if message.content_type == 'contact':
            phone = message.contact.phone_number
        else:
            phone = message.text
            
        await state.update_data(
            {"phone": phone}
        )

        datas = await state.get_data()
    
        await PersonalData.result.set()
        personal_info =  create_personal_infos(selected_language, datas)

        await message.answer(personal_info)
        await message.answer(get_text(selected_language, 'accept'), reply_markup=create_yes_no_btns(get_text(selected_language, 'yestxt'),
                                                                                                    get_text(selected_language, 'notxt')))
    else:
        await message.answer(get_text(selected_language, "error_contact") )       

        await PersonalData.phone.set()
        await message.answer(get_text(selected_language, "contact"),
                             reply_markup=create_contact_us_btns(get_text(selected_language, "send_contact"),
                                                                 get_text(selected_language, "back")))


@dp.message_handler(BlockedUserFilter(), text=get_values_for_key("yestxt"), state=PersonalData.result)
@dp.message_handler(BlockedUserFilter(), text=get_values_for_key("notxt"), state=PersonalData.result)
async def confirm_datas(message: types.Message, state: FSMContext):
    datas = await state.get_data()
    data = await db.select_user(telegram_id=message.from_user.id)
    selected_language = datas.get('language', 'uz_latin')

    if message.text in get_values_for_key("yestxt"):   
        try:
            if data:
                if not datas.get("from_profile_edit", False):
                    await db.update_user_partial_by_id(data['id'], language=datas.get("language", "uz_latin"),              #type: ignore
                                                    name=datas.get("name", "none"), phone=datas.get("phone", "none"),
                                                    city=datas.get("city", "none"), region=datas.get("region", "none"))
                
                if datas.get("from_profile_edit", False):
                    await message.answer(get_text(selected_language, 'accepted'))
                    await state.update_data({
                        "from_profile_edit": False
                    })
                else:
                    await message.answer(get_text(selected_language, 'registered'))
                data = await db.select_user(telegram_id=message.from_user.id)
            else:
                await message.answer(get_text(selected_language, "something_wrong"))
        except Exception as err:
            print(f"users -> start_hr -> confirm_datas -> updating_user (exist user) -> {err}")
            logging.exception(err)    

        try:
            if not datas.get("from_profile_edit", False):
                personal_info =  create_personal_infos(selected_language, data)
                if data:
                    #print(f"\nYangi foydalanuvchi: {data['telegram_id']} {data['telegram_name']} {data['language']}\n")      #type: ignore
                    for admin in SUPER_ADMINS:
                        await bot.send_message(chat_id=admin,
                                               text=f"{personal_info}"
                                               f"Telegram Name: {data['telegram_name']}\n"                                     #type: ignore
                                               f"Telegram ID: <code>{data['telegram_id']}</code>\n")                           #type: ignore

        except Exception as err:
            print(f"users -> start_hr -> confirm_datas -> sending_admin -> {err}")
            logging.exception(err)

        if datas.get('from_online_txt', False):
            await state.update_data({
                "from_online_txt": False
            })
            await PersonalData.online.set()
            await message.answer(get_text(selected_language, 'select_any_button'), 
                                reply_markup=online_menu(get_text(selected_language, 'from_website_txt'),
                                                        get_text(selected_language, 'info_txt'),
                                                        get_text(selected_language, 'home')))
        elif datas.get('from_expert_txt', False):
            await state.update_data({
                "from_expert_txt": False
            })
            await message.answer(get_text(selected_language, 'operator_txt'))
            await PersonalData.start.set()
            await message.answer(get_text(selected_language, 'select_any_button'), 
                                reply_markup=start_menu(get_text(selected_language, 'online_txt'), get_text(selected_language, 'expert_txt'),
                                                        get_text(selected_language, 'examples_txt'), get_text(selected_language, 'faq_txt'),
                                                        get_text(selected_language, 'info_txt'), get_text(selected_language, 'contact_txt'),
                                                        is_reg=is_registered(data), problem_txt=get_text(selected_language, 'problem_txt'),
                                                        profile_txt=get_text(selected_language, 'profile')))
        else:
            await PersonalData.start.set()
            await message.answer(get_text(selected_language, 'select_any_button'), 
                                reply_markup=start_menu(get_text(selected_language, 'online_txt'), get_text(selected_language, 'expert_txt'),
                                                        get_text(selected_language, 'examples_txt'), get_text(selected_language, 'faq_txt'),
                                                        get_text(selected_language, 'info_txt'), get_text(selected_language, 'contact_txt'),
                                                        is_reg=is_registered(data), problem_txt=get_text(selected_language, 'problem_txt'),
                                                        profile_txt=get_text(selected_language, 'profile')))

    else:
        if datas.get("from_profile_edit", False):
            await PersonalData.registration.set()
            await message.answer(get_text(selected_language, 'reg_note_txt'), 
                                 reply_markup=create_btn_with_back(get_text(selected_language, 'register'), 
                                                                   get_text(selected_language, 'back')))
        else:
            await message.answer(get_text(selected_language, 'not_registered'))
            await PersonalData.start.set()
            await message.answer(get_text(selected_language, 'select_any_button'), 
                                reply_markup=start_menu(get_text(selected_language, 'online_txt'), get_text(selected_language, 'expert_txt'),
                                                        get_text(selected_language, 'examples_txt'), get_text(selected_language, 'faq_txt'),
                                                        get_text(selected_language, 'info_txt'), get_text(selected_language, 'contact_txt'),
                                                        is_reg=is_registered(data), problem_txt=get_text(selected_language, 'problem_txt'),
                                                        profile_txt=get_text(selected_language, 'profile')))
      

@dp.message_handler(BlockedUserFilter(), text=get_values_for_key("home"), state='*')
async def home(message: types.Message, state: FSMContext):
    data = await state.get_data()
    selected_language=data.get('language', 'uz_latin')

    await PersonalData.start.set()
    await message.answer(get_text(selected_language, 'select_any_button'), 
                         reply_markup=start_menu(get_text(selected_language, 'online_txt'), get_text(selected_language, 'expert_txt'),
                                                 get_text(selected_language, 'examples_txt'), get_text(selected_language, 'faq_txt'),
                                                 get_text(selected_language, 'info_txt'), get_text(selected_language, 'contact_txt'),
                                                 is_reg=data is not None, problem_txt=get_text(selected_language, 'problem_txt'),
                                                 profile_txt=get_text(selected_language, 'profile')))


@dp.message_handler(BlockedUserFilter(), text=get_values_for_key("profile"), state='*')
async def profile(message: types.Message, state: FSMContext):
    data = await db.select_user(telegram_id=message.from_user.id)
    if not data:
        data = await state.get_data()
        
    selected_language=data.get('language', 'uz_latin')                      #type: ignore

    await PersonalData.result.set()

    personal_info =  create_personal_infos(selected_language, data)

    await state.update_data({
        "from_profile_edit": True
    })
    await message.answer(personal_info)
    await message.answer(get_text(selected_language, 'accept'), reply_markup=create_yes_no_btns(get_text(selected_language, 'yestxt'),
                                                                                                get_text(selected_language, 'notxt')))
     
