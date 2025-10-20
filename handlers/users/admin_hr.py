import re
import asyncio
import logging

from typing import List
from aiogram import types
from aiogram.dispatcher import FSMContext

from data.statistics import get_stats
from data.translation import get_text, get_values_for_key
from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import ChatPermissions, InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery

from keyboards.default.adminkeys import adm_adm
from keyboards.default.start_dk import create_main_keyboard

from loader import dp, bot, db, sdb
from data.config import SUPER_ADMINS, MAN_GROUP
from states.sos_states import AddAdmin

addbutton = InlineKeyboardMarkup(row_width=2)
addbutton.add(InlineKeyboardButton(text="👮‍♂️ Adminlarni ko'rish", callback_data='admin_see'))  # type: ignore
addbutton.add(InlineKeyboardButton(text="➕ Qo'shish", callback_data='admin_add'))            # type: ignore

delbutton = InlineKeyboardMarkup(row_width=2)
delbutton.insert(InlineKeyboardButton(text='⬅ Ortga', callback_data='admin_back'))            # type: ignore
delbutton.insert(InlineKeyboardButton(text="❌ O'chirish", callback_data='admin_del'))        # type: ignore

habar = "\nAvvalgi xabarga javob olingan yo'qligini tekshirib ko'ring!"


@dp.message_handler(text='/id', state='*')
async def idaniqlash(msg: Message):
    await msg.answer(f'Sizning ID raqamingiz:\n\n<code>{msg.from_user.id}</code>')


@dp.message_handler(text=['/admins'], user_id=SUPER_ADMINS, state="*")
async def buttons(msg: types.Message, state: FSMContext):
    admins = await sdb.all_admins()
    if len(admins) == 0:                                                                      #type: ignore
        for admin in SUPER_ADMINS:
            await sdb.add_admins(user_id=admin,
                                 fullname="Super admin")
    await msg.answer('Admin bosh menyusi', reply_markup=adm_adm)


@dp.message_handler(text='Count Users', user_id=SUPER_ADMINS)
async def admin_count_users(msg: Message):
    count = await db.count_users()
    await msg.answer(f"\nBazada {count} ta foydalanuvchi mavjud")


@dp.message_handler(text='Get Statistics', user_id=SUPER_ADMINS)
async def admin_get_stats(msg: Message):
    current_stats = get_stats()
    #res = json.dumps(current_stats, indent=4)

    # res = "<blockquote>Takliflar: </blockquote>\n"
    # res += f"  Kunlik: {current_stats['offer']['daily']}\n"
    # res += f"  Haftalik: {current_stats['offer']['weekly']}\n"
    # res += f"  Oylik: {current_stats['offer']['monthly']}\n"
    # res += f"  Yillik: {current_stats['offer']['yearly']}\n"
    # res += f"  Jami: {current_stats['offer']['total']}\n\n"

    res = "<blockquote>Murojaatlar: </blockquote>\n"
    res += f"  Kunlik: {current_stats['problem']['daily']}\n"
    res += f"  Haftalik: {current_stats['problem']['weekly']}\n"
    res += f"  Oylik: {current_stats['problem']['monthly']}\n"
    res += f"  Yillik: {current_stats['problem']['yearly']}\n"
    res += f"  Jami: {current_stats['problem']['total']}"

    await msg.answer(res)



@dp.message_handler(text='Forward ON', user_id=SUPER_ADMINS)
async def admin_forward_state(msg: Message, state: FSMContext):
    await msg.answer(f"<b>FORWARD STATE</b> yoqildi!{habar}")
    await state.set_state("forw")


@dp.message_handler(text='MediaGroup ON', user_id=SUPER_ADMINS)
async def admin_mediagr_state(msg: Message, state: FSMContext):
    await msg.answer(f"<b>MEDIA GROUP STATE</b> yoqildi!{habar}")
    await state.set_state("mediagroup")


@dp.message_handler(text='ID ON', user_id=SUPER_ADMINS)
async def admin_id_state(msg: Message, state: FSMContext):
    await msg.answer(f"<b>ID OLISH STATE</b> yoqildi!{habar}")
    await state.set_state("idolish")


@dp.message_handler(text='Sending messages', user_id=SUPER_ADMINS)
async def admin_sendmes_state(msg: Message, state: FSMContext):
    await msg.answer(f"<b>E'LON JO'NATISH STATE</b> yoqildi!{habar}")
    await state.set_state("elon")


@dp.message_handler(text="Add/Delete Admin", user_id=SUPER_ADMINS)
async def admin_add_state(msg: Message, state: FSMContext):
    await msg.answer('Tugmalardan birini tanlang:', reply_markup=addbutton)


async def set_admin(chat_id, user_id):
    await bot.promote_chat_member(chat_id, user_id, can_change_info=True, can_delete_messages=True,
                                  can_invite_users=True, can_restrict_members=True, can_pin_messages=True,
                                  can_promote_members=True)

async def remove_admin(chat_id, user_id):
    await bot.promote_chat_member(chat_id, user_id, can_change_info=False, can_delete_messages=False,
                                  can_invite_users=False, can_restrict_members=False, can_pin_messages=False,
                                  can_promote_members=False)


@dp.callback_query_handler(text='admin_add', state='*')
async def adminadd(call: CallbackQuery):
    await call.message.delete()
    await call.message.answer('Yangi admin ismini kiriting:')
    await AddAdmin.one.set()


@dp.message_handler(state=AddAdmin.one)
async def addadminone(msg: Message, state: FSMContext):
    await state.update_data({'admin_name': msg.text})
    await msg.answer('ID raqamini kiriting:')
    await AddAdmin.two.set()


@dp.message_handler(state=AddAdmin.two)
async def addadmintwo(msg: Message, state: FSMContext):
    if msg.text.isdigit():
        data = await state.get_data()
        await sdb.add_admins(user_id=int(msg.text),
                             fullname=data['admin_name'])
        await msg.answer("Yangi admin qo'shildi")
        await state.finish()

        await set_admin(MAN_GROUP, msg.text)
    else:
        await msg.answer('Iltimos, faqat raqam kiriting!')


@dp.callback_query_handler(text='admin_see', state='*')
async def onedel(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    admins = await sdb.all_admins()
    if len(admins) == 0:                                                                                          #type: ignore
        await call.message.answer("Bazadan barcha barcha adminlar o'chirilgan! Iltimos, /admins buyrug'ini qayta "
                                  "kiriting!")
        await state.finish()
    for n in admins:                                                                                              #type: ignore
        await call.message.answer(f'Admin: <b>{n[2]}</b>\n\nID raqam: <b>{n[1]}</b>',
                                  reply_markup=delbutton)
    await AddAdmin.three.set()


@dp.callback_query_handler(state=AddAdmin.three)
async def addadminthree(call: CallbackQuery, state: FSMContext):
    if call.data == 'admin_back':
        await call.message.answer('⬅ Ortga', reply_markup=addbutton)
    elif call.data == 'admin_del':
        user_id = call.message.text.split()
        await sdb.delete_admin(user_id=int(user_id[-1]))
        await call.answer(text="Admin bazadan o'chirildi!", show_alert=True)

        await remove_admin(MAN_GROUP, user_id[-1])
    await call.message.delete()
    await state.finish()


@dp.message_handler(content_types=['video', 'audio', 'voice', 'photo', 'document', 'text'], user_id=SUPER_ADMINS,
                    state="forw")
async def contumum(msg: types.Message, state: FSMContext):
    if msg.text == 'Forward OFF':
        await msg.answer("Forward ON state o'chirildi!")
        await state.finish()
    else:
        if msg.video or msg.audio or msg.voice or msg.document or msg.photo or msg.text:
            await msg.answer("Xabar yuborilmoqda...")
                             # reply_markup=create_main_keyboard(
                             #                            get_text('uz_latin', 'faq'),
                             #                            get_text('uz_latin', 'policy'),
                             #                            get_text('uz_latin', 'statistics'),
                             #                            get_text('uz_latin', 'technical_problems'),
                             #                            get_text('uz_latin', 'profile')
                             #                          ))
            await state.finish()

            users = await db.select_all_users()
            count_baza = await db.count_users()
            active = 0
            block = 0
            counter = 0

            for user in users:                                                                     #type: ignore
                user_id = user[1]
                try:
                    await msg.forward(chat_id=user_id)

                    active += 1

                except:

                    block += 1
                    continue

                counter += 1

                if counter == 25:
                    counter = 0
                    await asyncio.sleep(0.5)
            await state.finish()

            await msg.answer(f"SENT: <b>{active}</b>"
                             f"\nBLOCK: <b>{block}</b>"
                             f"\nALL_USERS: <b>{count_baza}</b>")

    active = 0
    block = 0
    counter = 0


@dp.message_handler(is_media_group=True, content_types=types.ContentType.ANY, state="mediagroup")
async def mediagr(msg: types.Message, album: List[types.Message], state: FSMContext):
    media_group = types.MediaGroup()
    for obj in album:
        if obj.photo:
            file_id = obj.photo[-1].file_id
        else:
            file_id = obj[obj.content_type].file_id            # type: ignore
        try:
            media_group.attach({"media": file_id,
                                "type": obj.content_type,
                                "caption": obj.caption})
        except Exception as err:
            logging.exception(err)
            return await msg.answer("Bu albomni bot qo‘llamaydi!")

    users = await db.select_all_users()
    count_baza = await db.count_users()
    active = 0
    block = 0
    counter = 0
    c = 0
    await msg.answer(f"<i>Xabar jo'natilganligi haqidagi to‘liq ma’lumot tez orada yuboriladi</i>")
                                                      # reply_markup=create_main_keyboard(
                                                      #   get_text('uz_latin', 'faq'),
                                                      #   get_text('uz_latin', 'policy'),
                                                      #   get_text('uz_latin', 'statistics'),
                                                      #   get_text('uz_latin', 'technical_problems'),
                                                      #   get_text('uz_latin', 'profile')
                                                      # ))
    for user in users:                                       #type: ignore
        user_id = user[1]
        try:
            await bot.send_media_group(chat_id=user_id,
                                       media=media_group
                                       )
            active += 1
            c += 1

        except Exception:
            block += 1
            continue

        counter += 1

        if counter == 25:
            counter = 0
            await asyncio.sleep(0.5)
    await state.finish()
    await msg.answer(f"SENT: <b>{active}</b>"
                     f"\nBLOCK: <b>{block}</b>"
                     f"\nALL_USERS: <b>{count_baza}</b>")

    active = 0
    block = 0
    counter = 0


@dp.message_handler(state="mediagroup")
async def mediagryopish(msg: types.Message, state: FSMContext):
    if msg.text == "MediaGroup OFF":
        await msg.answer("<b>MEDIA GROUP STATE</b> O'chirildi!")
        await state.finish()


@dp.message_handler(content_types=['video', 'audio', 'voice', 'photo', 'document', 'text'], user_id=SUPER_ADMINS,
                    state="idolish")
async def idvideo(msg: types.Message, state: FSMContext):
    if msg.video:
        await msg.answer(f"<b>VIDEO/CAPTION:</b> \n\n{msg.caption}"
                         f"<b>\n\nVIDEO/ID:</b> \n\n{msg.video.file_id}")
    if msg.audio:
        await msg.answer(f"<b>AUDIO/CAPTION:</b> \n\n{msg.caption}"
                         f"\n\n<b>AUDIO/ID:</b>\n\n{msg.audio.file_id}")
    if msg.voice:
        await msg.answer(f"<b>AUDIO/CAPTION:</b> \n\n{msg.caption}"
                         f"\n\n<b>AUDIO/ID:</b>\n\n{msg.voice.file_id}")
    if msg.photo:
        await msg.answer(f"<b>PHOTO/CAPTION:</b>\n\n{msg.caption}"
                         f"\n\n<b>PHOTO/ID:</b>\n\n{msg.photo[-1].file_id}")
    if msg.document:
        await msg.answer(f"<b>DOCUMENT/CAPTION:</b>\n\n{msg.caption}"
                         f"\n\n<b>DOCUMENT/ID:</b>\n\n{msg.document.file_id}")

    if msg.text == "ID OFF":
        await msg.answer("<b>ID OLISH STATE</b> O'chirildi!")
        await state.finish()

    elif msg.text:
        await msg.answer("Сиз <b>ID OLISH STATE</b>дасиз."
                         "\n\nChiqish uchun <b>ID o'chirish</b> tugmasini bosing!")


yes_no = InlineKeyboardMarkup(row_width=2)
yes_no.insert(InlineKeyboardButton(text='Ha',
                                   callback_data='yes'))            # type: ignore
yes_no.insert(InlineKeyboardButton(text= "Yo'q",
                                   callback_data='no_again'))       # type: ignore

@dp.message_handler(content_types=['text'], state="elon", user_id=SUPER_ADMINS)
async def elonj(msg: types.Message, state: FSMContext):
    if msg.text == "Cancel sending messages":
        await msg.answer("<b>E'LON JO'NATISH STATE</b> O'chirildi!")
        await state.finish()

    elif msg.text:
        matn = msg.text
        await msg.answer("<b><i>Yuboradigan xabaringizni tekshirdingizmi?"
                         "\n\n<b>OGOH BO‘LING XABARINGIZ KO‘PCHILIKKA BORADI!!!</b>"
                         "\n\nXabarni yuborasizmi?</i></b>", reply_markup=yes_no)
        await state.update_data(text=matn)
        await state.set_state("yes_no")


@dp.callback_query_handler(state="yes_no")
async def checkyes_no(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    users = await db.select_all_users()
    count_baza = await db.count_users()
    active = 0
    block = 0
    counter = 0
    c_two = 0
    if call.data == "yes":
        await call.message.answer(f"<i>Xabar jo'natilganligi haqidagi to‘liq ma’lumot tez orada yuboriladi</i>")
                                                      # reply_markup=create_main_keyboard(
                                                      #   get_text('uz_latin', 'faq'),
                                                      #   get_text('uz_latin', 'policy'),
                                                      #   get_text('uz_latin', 'statistics'),
                                                      #   get_text('uz_latin', 'technical_problems'),
                                                      #   get_text('uz_latin', 'profile')
                                                      # ))
        await state.finish()

        for user in users:                          #type: ignore
            user_id = user[1]
            try:
                await bot.send_message(chat_id=user_id,
                                       text=data['text']
                                       )
                active += 1
                c_two += 1

            except Exception:
                block += 1
                continue

            counter += 1

            if counter == 25:
                counter = 0
                await asyncio.sleep(0.5)

            if c_two == 1500:
                await call.message.answer(text=f"Xabar {c_two} ta foydalanuvchiga yuborildi!"
                                               f"\n\n3 daqiqadan so‘ng yana yuboriladi!")
                await asyncio.sleep(180)
                c_two = 0

        await call.message.answer(f"SENT: <b>{active}</b>"
                                  f"\nBLOCK: <b>{block}</b>"
                                  f"\nALL_USERS: <b>{count_baza}</b>")

    elif call.data == "no_again":
        await call.message.answer("Xabaringizni qayta yuborishingiz mumkin!")
        await state.set_state("elon")

    active = 0
    block = 0
    counter = 0

    await call.message.delete()



def extract_chat_id(text):
    pattern = r'Telegram ID:\s+(\d+)'
    match = re.search(pattern, text)

    if match:
        chat_id = match.group(1)
        return chat_id
    else:
        return None


@dp.message_handler(text=['/ban'], user_id=SUPER_ADMINS, state="*")
async def ban_user(msg: types.Message, state: FSMContext):
    if msg.reply_to_message:
        user_id = extract_chat_id(msg.reply_to_message.text)
        if user_id:
            data = await db.select_user(telegram_id=user_id)
            if data:
                await state.update_data({"telegram_id": int(data['telegram_id']),                 #type: ignore
                                        "telegram_name": data['telegram_name'],                   #type: ignore
                                        "username": data['username'],                             #type: ignore
                                        "name": data['name'],                                     #type: ignore
                                        "phone": data['phone'],                                   #type: ignore
                                        "region": data['region'],                                 #type: ignore
                                        "city": data['city'],                                     #type: ignore
                                        "language": data['language'],                             #type: ignore
                                        "status": "blocked"})                                     #type: ignore

                datas = await state.get_data()
                await db.update_existing_user(datas)

                await msg.reply(f"Foydalanuvchi @{data['username']} bloklandi.")                  #type: ignore
                await bot.send_message(user_id, get_text(data['language'], 'blocked'))            #type: ignore
        else:
            await msg.answer("Foydalanuvchini bloklash uchun u botga a`zo bo`lganligi"
                             " haqidagi xabardan foydalaning")
    else:
        await msg.answer("Foydalanuvchini bloklash uchun u botga a`zo bo`lganligi"
                             " haqidagi xabardan foydalaning")


@dp.message_handler(text=['/unban'], user_id=SUPER_ADMINS, state="*")
async def unban_user(msg: types.Message, state: FSMContext):
    if msg.reply_to_message:
        user_id = extract_chat_id(msg.reply_to_message.text)
        if user_id:
            data = await db.select_user(telegram_id=user_id)
            if data:
                await state.update_data({"telegram_id": int(data['telegram_id']),                #type: ignore
                                        "telegram_name": data['telegram_name'],                  #type: ignore
                                        "username": data['username'],                            #type: ignore
                                        "name": data['name'],                                    #type: ignore
                                        "phone": data['phone'],                                  #type: ignore
                                        "region": data['region'],                                #type: ignore
                                        "city": data['city'],                                    #type: ignore
                                        "language": data['language'],                            #type: ignore
                                        "status": "unblock"})                                    #type: ignore

                datas = await state.get_data()
                await db.update_existing_user(datas)

                await msg.reply(f"Foydalanuvchi @{data['username']} blokdan chiqarildi.")        #type: ignore
                await bot.send_message(user_id, get_text(data['language'], 'unblocked'))         #type: ignore
        else:
            await msg.answer("Foydalanuvchini blokdan chiqarish uchun u botga a`zo bo`lganligi"
                             " haqidagi xabardan foydalaning")
    else:
        await msg.answer("Foydalanuvchini blokdan chiqarish uchun u botga a`zo bo`lganligi"
                             " haqidagi xabardan foydalaning")

@dp.message_handler(text=['/ban', '/unban'], user_id=SUPER_ADMINS, state="*")
async def ignore_ban_unban(msg: types.Message):
    # Ushbu ishlov beruvchi “/ban” yoki “/unban” bilan xabarlarni e'tiborsiz qoldiradi.
    pass


@dp.message_handler(text='Get User From ID', user_id=SUPER_ADMINS, state='*')
async def ask_id(msg: Message, state: FSMContext):
    await msg.answer("Ma`lumot olmoqchi bo`lgan foydalanuvchi ID sini kiriting: ")
    await state.set_state("get_user_from_id")


@dp.message_handler(user_id=SUPER_ADMINS, state='get_user_from_id')
async def get_user_from_id(msg: Message, state: FSMContext):
    try:
        data = await db.select_user(telegram_id=int(msg.text))
        if data:
            await msg.answer( f"{get_text(data['language'], 'fullname_info')}: {data['name']}\n"          #type: ignore
                            f"{get_text(data['language'], 'contact_info')}: {data['phone']}\n"            #type: ignore
                            f"{get_text(data['language'], 'username')}:  @{data['username']}\n"      #type: ignore
                            f"{get_text(data['language'], 'lang')}: {data['language']}\n"            #type: ignore
                            f"Telegram Name: {data['telegram_name']}\n"                              #type: ignore
                            f"Telegram ID: <code>{data['telegram_id']}</code>\n")                    #type: ignore
        await state.set_state()
    except Exception as e:
        print(f"handlers -> users -> admin_hr -> get_user_from_id() -> {e}")
        await msg.answer("XATO !\nMa`lumot olmoqchi bo`lgan foydalanuvchi ID sini kiriting: ")
        await state.set_state("get_user_from_id")


@dp.message_handler(user_id=SUPER_ADMINS, state="*", is_reply=True)
async def message_for_user(msg: types.Message, state: FSMContext):
    if msg.reply_to_message and msg.reply_to_message.text:
        user_id = extract_chat_id(msg.reply_to_message.text)
        # print(user_id)
        # print(user_id.isdigit())
        if user_id:
            await bot.send_message(user_id, msg.text)
            await msg.answer(f"Xabar <code>{user_id}</code> ga yuborildi !")
        else:
            await msg.answer("Foydalanuvchiga xabar yuborish uchun foydalanuvchi haqidagi"
                             " ma`lumotlar joylashgan xabarga 'reply' qiling!")
    else:
        await msg.answer("2Foydalanuvchiniga xabar yuborish uchun foydalanuvchi haqidagi"
                              " ma`lumotlar joylashgan xabarga 'reply' qiling!")
