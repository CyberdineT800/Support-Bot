import logging

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from loader import sdb, bot, dp
from states.sos_states import ManAdmin
from handlers.sos_man.mz_buttons import button_one
from handlers.sos_man.mz_functions import all_send_man
from handlers.sos_man.mb_bosh_oyna import PAGE_COUNT, buttons_generator, user_id_dict, add_bot_answer, man_bot_dict
from keyboards.inline.sos_inline_keyboards import answer_questions_two, check_bot_answer, create_user_check_ikeys


@dp.callback_query_handler(state=ManAdmin.bot_one)
async def adm_answer_fone(call: CallbackQuery, state: FSMContext):
    user_id = user_id_dict['user_id']
    audio_db = await sdb.select_man_audio(user_id=user_id, turi='audio')
    document_db = await sdb.select_man_document(user_id=user_id, turi='document')
    photo_db = await sdb.select_man_photo(user_id=user_id, turi='photo')
    text_db = await sdb.select_man_text(user_id=user_id, turi='text')
    video_db = await sdb.select_man_video(user_id=user_id, turi='video')
    voice_db = await sdb.select_man_voice(user_id=user_id, turi='voice')

    if call.data == 'edit_bot_answer':
        await call.message.answer('Ushbu javob <b>ℹ️ Bot javobi</b> tugmasini bosganingizda foydalanuvchiga boradi.'
                                  '\nJavob matnini kiriting:')
        await ManAdmin.bot_editone.set()

    elif call.data == 'send_answer':
        bot_answer = await sdb.select_bot_answer(gender='man')
        user_question = 'Sizning matningiz\n\n'

        if call.message.content_type == 'audio':
            await bot.send_audio(chat_id=user_id, audio=call.message.audio.file_id, caption=f'{user_question}'
                                                                                            f'{call.message.caption}')
            await sdb.delete_man_unique(unique_id=call.message.audio.file_unique_id)

        elif call.message.content_type == 'document':
            await bot.send_document(chat_id=user_id, document=call.message.document.file_id,
                                    caption=f'{user_question}{call.message.caption}')
            await sdb.delete_man_unique(unique_id=call.message.document.file_unique_id)

        elif call.message.content_type == 'photo':
            await bot.send_photo(chat_id=user_id, photo=call.message.photo[-1].file_id,
                                 caption=f'{user_question}{call.message.caption}')
            await sdb.delete_man_unique(unique_id=call.message.photo[-1].file_unique_id)

        elif call.message.content_type == 'text':
            user_quest = man_bot_dict['user_question']
            await bot.send_message(chat_id=user_id, text=f"{user_question}{user_quest}"
                                                         f"<b>\n\nJavob:</b>\n\n{bot_answer[0][1]}")            #type: ignore
            await sdb.delete_man_text(text=user_quest)

        elif call.message.content_type == 'video':
            await bot.send_video(chat_id=user_id, video=call.message.video.file_id,
                                 caption=f'{user_question}{call.message.caption}')
            await sdb.delete_man_unique(unique_id=call.message.video.file_unique_id)

        elif call.message.content_type == 'voice':
            await bot.send_voice(chat_id=user_id, voice=call.message.voice.file_id,
                                 caption=f'{user_question}{call.message.caption}')
            await sdb.delete_man_unique(unique_id=call.message.voice.file_unique_id)

        await call.answer('Javob yuborildi va murojaat bazadan o‘chirildi!', show_alert=True)
        user_questions = await sdb.select_all_manuser(user_id=user_id)
        if len(user_questions) > 0:                                                                             #type: ignore
            await call.message.answer('Foydalanuvchi murojaatlari bo‘limiga qaytasizmi?', reply_markup=create_user_check_ikeys("✅ Ha", "❌ Yo`q"))
            await ManAdmin.admin_delone.set()
        else:
            all_users_db = await sdb.select_all_man()
            if len(all_users_db) == 0:                                                                          #type: ignore
                await call.message.answer('Bazada murojaatlar mavjud emas!')
                await state.finish()
            else:
                await call.message.answer('Murojaatlar bo‘limi', reply_markup=await button_one())
                await ManAdmin.SOS_one.set()

    elif call.data == 'back_bot_answer':
        await all_send_man(call=call, markup=await answer_questions_two(), audio_db=audio_db, document_db=document_db,
                           photo_db=photo_db, text_db=text_db, video_db=video_db, voice_db=voice_db, info_msg_id=user_id_dict['info_msg_id'])
        await ManAdmin.SOS_two.set()
        
    await call.message.delete()


@dp.message_handler(state=ManAdmin.bot_addone)
async def bat_one_func(msg: Message):
    try:
        await msg.answer('Javob qabul qilindi! Tasdiqlaysizmi?', reply_markup=check_bot_answer)
        add_bot_answer['add_bot_answer'] = msg.text
        await ManAdmin.bot_two.set()
    except Exception as err:
        logging.info(err)


@dp.callback_query_handler(state=ManAdmin.bot_two)
async def bat_two_func(call: CallbackQuery, state: FSMContext):
    user_id = user_id_dict['user_id']
    audio_db = await sdb.select_man_audio(user_id=user_id, turi='audio')
    document_db = await sdb.select_man_document(user_id=user_id, turi='document')
    photo_db = await sdb.select_man_photo(user_id=user_id, turi='photo')
    text_db = await sdb.select_man_text(user_id=user_id, turi='text')
    video_db = await sdb.select_man_video(user_id=user_id, turi='video')
    voice_db = await sdb.select_man_voice(user_id=user_id, turi='voice')

    if call.data == 'check_bot':
        await sdb.add_bot_answer(text=add_bot_answer['add_bot_answer'], gender='man')
        await all_send_man(call=call, markup=await answer_questions_two(), audio_db=audio_db, document_db=document_db,
                           photo_db=photo_db, text_db=text_db, video_db=video_db, voice_db=voice_db, info_msg_id=user_id_dict['info_msg_id'])
        await ManAdmin.SOS_two.set()

    elif call.data == 'again_bot':
        await call.message.answer('Bot javobini qayta kiriting:')
        await ManAdmin.bot_addone.set()
    elif call.data == 'back_check':
        await all_send_man(call=call, markup=await answer_questions_two(), audio_db=audio_db, document_db=document_db,
                           photo_db=photo_db, text_db=text_db, video_db=video_db, voice_db=voice_db, info_msg_id=user_id_dict['info_msg_id'])
        await ManAdmin.SOS_two.set()
    add_bot_answer.clear()
    await call.message.delete()


@dp.message_handler(state=ManAdmin.bot_editone)
async def adm_answer_ftwo(msg: Message, state: FSMContext):
    try:
        await sdb.update_bot_answerman(text=msg.text, gender='man')
        await msg.answer(text='Bot javobi o‘zgartirildi!')
        
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

            key = buttons_generator(all_messages[:PAGE_COUNT], current_page=current_page, all_pages=all_pages)              #type: ignore
        
            await msg.answer(text='Murojaatlar bo‘limi', reply_markup=key)
        
            await state.update_data(current_page=current_page, 
                                    all_pages=all_pages)
        
            await state.set_state("user_select_messages")
    except Exception as err:
        logging.info(err)
