import time
import asyncio
from aiogram import executor
from loader import dp, db, sdb, bot
from middlewares.checksub import BigBrother
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands
from handlers.users.help import AlbumMiddleware


async def on_startup(dispatcher):
    await db.create()
    await db.create_table_users()

    await sdb.create()
    await sdb.create_table_bot_answer()
    await sdb.create_table_man_sos()
    await sdb.create_table_admins()

    await set_default_commands(dispatcher)
    await on_startup_notify(bot, dispatcher)


async def start_bot():
    dp.middleware.setup(BigBrother())
    dp.middleware.setup(AlbumMiddleware())

    await on_startup(dp)
    await dp.start_polling(bot, allowed_updates=["message", "callback_query", "chat_member"])


if __name__ == '__main__':
    print("Bot ishga tushdi !")

    while True:
        try:
            asyncio.run(start_bot())
        except (asyncio.CancelledError, asyncio.TimeoutError):
            print("\n>>> Tarmoq xatosi yoki timeout — qayta urinish...\n")
            continue
        except Exception as err:
            print(f"\n>>> Ishlashdagi xatolik: {err}\n")
            continue
        finally:
            print("<---- Qayta ishga tushirilmoqda! ---->")

        time.sleep(5)
