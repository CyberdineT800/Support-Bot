import logging

from aiogram import Dispatcher, Bot
from data.config import SUPER_ADMINS

async def on_startup_notify(bot: Bot, dp: Dispatcher):
    for admin in SUPER_ADMINS:
        try:
            await bot.send_message(chat_id=admin, text="Bot ishga tushdi!\n/admins buyrug'ini yuboring!")
        except Exception as err:
            print(f"notify_admins -> on_startup_notify -> {err}")
            logging.exception(err)
