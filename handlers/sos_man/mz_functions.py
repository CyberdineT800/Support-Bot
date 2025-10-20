from keyboards.inline.sos_inline_keyboards import bot_answer_keyboard
from loader import sdb, bot


async def admin_check_delete(answer, type_db, text=False, boshqa=False):
    if text:
        for n in type_db:
            if n[1] == answer:
                await sdb.delete_man_text(text=answer)
    if boshqa:
        for n in type_db:
            if n[1] == answer:
                await sdb.delete_man_unique(unique_id=answer)


# async def send_audio_man(call, audio_db, markup):
#     for n in audio_db:
#         await call.message.answer_audio(audio=n[0], caption=n[2], reply_markup=markup)


# async def send_document_man(call, document_db, markup):
#     for n in document_db:
#         await call.message.answer_document(document=n[0], caption=n[2], reply_markup=markup)


# async def send_photo_man(call, photo_db, markup):
#     for n in photo_db:
#         await call.message.answer_photo(photo=n[0], caption=n[2], reply_markup=markup)


# async def send_text_man(call, text_db, markup):
#     for n in text_db:
#         await bot.send_message(chat_id=call.message.chat.id,
#                                reply_to_message_id=call.message.message_id+1, 
#                                text=n[1], 
#                                reply_markup=markup)


# async def send_video_man(call, video_db, markup):
#     for n in video_db:
#         await call.message.answer_video(video=n[0], caption=n[2], reply_markup=markup)


# async def send_voice_man(call, voice_db, markup):
#     for n in voice_db:
#         await call.message.answer_voice(voice=n[0], caption=n[2], reply_markup=markup)


async def send_audio_man(call, audio_db, markup, info_msg_id):
    for n in audio_db:
        await bot.send_audio(chat_id=call.message.chat.id, 
                             audio=n[0], 
                             caption=n[2], 
                             reply_markup=markup,
                             reply_to_message_id=info_msg_id)


async def send_document_man(call, document_db, markup, info_msg_id):
    for n in document_db:
        await bot.send_document(chat_id=call.message.chat.id, 
                                document=n[0], 
                                caption=n[2], 
                                reply_markup=markup,
                                reply_to_message_id=info_msg_id)


async def send_photo_man(call, photo_db, markup, info_msg_id):
    for n in photo_db:
        await bot.send_photo(chat_id=call.message.chat.id, 
                             photo=n[0], 
                             caption=n[2], 
                             reply_markup=markup,
                             reply_to_message_id=info_msg_id)


async def send_text_man(call, text_db, markup, info_msg_id):
    for n in text_db:
        await bot.send_message(chat_id=call.message.chat.id,
                               text=n[1], 
                               reply_markup=markup,
                               reply_to_message_id=info_msg_id)


async def send_video_man(call, video_db, markup, info_msg_id):
    for n in video_db:
        await bot.send_video(chat_id=call.message.chat.id, 
                             video=n[0], 
                             caption=n[2], 
                             reply_markup=markup,
                             reply_to_message_id=info_msg_id)


async def send_voice_man(call, voice_db, markup, info_msg_id):
    for n in voice_db:
        await bot.send_voice(chat_id=call.message.chat.id, 
                             voice=n[0], 
                             caption=n[2], 
                             reply_markup=markup,
                             reply_to_message_id=info_msg_id)


async def all_send_man(call, markup, audio_db=None, document_db=None, photo_db=None, text_db=None,
                       video_db=None, voice_db=None, info_msg_id=None):
    if audio_db:
        await send_audio_man(call=call, audio_db=audio_db, markup=markup, info_msg_id=info_msg_id)
    if document_db:
        await send_document_man(call=call, document_db=document_db, markup=markup, info_msg_id=info_msg_id)
    if photo_db:
        await send_photo_man(call=call, photo_db=photo_db, markup=markup, info_msg_id=info_msg_id)
    if text_db:
        await send_text_man(call=call, text_db=text_db, markup=markup, info_msg_id=info_msg_id)
    if video_db:
        await send_video_man(call=call, video_db=video_db, markup=markup, info_msg_id=info_msg_id)
    if voice_db:
        await send_voice_man(call=call, voice_db=voice_db, markup=markup, info_msg_id=info_msg_id)


# ============================ BOT SEND MAN ============================ #
async def bot_answer_content_type(call, bot_answer, bot_dict):
    if call.message.content_type == 'audio':
        bot_dict['audio_caption'] = call.message.caption
        bot_dict['audio_id'] = call.message.audio.file_id
        await call.message.answer_audio(audio=call.message.audio.file_id, caption=f'{call.message.caption}{bot_answer}',
                                        reply_markup=bot_answer_keyboard)

    elif call.message.content_type == 'document':
        bot_dict['document_caption'] = call.message.caption
        bot_dict['document_id'] = call.message.document.file_id
        await call.message.answer_document(document=call.message.document.file_id, caption=f'{call.message.caption}'
                                                                                           f'{bot_answer}',
                                           reply_markup=bot_answer_keyboard)

    elif call.message.content_type == 'photo':
        bot_dict['photo_caption'] = call.message.caption
        bot_dict['photo_id'] = call.message.photo[-1].file_id
        await call.message.answer_photo(photo=call.message.photo[-1].file_id, caption=f'{call.message.caption}'
                                                                                      f'{bot_answer}',
                                        reply_markup=bot_answer_keyboard)

    elif call.message.content_type == 'text':
        bot_dict['user_question'] = call.message.text
        user_question_text = f"Foydalanuvchi savoli:\n\n{call.message.text}"
        bot_dict['user_question_text'] = user_question_text
        await call.message.answer(f'{user_question_text}{bot_answer}', reply_markup=bot_answer_keyboard)

    elif call.message.content_type == 'video':
        bot_dict['video_caption'] = call.message.caption
        bot_dict['video_id'] = call.message.video.file_id
        await call.message.answer_video(video=call.message.video.file_id, caption=f'{call.message.caption}{bot_answer}',
                                        reply_markup=bot_answer_keyboard)

    elif call.message.content_type == 'voice':
        bot_dict['voice_caption'] = call.message.caption
        bot_dict['voice_id'] = call.message.voice.file_id
        await call.message.answer_voice(voice=call.message.voice.file_id, caption=f'{call.message.caption}{bot_answer}',
                                        reply_markup=bot_answer_keyboard)
