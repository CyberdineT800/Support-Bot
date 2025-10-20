from loader import bot

your_question = '<b>Sizning savolingiz:</b>\n\n'
admin_text = '<b>\nMas\'ul shaxs javobi:</b>\n\n'
no_caption = 'Xabaringiz matnsiz!'
caption_answer = your_question + no_caption


# async def admin_answer_func(call, gender_state, info_msg_id):
#     user_question = "Foydalanuvchi savoli:\n\n"
#     if call.message.content_type == 'audio':
#         gender_state['audio_admin_unique'] = call.message.audio.file_unique_id
#         gender_state['audio_admin_caption'] = call.message.caption
#         gender_state['audio_admin_id'] = call.message.audio.file_id
#         await bot.send_audio(chat_id=call.message.chat.id,
#                              audio=call.message.audio.file_id,
#                              caption=f'{user_question}{call.message.caption}',
#                              reply_to_message_id=info_msg_id)

#     elif call.message.content_type == 'document':
#         gender_state['document_admin_unique'] = call.message.document.file_unique_id
#         gender_state['document_admin_caption'] = call.message.caption
#         gender_state['document_admin_id'] = call.message.document.file_id
#         await call.message.answer_document(document=call.message.document.file_id,
#                                            caption=f'{user_question}{call.message.caption}')

#     elif call.message.content_type == 'photo':
#         gender_state['photo_admin_unique'] = call.message.photo[-1].file_unique_id
#         gender_state['photo_admin_caption'] = call.message.caption
#         gender_state['photo_admin_id'] = call.message.photo[-1].file_id
#         await call.message.answer_photo(photo=call.message.photo[-1].file_id,
#                                         caption=f'{user_question}{call.message.caption}')

#     elif call.message.content_type == 'text':
#         gender_state['text_adm_ans'] = call.message.text
#         await call.message.answer(user_question + call.message.text)

#     elif call.message.content_type == 'video':
#         gender_state['video_admin_unique'] = call.message.video.file_unique_id
#         gender_state['video_admin_caption'] = call.message.caption
#         gender_state['video_admin_id'] = call.message.video.file_id
#         await call.message.answer_video(video=call.message.video.file_id, caption=f'{user_question}'
#                                                                                   f'{call.message.caption}')

#     elif call.message.content_type == 'voice':
#         gender_state['voice_admin_unique'] = call.message.voice.file_unique_id
#         gender_state['voice_admin_caption'] = call.message.caption
#         gender_state['voice_admin_id'] = call.message.voice.file_id
#         await call.message.answer_voice(voice=call.message.voice.file_id,
#                                         caption=f'{user_question}{call.message.caption}')
#     await call.message.answer('Javobingizni kiriting:')


async def admin_answer_func(call, gender_state, info_msg_id):
    user_question = "Foydalanuvchi savoli:\n\n"
    
    if call.message.content_type == 'audio':
        gender_state['audio_admin_unique'] = call.message.audio.file_unique_id
        gender_state['audio_admin_caption'] = call.message.caption
        gender_state['audio_admin_id'] = call.message.audio.file_id
        await bot.send_audio(chat_id=call.message.chat.id,
                             audio=call.message.audio.file_id,
                             caption=f'{user_question}{call.message.caption}',
                             reply_to_message_id=info_msg_id)

    elif call.message.content_type == 'document':
        gender_state['document_admin_unique'] = call.message.document.file_unique_id
        gender_state['document_admin_caption'] = call.message.caption
        gender_state['document_admin_id'] = call.message.document.file_id
        await bot.send_document(chat_id=call.message.chat.id,
                                document=call.message.document.file_id,
                                caption=f'{user_question}{call.message.caption}',
                                reply_to_message_id=info_msg_id)

    elif call.message.content_type == 'photo':
        gender_state['photo_admin_unique'] = call.message.photo[-1].file_unique_id
        gender_state['photo_admin_caption'] = call.message.caption
        gender_state['photo_admin_id'] = call.message.photo[-1].file_id
        await bot.send_photo(chat_id=call.message.chat.id,
                             photo=call.message.photo[-1].file_id,
                             caption=f'{user_question}{call.message.caption}',
                             reply_to_message_id=info_msg_id)

    elif call.message.content_type == 'text':
        gender_state['text_adm_ans'] = call.message.text
        await bot.send_message(chat_id=call.message.chat.id,
                               text=user_question + call.message.text,
                               reply_to_message_id=info_msg_id)

    elif call.message.content_type == 'video':
        gender_state['video_admin_unique'] = call.message.video.file_unique_id
        gender_state['video_admin_caption'] = call.message.caption
        gender_state['video_admin_id'] = call.message.video.file_id
        await bot.send_video(chat_id=call.message.chat.id,
                             video=call.message.video.file_id,
                             caption=f'{user_question}{call.message.caption}',
                             reply_to_message_id=info_msg_id)

    elif call.message.content_type == 'voice':
        gender_state['voice_admin_unique'] = call.message.voice.file_unique_id
        gender_state['voice_admin_caption'] = call.message.caption
        gender_state['voice_admin_id'] = call.message.voice.file_id
        await bot.send_voice(chat_id=call.message.chat.id,
                             voice=call.message.voice.file_id,
                             caption=f'{user_question}{call.message.caption}',
                             reply_to_message_id=info_msg_id)
                             
    await call.message.answer('Javobingizni kiriting:')



async def audio_answer_admin(user_id, gender_id, gender_caption):
    await bot.send_audio(chat_id=user_id, audio=gender_id, caption=f"{your_question}{gender_caption}")


async def document_answer_admin(user_id, gender_id, gender_caption):
    await bot.send_document(chat_id=user_id, document=gender_id, caption=f"{your_question}{gender_caption}")


async def photo_answer_admin(user_id, gender_id, gender_caption):
    await bot.send_photo(chat_id=user_id, photo=gender_id, caption=f"{your_question}{gender_caption}")


async def text_answer_admin(user_id, gender_dict):
    await bot.send_message(chat_id=user_id, text=f"{your_question}{gender_dict}")


async def video_answer_admin(user_id, gender_id, gender_caption):
    await bot.send_video(chat_id=user_id, video=gender_id, caption=f"{your_question}{gender_caption}")


async def voice_answer_admin(user_id, gender_id, gender_caption):
    await bot.send_voice(chat_id=user_id, voice=gender_id, caption=f"{your_question}{gender_caption}")


# =============================== Guruhdan habarlarni userga yuboruvchi funksiyalar, admin javobi bo'lib boradi

async def audio_answer_yes(user_id, caption_admin, gender_id):
    await bot.send_audio(chat_id=user_id, audio=gender_id, caption=f"{admin_text}{caption_admin}")


async def document_answer_yes(user_id, caption_admin, gender_id):
    await bot.send_document(chat_id=user_id, document=gender_id, caption=f"{admin_text}{caption_admin}")


async def photo_answer_yes(user_id, caption_admin, gender_id):
    await bot.send_photo(chat_id=user_id, photo=gender_id, caption=f"{admin_text}{caption_admin}")


async def text_answer_yes(user_id, gender_text):
    await bot.send_message(chat_id=user_id, text=f'{admin_text}{gender_text}')


async def video_answer_yes(caption_admin, user_id, gender_id):
    await bot.send_video(chat_id=user_id, video=gender_id, caption=f"{admin_text}{caption_admin}")


async def voice_answer_yes(caption_admin, user_id, gender_id):
    await bot.send_voice(chat_id=user_id, voice=gender_id, caption=f"{admin_text}{caption_admin}")


# =============================== Userdan kelgan audio/doc/photo/text/video/voice turdagi habarlarga
# audio/doc/photo/text/video/voice javob yuboruvchi funksiyalar

async def admin_answer_yes_audio(user_id, admin_javobi, user_savoli):
    for n in user_savoli.keys():
        if n == 'audio_admin_id':
            await audio_answer_admin(user_id=user_id, gender_id=user_savoli[n],
                                     gender_caption=user_savoli['audio_admin_caption'])
            await audio_answer_yes(user_id=user_id, caption_admin=admin_javobi['audio_caption'],
                                   gender_id=admin_javobi['audio_id'])
        elif n == 'document_admin_id':
            await document_answer_admin(user_id=user_id, gender_id=user_savoli[n],
                                        gender_caption=user_savoli['document_admin_caption'])
            await audio_answer_yes(user_id=user_id, caption_admin=admin_javobi['audio_caption'],
                                   gender_id=admin_javobi['audio_id'])
        elif n == 'photo_admin_id':
            await photo_answer_admin(user_id=user_id, gender_id=user_savoli[n],
                                     gender_caption=user_savoli['photo_admin_caption'])
            await audio_answer_yes(user_id=user_id, caption_admin=admin_javobi['audio_caption'],
                                   gender_id=admin_javobi['audio_id'])
        elif n == 'text_adm_ans':
            await text_answer_admin(user_id=user_id, gender_dict=user_savoli[n])
            await audio_answer_yes(user_id=user_id, caption_admin=admin_javobi['audio_caption'],
                                   gender_id=admin_javobi['audio_id'])
        elif n == 'video_admin_id':
            await video_answer_admin(user_id=user_id, gender_id=user_savoli[n],
                                     gender_caption=user_savoli['video_admin_caption'])
            await audio_answer_yes(user_id=user_id, caption_admin=admin_javobi['audio_caption'],
                                   gender_id=admin_javobi['audio_id'])
        elif n == 'voice_admin_id':
            await voice_answer_admin(user_id=user_id, gender_id=user_savoli[n],
                                     gender_caption=user_savoli['voice_admin_caption'])
            await audio_answer_yes(user_id=user_id, caption_admin=admin_javobi['audio_caption'],
                                   gender_id=admin_javobi['audio_id'])


async def admin_answer_yes_document(user_id, admin_javobi, user_savoli):
    for n in user_savoli.keys():
        if n == 'audio_admin_id':
            await audio_answer_admin(user_id=user_id, gender_id=user_savoli[n],
                                     gender_caption=user_savoli['audio_admin_caption'])
            await document_answer_yes(user_id=user_id, caption_admin=admin_javobi['document_caption'],
                                      gender_id=admin_javobi['document_id'])
        elif n == 'document_admin_id':
            await document_answer_admin(user_id=user_id, gender_id=user_savoli[n],
                                        gender_caption=user_savoli['document_admin_caption'])
            await document_answer_yes(user_id=user_id, caption_admin=admin_javobi['document_caption'],
                                      gender_id=admin_javobi['document_id'])
        elif n == 'photo_admin_id':
            await photo_answer_admin(user_id=user_id, gender_id=user_savoli[n],
                                     gender_caption=user_savoli['photo_admin_caption'])
            await document_answer_yes(user_id=user_id, caption_admin=admin_javobi['document_caption'],
                                      gender_id=admin_javobi['document_id'])
        elif n == 'text_adm_ans':
            await text_answer_admin(user_id=user_id, gender_dict=user_savoli[n])
            await document_answer_yes(user_id=user_id, caption_admin=admin_javobi['document_caption'],
                                      gender_id=admin_javobi['document_id'])
        elif n == 'video_admin_id':
            await video_answer_admin(user_id=user_id, gender_id=user_savoli[n],
                                     gender_caption=user_savoli['video_admin_caption'])
            await document_answer_yes(user_id=user_id, caption_admin=admin_javobi['document_caption'],
                                      gender_id=admin_javobi['document_id'])
        elif n == 'voice_admin_id':
            await voice_answer_admin(user_id=user_id, gender_id=user_savoli[n],
                                     gender_caption=user_savoli['voice_admin_caption'])
            await document_answer_yes(user_id=user_id, caption_admin=admin_javobi['document_caption'],
                                      gender_id=admin_javobi['document_id'])


async def admin_answer_yes_photo(user_id, admin_javobi, user_savoli):
    for n in user_savoli.keys():
        if n == 'audio_admin_id':
            await audio_answer_admin(user_id=user_id, gender_id=user_savoli[n],
                                     gender_caption=user_savoli['audio_admin_caption'])
            await photo_answer_yes(user_id=user_id, caption_admin=admin_javobi['photo_caption'],
                                   gender_id=admin_javobi['photo_id'])
        elif n == 'document_admin_id':
            await document_answer_admin(user_id=user_id, gender_id=user_savoli[n],
                                        gender_caption=user_savoli['document_admin_caption'])
            await photo_answer_yes(user_id=user_id, caption_admin=admin_javobi['photo_caption'],
                                   gender_id=admin_javobi['photo_id'])
        elif n == 'photo_admin_id':
            await photo_answer_admin(user_id=user_id, gender_id=user_savoli[n],
                                     gender_caption=user_savoli['photo_admin_caption'])
            await photo_answer_yes(user_id=user_id, caption_admin=admin_javobi['photo_caption'],
                                   gender_id=admin_javobi['photo_id'])
        elif n == 'text_adm_ans':
            await text_answer_admin(user_id=user_id, gender_dict=user_savoli[n])
            await photo_answer_yes(user_id=user_id, caption_admin=admin_javobi['photo_caption'],
                                   gender_id=admin_javobi['photo_id'])
        elif n == 'video_admin_id':
            await video_answer_admin(user_id=user_id, gender_id=user_savoli[n],
                                     gender_caption=user_savoli['video_admin_caption'])
            await photo_answer_yes(user_id=user_id, caption_admin=admin_javobi['photo_caption'],
                                   gender_id=admin_javobi['photo_id'])
        elif n == 'voice_admin_id':
            await voice_answer_admin(user_id=user_id, gender_id=user_savoli[n],
                                     gender_caption=user_savoli['voice_admin_caption'])
            await photo_answer_yes(user_id=user_id, caption_admin=admin_javobi['photo_caption'],
                                   gender_id=admin_javobi['photo_id'])


async def admin_answer_yes_text(user_id, admin_javobi, user_savoli):
    for n in user_savoli.keys():
        if n == 'audio_admin_id':
            await audio_answer_admin(user_id=user_id, gender_id=user_savoli[n],
                                     gender_caption=user_savoli['audio_admin_caption'])
            await text_answer_yes(user_id=user_id, gender_text=admin_javobi)
        elif n == 'document_admin_id':
            await document_answer_admin(user_id=user_id, gender_id=user_savoli[n],
                                        gender_caption=user_savoli['document_admin_caption'])
            await text_answer_yes(user_id=user_id, gender_text=admin_javobi)
        elif n == 'photo_admin_id':
            await photo_answer_admin(user_id=user_id, gender_id=user_savoli[n],
                                     gender_caption=user_savoli['photo_admin_caption'])
            await text_answer_yes(user_id=user_id, gender_text=admin_javobi)
        elif n == 'text_adm_ans':
            await text_answer_admin(user_id=user_id, gender_dict=user_savoli[n])
            await text_answer_yes(user_id=user_id, gender_text=admin_javobi)
        elif n == 'video_admin_id':
            await video_answer_admin(user_id=user_id, gender_id=user_savoli[n],
                                     gender_caption=user_savoli['video_admin_caption'])
            await text_answer_yes(user_id=user_id, gender_text=admin_javobi)
        elif n == 'voice_admin_id':
            await voice_answer_admin(user_id=user_id, gender_id=user_savoli[n],
                                     gender_caption=user_savoli['voice_admin_caption'])
            await text_answer_yes(user_id=user_id, gender_text=admin_javobi)


async def admin_answer_yes_video(user_id, admin_javobi, user_savoli):
    for n in user_savoli.keys():
        if n == 'audio_admin_id':
            await audio_answer_admin(user_id=user_id, gender_id=user_savoli[n],
                                     gender_caption=user_savoli['audio_admin_caption'])
            await video_answer_yes(user_id=user_id, caption_admin=admin_javobi['video_caption'],
                                   gender_id=admin_javobi['video_id'])
        elif n == 'document_admin_id':
            await document_answer_admin(user_id=user_id, gender_id=user_savoli[n],
                                        gender_caption=user_savoli['document_admin_caption'])
            await video_answer_yes(user_id=user_id, caption_admin=admin_javobi['video_caption'],
                                   gender_id=admin_javobi['video_id'])
        elif n == 'photo_admin_id':
            await photo_answer_admin(user_id=user_id, gender_id=user_savoli[n],
                                     gender_caption=user_savoli['photo_admin_caption'])
            await video_answer_yes(user_id=user_id, caption_admin=admin_javobi['video_caption'],
                                   gender_id=admin_javobi['video_id'])
        elif n == 'text_adm_ans':
            await text_answer_admin(user_id=user_id, gender_dict=user_savoli[n])
            await video_answer_yes(user_id=user_id, caption_admin=admin_javobi['video_caption'],
                                   gender_id=admin_javobi['video_id'])
        elif n == 'video_admin_id':
            await video_answer_admin(user_id=user_id, gender_id=user_savoli[n],
                                     gender_caption=user_savoli['video_admin_caption'])
            await video_answer_yes(user_id=user_id, caption_admin=admin_javobi['video_caption'],
                                   gender_id=admin_javobi['video_id'])
        elif n == 'voice_admin_id':
            await voice_answer_admin(user_id=user_id, gender_id=user_savoli[n],
                                     gender_caption=user_savoli['voice_admin_caption'])
            await video_answer_yes(user_id=user_id, caption_admin=admin_javobi['video_caption'],
                                   gender_id=admin_javobi['video_id'])


async def admin_answer_yes_voice(user_id, admin_javobi, user_savoli):
    for n in user_savoli.keys():
        if n == 'audio_admin_id':
            await audio_answer_admin(user_id=user_id, gender_id=user_savoli[n],
                                     gender_caption=user_savoli['audio_admin_caption'])
            await voice_answer_yes(user_id=user_id, caption_admin=admin_javobi['voice_caption'],
                                   gender_id=admin_javobi['voice_id'])
        elif n == 'document_admin_id':
            await document_answer_admin(user_id=user_id, gender_id=user_savoli[n],
                                        gender_caption=user_savoli['document_admin_caption'])
            await voice_answer_yes(user_id=user_id, caption_admin=admin_javobi['voice_caption'],
                                   gender_id=admin_javobi['voice_id'])
        elif n == 'photo_admin_id':
            await photo_answer_admin(user_id=user_id, gender_id=user_savoli[n],
                                     gender_caption=user_savoli['photo_admin_caption'])
            await voice_answer_yes(user_id=user_id, caption_admin=admin_javobi['voice_caption'],
                                   gender_id=admin_javobi['voice_id'])
        elif n == 'text_adm_ans':
            await text_answer_admin(user_id=user_id, gender_dict=user_savoli[n])
            await voice_answer_yes(user_id=user_id, caption_admin=admin_javobi['voice_caption'],
                                   gender_id=admin_javobi['voice_id'])
        elif n == 'video_admin_id':
            await video_answer_admin(user_id=user_id, gender_id=user_savoli[n],
                                     gender_caption=user_savoli['video_admin_caption'])
            await voice_answer_yes(user_id=user_id, caption_admin=admin_javobi['voice_caption'],
                                   gender_id=admin_javobi['voice_id'])
        elif n == 'voice_admin_id':
            await voice_answer_admin(user_id=user_id, gender_id=user_savoli[n],
                                     gender_caption=user_savoli['voice_admin_caption'])
            await voice_answer_yes(user_id=user_id, caption_admin=admin_javobi['voice_caption'],
                                   gender_id=admin_javobi['voice_id'])
