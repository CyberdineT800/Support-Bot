from aiogram.dispatcher.filters.state import StatesGroup, State

class Man_State(StatesGroup):
    man_audio = State()
    man_document = State()
    man_photo = State()
    man_text = State()
    man_video = State()
    man_voice = State()
    user_checkone = State()


class ManAdmin(StatesGroup):
    SOS_one = State()
    SOS_two = State()
    SOS_three = State()
    bot_addone = State()
    bot_editone = State()
    bot_one = State()
    bot_two = State()
    admin_one = State()
    admin_two = State()
    admin_delone = State()

class Man_Woman_State(StatesGroup):
    man_woman = State()
    man_one = State()
    
    man_anon_select = State()
    woman_anon_select = State()

    woman_one = State()
    woman_two = State()
    cancel = State()


class AddAdmin(StatesGroup):
    one = State()
    two = State()
    three = State()
