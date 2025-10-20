from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


class AdminFilter(BoundFilter):
    async def check(self, message: types.Message):
        member = await message.chat.get_member(message.from_user.id)
        return member.is_chat_admin()


class TextReply(BoundFilter):
    key = "text_reply"

    async def check(self, message: types.Message):
        message = message.reply_to_message
        if message.content_type == 'text':
            return True


class PhotoReply(BoundFilter):
    key = "photo_reply"

    async def check(self, message: types.Message):
        message = message.reply_to_message
        if message.content_type == 'photo':
            return True


class VoiceReply(BoundFilter):
    key = "voice_reply"

    async def check(self, message: types.Message):
        message = message.reply_to_message
        if message.content_type == 'voice':
            return True


class VideoReply(BoundFilter):
    key = "video_reply"

    async def check(self, message: types.Message):
        message = message.reply_to_message
        if message.content_type == 'video':
            return True


class AudioReply(BoundFilter):
    key = "audio_reply"

    async def check(self, message: types.Message):
        message = message.reply_to_message
        if message.content_type == 'audio':
            return True
