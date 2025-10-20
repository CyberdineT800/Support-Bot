import logging
from aiogram import types

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import ChatTypeFilter, Command, AdminFilter
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message, Update

from filters import IsGroup
from loader import sdb, dp, bot, db
from data.translation import get_text
from states.sos_states import ManAdmin
from data.config import MAN_GROUP
from handlers.sos_man.mz_buttons import button_one
from handlers.users.help import create_personal_infos
from handlers.sos_all.admin_functions import admin_answer_func
from handlers.sos_man.mz_functions import all_send_man, admin_check_delete, bot_answer_content_type
from keyboards.inline.sos_inline_keyboards import answer_questions_two, unblock_inline_btn

user_id_dict = {}
add_bot_answer = {}
man_dict_one = {}
man_bot_dict = {}

son = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]

PAGE_COUNT = 25

def buttons_generator(database: list, current_page: int, all_pages: int):
    key = InlineKeyboardMarkup(
        row_width=3
    )
    
    for i in database:
        key.insert(
            InlineKeyboardButton(
                text=str(i[0]),                  # user full_namesi      
                callback_data=f"message_{i[1]}"  # user_idsi
            ))                                                                    #type: ignore

    key.add(
        InlineKeyboardButton(
            text="⬅️ Orqaga",
            callback_data="prev"
        ))                                                                        #type: ignore

    key.insert(
        InlineKeyboardButton(
            text=f"{current_page}/{all_pages}",
            callback_data="pages"
        ))                                                                        #type: ignore

    key.insert(InlineKeyboardButton(
        text="Oldinga ➡️",
        callback_data="next"
    ))                                                                            #type: ignore
    
    return key


class CommandMan(Command):
    def __init__(self):
        super().__init__(['problems'])
        

@dp.message_handler(AdminFilter(), commands=['problems'], state='*')
#@dp.message_handler(commands=['dasturiy_savollar'], state='*')
async def questions_command_func(msg: Message, state: FSMContext):
    if msg.chat.id == int(MAN_GROUP):
        try:
            # admins = await sdb.all_admins()
            # print(await bot.get_chat_member(msg.chat.id, msg.from_user.id))
            
            # print(msg.from_user.id)
            all_messages = await sdb.select_all_man()  # db.get_all_message(_)
            
            # PEP8
            if all_messages:
                current_page = 1
                # if len(all_messages) % 25 == 0 else
                if len(all_messages) % PAGE_COUNT == 0:
                    all_pages = len(all_messages) // PAGE_COUNT
                else:
                    all_pages = len(all_messages) // PAGE_COUNT + 1
                # 200 // 25

                #####
                all_messages = await sdb.select_question_man()
                #####

                key = buttons_generator(all_messages[:PAGE_COUNT], current_page=current_page, all_pages=all_pages)   #type: ignore
                
                await msg.answer(text='Murojaatlar bo‘limi', reply_markup=key)
                
                await state.update_data(current_page=current_page, 
                                        all_pages=all_pages)
                
                await state.set_state("user_select_messages")
            else:
                await msg.answer(text="Xabarlar hozircha mavjud emas")

    
            # all_users_db = await sdb.select_all_man()
            # if len(all_users_db) == 0:
            #     await msg.answer('Bazada savollar mavjud emas!')
            # else:
            #     await msg.answer('❓ Savollar bo‘limi', reply_markup=await button_one())
            
            await msg.delete()
            #await ManAdmin.SOS_one.set()
        except Exception as err:
            logging.info(err)


# @dp.callback_query_handler(state="user_select_messages", text_contains="message_")
# async def get_user_details(call: types.CallbackQuery, state: FSMContext):
#     await call.answer(
#         text=f"You are selected {call.data.split('_')[1]} number",
#         show_alert=True
#     )
    
#     await ManAdmin.SOS_one.set()


@dp.callback_query_handler(state="user_select_messages", text_contains="message_")
async def group_ans_two(call: CallbackQuery, state: FSMContext):
    user_id = int(call.data.split('_')[1])
    audio_db = await sdb.select_man_audio(user_id=user_id, turi='audio')
    document_db = await sdb.select_man_document(user_id=user_id, turi='document')
    photo_db = await sdb.select_man_photo(user_id=user_id, turi='photo')
    text_db = await sdb.select_man_text(user_id=user_id, turi='text')
    video_db = await sdb.select_man_video(user_id=user_id, turi='video')
    voice_db = await sdb.select_man_voice(user_id=user_id, turi='voice')
    user_id_dict['user_id'] = user_id
    
    user = await db.select_user(telegram_id=user_id)
    infos = create_personal_infos(selected_language=user['language'], datas=user)                               #type: ignore
    
    info_msg = await call.message.answer(text=infos, reply_markup=unblock_inline_btn(user))
    user_id_dict['info_msg_id'] = info_msg.message_id
    
    try:
        await all_send_man(call=call, markup=await answer_questions_two(), audio_db=audio_db, document_db=document_db,
                           photo_db=photo_db, text_db=text_db, video_db=video_db, voice_db=voice_db,
                           info_msg_id=user_id_dict['info_msg_id'])
    except Exception as err:
        logging.info(err)
    
    await ManAdmin.SOS_two.set()
    await call.message.delete() 



@dp.callback_query_handler(state="*", text_contains="block_user")
async def user_set_permissions(call: CallbackQuery, state: FSMContext):
    datas = call.data.split('_')
    action = datas[0]
    user_id = int(datas[-1])
    
    if action == 'block':
        data = await db.select_user(telegram_id=user_id)
        await state.update_data({"telegram_id": int(data['telegram_id']),                             #type: ignore
                                 "telegram_name": data['telegram_name'],                              #type: ignore
                                 "username": data['username'],                                        #type: ignore
                                 "name": data['name'],                                                #type: ignore
                                 "phone": data['phone'],                                              #type: ignore
                                 "region": data['region'],                                            #type: ignore
                                 "city": data['city'],                                                #type: ignore
                                 "language": data['language'],                                        #type: ignore
                                 "status": "blocked"})
    
        data = await db.update_existing_user(await state.get_data())
    
        await call.message.reply(f"Foydalanuvchi @{data['username']} bloklandi.")                     #type: ignore
        await bot.send_message(user_id, get_text(data['language'], 'blocked'))                        #type: ignore
        await call.message.edit_reply_markup(reply_markup=unblock_inline_btn(data))
    else:
        data = await db.select_user(telegram_id=user_id)
        await state.update_data({"telegram_id": int(data['telegram_id']),                             #type: ignore
                                 "telegram_name": data['telegram_name'],                              #type: ignore
                                 "username": data['username'],                                        #type: ignore
                                 "name": data['name'],                                                #type: ignore
                                 "phone": data['phone'],                                              #type: ignore
                                 "region": data['region'],                                            #type: ignore
                                 "city": data['city'],                                                #type: ignore
                                 "language": data['language'],                                        #type: ignore
                                 "status": "unblock"}) 
    
    
        data = await db.update_existing_user(await state.get_data())
    
        await call.message.reply(f"Foydalanuvchi @{data['username']} blokdan chiqarildi.")           #type: ignore
        await bot.send_message(user_id, get_text(data['language'], 'unblocked'))                     #type: ignore
        await call.message.edit_reply_markup(reply_markup=unblock_inline_btn(data))


@dp.callback_query_handler(state="user_select_messages")
async def select_message_handler(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()

    call_data = call.data
    current_page = data['current_page']
    all_pages = data['all_pages']
    
    if call.data == "prev":
        if current_page == 1:
            current_page = all_pages
        else:
            current_page -= 1
    if call.data == 'next':
        if current_page == all_pages:
            current_page = 1
        else:
            current_page += 1

    all_messages = await sdb.select_question_man()
    all_messages = all_messages[(current_page - 1) * PAGE_COUNT: current_page * PAGE_COUNT]

    key = buttons_generator(all_messages, current_page, all_pages)
    
    await call.message.answer(text='Murojaatlar bo‘limi', reply_markup=key)
    await state.update_data(current_page=current_page, all_pages=all_pages)
    
    await call.message.delete()
    

@dp.callback_query_handler(state=ManAdmin.SOS_two)
async def group_ans_three(call: CallbackQuery, state: FSMContext):
    bot_db = await sdb.select_bot_answer(gender='man')
    user_id = user_id_dict['user_id']
    audio_db = await sdb.select_man_audio(user_id=user_id, turi='audio')
    document_db = await sdb.select_man_document(user_id=user_id, turi='document')
    photo_db = await sdb.select_man_photo(user_id=user_id, turi='photo')
    text_db = await sdb.select_man_text(user_id=user_id, turi='text')
    video_db = await sdb.select_man_video(user_id=user_id, turi='video')
    voice_db = await sdb.select_man_voice(user_id=user_id, turi='voice')
    
    try:
        if call.data == 'bot_answer':
            if len(bot_db) == 0:                                                                                 #type: ignore
                await call.message.answer('Javob kiritilmagan! Bot javobini kiriting.\n\nUshbu javob <b>ℹ Bot'
                                          'javobi</b> tugmasini bosganingizda foydalanuvchiga boradi')
                await ManAdmin.bot_addone.set()
            else:
                bot_answer = f'\n\n<b>ℹ Bot javobi:\n\n{bot_db[0][1]}</b>'                                        #type: ignore
                await bot_answer_content_type(call=call, bot_answer=bot_answer, bot_dict=man_bot_dict)
                await ManAdmin.bot_one.set()
        elif call.data == 'admin_answer':
            await admin_answer_func(call=call, gender_state=man_dict_one, info_msg_id=user_id_dict['info_msg_id'])
            await ManAdmin.admin_one.set()
        elif call.data == 'delete_answer':
            if call.message.content_type == 'audio':
                await admin_check_delete(answer=call.message.audio.file_unique_id,
                                         type_db=audio_db, boshqa=True)
            elif call.message.content_type == 'document':
                await admin_check_delete(answer=call.message.document.file_unique_id,
                                         type_db=document_db, boshqa=True)
            elif call.message.content_type == 'photo':
                await admin_check_delete(answer=call.message.photo[-1].file_unique_id,
                                         type_db=photo_db, boshqa=True)
            elif call.message.content_type == 'text':
                await admin_check_delete(answer=call.message.text, type_db=text_db,
                                         text=True)
            elif call.message.content_type == 'video':
                await admin_check_delete(answer=call.message.video.file_unique_id,
                                         type_db=video_db, boshqa=True)
            elif call.message.content_type == 'voice':
                await admin_check_delete(answer=call.message.voice.file_unique_id,
                                         type_db=voice_db, boshqa=True)
            await call.answer(text='Murojaat bazadan o‘chirildi!', show_alert=True)

            await call.message.delete()
            
            all_users_db = await sdb.select_all_man()
            user_questions = await sdb.select_all_manuser(user_id=user_id)
            
            if len(user_questions) == 0:                                                                 #type: ignore
                if len(all_users_db) == 0:                                                               #type: ignore
                    await call.message.answer('Bazada murojaat mavjud emas!')
                    await state.finish()
                else:
                    all_messages = await sdb.select_all_man()  # db.get_all_message(_)
                    # PEP8
                    if all_messages:
                        current_page = 1 
                        # if len(all_messages) % 25 == 0 else
                        if len(all_messages) % PAGE_COUNT == 0:
                            all_pages = len(all_messages) // PAGE_COUNT
                        else:
                            all_pages = len(all_messages) // PAGE_COUNT + 1
                        # 200 // 25

                        #####
                        all_messages = await sdb.select_question_man()
                        #####

                        key = buttons_generator(all_messages[:PAGE_COUNT], current_page=current_page, all_pages=all_pages) #type: ignore

                        await call.message.answer(text='Murojaatlar bo‘limi', reply_markup=key)

                        await state.update_data(current_page=current_page, 
                                                all_pages=all_pages)

                        await state.set_state("user_select_messages")
            elif call.data == 'back_answer_true':
                all_messages = await sdb.select_all_man()  # db.get_all_message(_)
                # PEP8
                if all_messages:
                    current_page = 1
                    # if len(all_messages) % 25 == 0 else
                    if len(all_messages) % PAGE_COUNT == 0:
                        all_pages = len(all_messages) // PAGE_COUNT
                    else:
                        all_pages = len(all_messages) // PAGE_COUNT + 1
                    # 200 // 25

                    #####
                    all_messages = await sdb.select_question_man()
                    #####

                    key = buttons_generator(all_messages[:PAGE_COUNT], current_page=current_page, all_pages=all_pages)  #type: ignore

                    await call.message.answer(text='Murojaatlar bo‘limi', reply_markup=key)

                    await state.update_data(current_page=current_page, 
                                            all_pages=all_pages)

                    await state.set_state("user_select_messages")
            elif call.data == 'back_answer_false':
                all_users_db = await sdb.select_all_man() 
                if len(all_users_db) == 0:                                                                              #type: ignore
                    await call.message.answer('Bazada murojaatlar mavjud emas!')
                    await state.finish()
                else:
                    all_messages = await sdb.select_all_man()  # db.get_all_message(_)
                    # PEP8
                    if all_messages:
                        current_page = 1
                        # if len(all_messages) % 25 == 0 else
                        if len(all_messages) % PAGE_COUNT == 0:
                            all_pages = len(all_messages) // PAGE_COUNT
                        else:
                            all_pages = len(all_messages) // PAGE_COUNT + 1
                        # 200 // 25

                        #####
                        all_messages = await sdb.select_question_man()
                        #####

                        key = buttons_generator(all_messages[:PAGE_COUNT], current_page=current_page, all_pages=all_pages)  #type: ignore

                        await call.message.answer(text='Murojaatlar bo‘limi', reply_markup=key)

                        await state.update_data(current_page=current_page, 
                                                all_pages=all_pages)

                        await state.set_state("user_select_messages")
                
        await call.message.delete()
    
    except Exception as err:
        logging.info(err)
