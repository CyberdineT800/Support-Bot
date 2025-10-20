import logging
from typing import List
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery

from data.config import MAN_GROUP
from data.statistics import update_stats
from handlers.users.help import is_registered
from filters.blockeds import BlockedUserFilter
from data.translation import get_text, get_values_for_key
from keyboards.default.start_dk import create_main_keyboard
from keyboards.default.bottons import create_cancel_button, start_menu, create_start_menu
from keyboards.inline.sos_inline_keyboards import create_user_check_ikeys, create_user_yes_no

from loader import dp, sdb, db, bot
from states.sos_states import Man_Woman_State, Man_State


async def first_check_man(call, user_id, text_id=None, any_id=None, m_id=False, unique=False):
    try:
        data = await db.select_user(telegram_id=user_id)
        if call.data == 'user_yes':
            man_questions = await sdb.select_all_manuser(user_id=user_id)
            if len(man_questions) < 5:                                                                                                          #type: ignore
                await bot.send_message(chat_id=MAN_GROUP,
                                       text='Botga yangi murojaat qabul qilindi! Ko‘rish uchun /problems '
                                            'buyrug‘ini kiriting')
                await call.message.answer(f"{get_text(data['language'], 'message_accepted')}",                                                  #type: ignore
                                          reply_markup=create_user_check_ikeys(f"{get_text(data['language'], 'yestxt')}",                       #type: ignore
                                                                               f"{get_text(data['language'], 'notxt')}"))                       #type: ignore
                await Man_State.user_checkone.set()
                
                update_stats("problem")
            else:
                await call.message.answer(text=f"{get_text(data['language'], 'message_arranged')}",                                             #type: ignore
                                          reply_markup=await create_start_menu(data.get('language', 'uz_latin'), is_reg=True))                  #type: ignore
        elif call.data == 'user_no_again':
            if m_id:
                await sdb.delete_man_id(m_id=text_id)
            elif unique:
                await sdb.delete_man_unique(unique_id=any_id)
            await call.message.answer(f"{get_text(data['language'], 'message_resend')}")                                                        #type: ignore
            await Man_Woman_State.man_one.set()
        await call.message.delete()
    except Exception as err:
        logging.error(err)


async def second_check_man(call, state):
    data = await db.select_user(telegram_id=call.message.chat.id)
    if call.data == 'user_check_yes':
        await call.message.answer(f"{get_text(data['language'], 'message_enter')}")                                                             #type: ignore
        await Man_Woman_State.man_one.set()
    elif call.data == 'user_check_no':
        await call.message.answer(get_text(data['language'], 'home'),                                                                           #type: ignore
                                  reply_markup=start_menu(get_text(data['language'], 'online_txt'), get_text(data['language'], 'expert_txt'),   #type: ignore
                                                          get_text(data['language'], 'examples_txt'), get_text(data['language'], 'faq_txt'),    #type: ignore
                                                          get_text(data['language'], 'info_txt'), get_text(data['language'], 'contact_txt'),    #type: ignore
                                                          is_reg=is_registered(data), problem_txt=get_text(data['language'], 'problem_txt'),    #type: ignore
                                                          profile_txt=get_text(data['language'], 'profile')))                                   #type: ignore
        #await state.finish()
    await call.message.delete()

@dp.message_handler(BlockedUserFilter(), text=get_values_for_key("problem_txt"), state='*')
async def sos_func1(msg: Message, state: FSMContext):
    data = await db.select_user(telegram_id=msg.from_user.id) 
    await msg.answer(get_text(data['language'], 'message_sending'),                            #type: ignore 
                     reply_markup=create_cancel_button(get_text(data['language'], 'cancel')))  #type: ignore
    await Man_Woman_State.man_one.set()


@dp.message_handler(BlockedUserFilter(), text=get_values_for_key("cancel"), state='*')
async def sos_func(msg: Message):
    data = await db.select_user(telegram_id=msg.from_user.id) 
    if data:
        await msg.answer(get_text(data['language'], 'canceled'),                                                                       #type: ignore
                        reply_markup=start_menu(get_text(data['language'], 'online_txt'), get_text(data['language'], 'expert_txt'),   #type: ignore
                                                get_text(data['language'], 'examples_txt'), get_text(data['language'], 'faq_txt'),    #type: ignore
                                                get_text(data['language'], 'info_txt'), get_text(data['language'], 'contact_txt'),    #type: ignore
                                                is_reg=is_registered(data), problem_txt=get_text(data['language'], 'problem_txt'),    #type: ignore
                                                profile_txt=get_text(data['language'], 'profile')))                                   #type: ignore
    await Man_Woman_State.cancel.set()


@dp.message_handler(BlockedUserFilter(), state=Man_Woman_State.man_woman)
async def sos_manwoman(msg: Message):
    data = await db.select_user(telegram_id=msg.from_user.id)    
    javob = get_text(data['language'], 'message_sending')                                  #type: ignore
    if msg.text in get_values_for_key("offer"):
        await msg.answer(javob)
        await Man_Woman_State.man_one.set()


@dp.message_handler(BlockedUserFilter(), is_media_group=True, content_types=['video', 'photo', 'document', 'voice'],
                    state=Man_Woman_State.man_one)
async def mediagr(msg: Message, album: List[Message], state: FSMContext):
    data = await db.select_user(telegram_id=msg.from_user.id) 
    await msg.answer(f"{get_text(data['language'], 'message_file_arranged')}")            #type: ignore
    #await state.finish()


@dp.message_handler(BlockedUserFilter(), state=Man_Woman_State.man_one, content_types=['audio', 'document', 'photo', 'text', 'video',
                                                                  'voice'])
async def man_bir(msg: Message, state: FSMContext):
    fullname = msg.from_user.full_name
    user_id = int(msg.from_user.id)
    data = await db.select_user(telegram_id=user_id) 
    
    await state.update_data({'user_id': user_id})
    m_one = f"{get_text(data['language'], 'message_accepted_query')}"                    #type: ignore
    
    try:
        if msg.content_type == 'audio':
            await msg.answer_audio(audio=msg.audio.file_id, caption=msg.caption)
            await sdb.add_man_audio(fullname=fullname, user_id=user_id, audio_id=msg.audio.file_id,
                                    unique_id=msg.audio.file_unique_id, caption=msg.caption, turi='audio')
            
            user_audio = await sdb.select_man_audio(user_id=user_id, turi='audio')
            
            for n in user_audio:                                                                          #type: ignore
                if n[1] == msg.audio.file_unique_id:
                    await state.update_data({'audio_unique': n[1]})
            
            await Man_State.man_audio.set()
            await msg.answer(m_one, 
                             reply_markup=create_user_yes_no(get_text(data['language'], 'confirmtxt'),    #type: ignore
                                                             get_text(data['language'], 'reentertxt')))   #type: ignore

        elif msg.content_type == 'document':
            await msg.answer_document(document=msg.document.file_id, caption=msg.caption)
            await sdb.add_man_document(fullname=fullname, user_id=user_id, document_id=msg.document.file_id,
                                       unique_id=msg.document.file_unique_id, caption=msg.caption, turi='document')
            
            user_document = await sdb.select_man_document(user_id=user_id, turi='document')
            
            for n in user_document:                                                                      #type: ignore
                if n[1] == msg.document.file_unique_id:
                    await state.update_data({'document_unique': n[1]})
            
            await Man_State.man_document.set()
            await msg.answer(m_one, 
                             reply_markup=create_user_yes_no(get_text(data['language'], 'confirmtxt'),   #type: ignore
                                                             get_text(data['language'], 'reentertxt')))  #type: ignore

        elif msg.content_type == 'photo':
            await msg.answer_photo(photo=msg.photo[-1].file_id, caption=msg.caption)
            await sdb.add_man_photo(fullname=fullname, user_id=user_id, photo_id=msg.photo[-1].file_id,
                                    unique_id=msg.photo[-1].file_unique_id, caption=msg.caption, turi='photo')
            
            user_photo = await sdb.select_man_photo(user_id=user_id, turi='photo')
            
            for n in user_photo:                                                                         #type: ignore
                if n[1] == msg.photo[-1].file_unique_id:
                    await state.update_data({'photo_unique': n[1]})
            
            await Man_State.man_photo.set()
            await msg.answer(m_one, 
                             reply_markup=create_user_yes_no(get_text(data['language'], 'confirmtxt'),   #type: ignore
                                                             get_text(data['language'], 'reentertxt')))  #type: ignore

        elif msg.content_type == 'text':
            await msg.answer(msg.text)
            await sdb.add_man_text(fullname=fullname, user_id=msg.from_user.id, text=msg.text, turi='text')
            
            user_text = await sdb.select_man_text(user_id=user_id, turi='text')
            
            for n in user_text:                                                                          #type: ignore
                if n[1] == msg.text:
                    await state.update_data({'question_id': n[0]})
            
            await Man_State.man_text.set()
            await msg.answer(m_one, 
                             reply_markup=create_user_yes_no(get_text(data['language'], 'confirmtxt'),   #type: ignore
                                                             get_text(data['language'], 'reentertxt')))  #type: ignore

        elif msg.content_type == 'video':
            await msg.answer_video(video=msg.video.file_id, caption=msg.caption)
            await sdb.add_man_video(fullname=fullname, user_id=user_id, video_id=msg.video.file_id,
                                    unique_id=msg.video.file_unique_id, caption=msg.caption, turi='video')
            
            user_video = await sdb.select_man_video(user_id=user_id, turi='video')
            
            for n in user_video:                                                                         #type: ignore
                if n[1] == msg.video.file_unique_id:
                    await state.update_data({'video_unique': n[1]})
            
                    await Man_State.man_video.set()
            await msg.answer(m_one, 
                             reply_markup=create_user_yes_no(get_text(data['language'], 'confirmtxt'),   #type: ignore
                                                             get_text(data['language'], 'reentertxt')))  #type: ignore

        elif msg.content_type == 'voice':
            await msg.answer_voice(voice=msg.voice.file_id, caption=msg.caption)
            await sdb.add_man_voice(fullname=fullname, user_id=user_id, voice_id=msg.voice.file_id,
                                    unique_id=msg.voice.file_unique_id, caption=msg.caption, turi='voice')
            user_voice = await sdb.select_man_voice(user_id=user_id, turi='voice')
            
            for n in user_voice:                                                                         #type: ignore
                if n[1] == msg.voice.file_unique_id:
                    await state.update_data({'voice_unique': n[1]})
            
                    await Man_State.man_voice.set()
            await msg.answer(m_one, 
                             reply_markup=create_user_yes_no(get_text(data['language'], 'yestxt'),      #type: ignore
                                                             get_text(data['language'], 'notxt')))      #type: ignore
        elif msg.content_type:
            await msg.answer(get_text(data['language'], 'message_file_types'))                          #type: ignore
        await msg.delete()
    except Exception as err:
        logging.error(err)
        await msg.answer(get_text(data['language'], 'something_wrong'))                                 #type: ignore


@dp.callback_query_handler(BlockedUserFilter(), state=Man_State.man_audio)
async def stateaudio_func(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    unique = data['audio_unique']
    await first_check_man(call=call, user_id=data['user_id'], any_id=unique, unique=True)


@dp.callback_query_handler(BlockedUserFilter(), state=Man_State.man_document)
async def statedocumentid_func(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    unique = data['document_unique']
    await first_check_man(call=call, user_id=data['user_id'], any_id=unique, unique=True)


@dp.callback_query_handler(BlockedUserFilter(), state=Man_State.man_photo)
async def statephotoid_func(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    unique = data['photo_unique']
    await first_check_man(call=call, user_id=data['user_id'], any_id=unique, unique=True)


@dp.callback_query_handler(BlockedUserFilter(), state=Man_State.man_text)
async def statesos2_func(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    text = data['question_id']
    await first_check_man(call=call, user_id=data['user_id'], text_id=int(text), m_id=True)


@dp.callback_query_handler(BlockedUserFilter(), state=Man_State.man_video)
async def statevideoid_func(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    unique = data['video_unique']
    await first_check_man(call=call, user_id=data['user_id'], any_id=unique, unique=True)


@dp.callback_query_handler(BlockedUserFilter(), state=Man_State.man_voice)
async def statevoiceid_func(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    unique = data['voice_unique']
    await first_check_man(call=call, user_id=data['user_id'], any_id=unique, unique=True)


@dp.callback_query_handler(BlockedUserFilter(), state=Man_State.user_checkone)
async def check_ikeys_func(call: CallbackQuery, state: FSMContext):
    await second_check_man(call=call, state=state)
