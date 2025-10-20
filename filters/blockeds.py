import typing
from aiogram import types
from loader import db, dp, bot
from data.translation import get_text
from aiogram.dispatcher.filters import BoundFilter


async def get_user(user_id):
    user = await db.select_user(telegram_id=user_id)
    
    if user:
        return user
    
    return None


class BlockedUserFilter(BoundFilter):
    key = 'blocked_user'

    # def __init__(self, chat_id: typing.Union[typing.Iterable, int]):
    #         if isinstance(chat_id, int):
    #             chat_id = [chat_id]
    #         self.chat_id = chat_id
        
    async def check(self, message: types.Message):
        user_id = message.from_user.id
        user = await get_user(user_id)
        is_blocked = False
        
        if user:
            is_blocked = user['status'] == 'blocked'                                                #type: ignore

            if is_blocked:
                await bot.send_message(text=get_text(user['language'], 'blocked'), chat_id=user_id) #type: ignore
            
            return not is_blocked 

        return not is_blocked                                                                       #type: ignore  

dp.filters_factory.bind(BlockedUserFilter, event_handlers=[dp.message_handlers])