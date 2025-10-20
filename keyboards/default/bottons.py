import json
from data.translation import get_text 
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup


def load_language_config(language):
    with open('data/languages.json', 'r') as file:
        config = json.load(file)
    return config #.get(language, {}).get('button_texts', {})


languages_btns=ReplyKeyboardMarkup(             
    keyboard=[
        [
            KeyboardButton(text="O'zbek tili"),                 # type: ignore
            KeyboardButton(text='Ўзбек тили'),                  # type: ignore
        ], 
        [ 
            KeyboardButton(text='Русский язык'),                # type: ignore
        ], 
    ],
    resize_keyboard=True,
)                                                               # type: ignore


async def create_start_menu(selected_language, is_reg=False):
    keyboard=ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=get_text(selected_language, 'online_txt')),                 # type: ignore
                KeyboardButton(text=get_text(selected_language, 'expert_txt')),                 # type: ignore
            ],
            [
                KeyboardButton(text=get_text(selected_language, 'examples_txt')),               # type: ignore
                KeyboardButton(text=get_text(selected_language, 'faq_txt')),                    # type: ignore
            ],
            [
                KeyboardButton(text=get_text(selected_language, 'info_txt')),                   # type: ignore
                KeyboardButton(text=get_text(selected_language, 'contact_txt')),                # type: ignore
            ],
            [
                KeyboardButton(text=get_text(selected_language, 'problem_txt')),                # type: ignore
                KeyboardButton(text=get_text(selected_language, 'profile')),                    # type: ignore
            ] if is_reg else []
        ],
        resize_keyboard=True,
    )                                                                                           # type: ignore
    
    return keyboard


def start_menu(online_txt, expert_txt, examples_txt, faq_txt, info_txt, contact_txt, is_reg=False, problem_txt=None, profile_txt=None):
    keyboard=ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=online_txt),                 # type: ignore
                KeyboardButton(text=expert_txt),                 # type: ignore
            ],
            [
                KeyboardButton(text=examples_txt),               # type: ignore
                KeyboardButton(text=faq_txt),                    # type: ignore
            ],
            [
                KeyboardButton(text=info_txt),                   # type: ignore
                KeyboardButton(text=contact_txt),                # type: ignore
            ],
            [
                KeyboardButton(text=problem_txt),                # type: ignore
                KeyboardButton(text=profile_txt),                # type: ignore
            ] if is_reg else []
        ],
        resize_keyboard=True,
    )                                                            # type: ignore
    
    return keyboard


def online_menu(from_website_txt, info_txt, home_txt, back_txt=None):
    keyboard=ReplyKeyboardMarkup(

        keyboard=[
            [
                KeyboardButton(text=from_website_txt),            # type: ignore
                KeyboardButton(text=info_txt),                    # type: ignore
            ],
            [
                KeyboardButton(text=home_txt),                    # type: ignore
            ],
            [
                KeyboardButton(text=back_txt),                    # type: ignore
            ] if back_txt else [] ,
        ],
        resize_keyboard=True,
    )                                                             # type: ignore
    
    return keyboard


def create_btn_with_back (text, back_text):
    menuAsosiy=ReplyKeyboardMarkup(

        keyboard=[
            [
                KeyboardButton(text=text),                        # type: ignore
            ],
            [
                KeyboardButton(text=back_text),                   # type: ignore
            ],

        ],
        resize_keyboard=True,
    )                                                             # type: ignore
    
    return menuAsosiy


def create_contact_us_btns(text, back_text, skip_txt=None):
    contact_us=ReplyKeyboardMarkup(

        keyboard=[
            [
                KeyboardButton(text=text, request_contact=True),              # type: ignore
            ],
            [
                KeyboardButton(text=skip_txt if skip_txt else back_text),     # type: ignore
            ],
        ],
        resize_keyboard=True,
    )                                                                         # type: ignore
    
    return contact_us




def create_back_btn(selected_language):
    back_text = get_text(selected_language, 'back')
    
    keyboard=ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=back_text),                  # type: ignore
            ],
        ],
        resize_keyboard=True,
    )                                                            # type: ignore
    
    return keyboard


def create_cancel_button (canceltxt):
    cancel=ReplyKeyboardMarkup(

        keyboard=[
            [
                KeyboardButton(text=f'{canceltxt}'),             # type: ignore
            ],
        ],
        
        resize_keyboard=True,
    )                                                            # type: ignore
    
    return cancel


def create_region_btns(selected_language):
    regions = get_text(selected_language, 'regions')
    inline_keyboard = []

    for key, value in regions.items():
        inline_keyboard.append([InlineKeyboardButton(text=value, 
                                                     callback_data=f'region_{key}')])        # type: ignore
        
    inline_keyboard.append([InlineKeyboardButton(text=get_text(selected_language, 'back'), 
                                                 callback_data=f'region_back')])             # type: ignore  

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def create_city_btns(selected_language, region_key):
    districts = get_text(selected_language, 'districts')[region_key]
    inline_keyboard = []

    for key, value in districts.items():
        inline_keyboard.append([InlineKeyboardButton(text=value, 
                                                     callback_data=f'city_{key}')])           # type: ignore
        
    inline_keyboard.append([InlineKeyboardButton(text=get_text(selected_language, 'back'), 
                                                 callback_data=f'city_back')])                # type: ignore

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)



def create_yes_no_btns(yestext, notext):
    hayuq=ReplyKeyboardMarkup(

        keyboard=[
            [
                KeyboardButton(text=f'{yestext}'),             # type: ignore
                KeyboardButton(text=f'{notext}'),              # type: ignore
            ],
        ],
        resize_keyboard=True,
    )                                                          # type: ignore
    
    return hayuq


def create_informations_btns (general, categories, back):
    result=ReplyKeyboardMarkup(

        keyboard=[
                    [
                        KeyboardButton(text=f'{general}'),         # type: ignore
                        KeyboardButton(text=f'{categories}'),      # type: ignore
                    ],
                    [
                        KeyboardButton(text=f'{back}'),            # type: ignore
                    ],
                ],
        resize_keyboard=True,
    )                                                              # type: ignore
    
    return result
