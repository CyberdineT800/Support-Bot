from aiogram.dispatcher.filters.state import StatesGroup, State

class UserState(StatesGroup):
    language = State()

class PersonalData(StatesGroup):
    language = State()
    start = State()
    online = State()
    expert = State()
    registration = State()
    name = State()
    phone = State()
    region = State()
    city = State()
    result = State()
    problem = State()

class Application(StatesGroup):
    tip = State()
    data = State()
    nomer = State()
    id = State()
    natija = State()

class ArizaState(StatesGroup):
    savollar = State()
    javoblar = State()

class ArizaStatex(StatesGroup):
    description = State()

class StudentState(StatesGroup):
    speciality = State()
    course = State()
    group = State()
