from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Botni qayta ishga tushirish"),
            #types.BotCommand("admins", "Adminlar uchun tugmalar"),
            #types.BotCommand("dasturiy_savollar", "Dasturiy yordam bo'yicha qo'llab-quvvatlash")
            #types.BotCommand("texnik_savollar", "Texnik yordam bo'yicha qo'llab-quvvatlash")
        ]
    )
