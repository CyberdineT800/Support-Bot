import asyncio
from typing import List, Union

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from data.translation import get_text

from loader import dp, bot


def is_contact(contact):
    if contact.startswith('+'):
        contact = contact[1:]
    if contact.startswith('998'):
        contact = contact[3:]
    if len(contact)!=9:
        return False
    try:
        contact = int(contact)
        return True
    except:
        return False

def is_registered(datas):
    if datas and \
       datas.get('name', 'none') != 'none' and \
       datas.get('region', 'none') != 'none' and \
       datas.get('city', 'none') != 'none' and \
       datas.get('phone', 'none') != 'none':
        return True
    return False


def create_personal_infos(selected_language, datas):
    res = f"<blockquote>{get_text(selected_language, 'information')}</blockquote>\n\n"
    res +=  f"|- {get_text(selected_language, 'fullname_info')}: {datas['name']}\n"
    res +=  f"|- {get_text(selected_language, 'region_info')}: {datas['region']}\n"
    res +=  f"|- {get_text(selected_language, 'city_info')}: {datas['city']}\n"
    res +=  f"|- {get_text(selected_language, 'contact_info')}: {datas['phone']}\n"
    
    if datas['username'] != 'none':
        res +=  f"|- {get_text(selected_language, 'username')}: @{datas['username']}\n"
    
    return res


class AlbumMiddleware(BaseMiddleware):
    """This middleware is for capturing media groups."""

    album_data: dict = {}

    def __init__(self, latency: Union[int, float] = 0.01):
        """
        You can provide custom latency to make sure
        albums are handled properly in highload.
        """
        self.latency = latency
        super().__init__()

    async def on_process_message(self, message: types.Message, data: dict):
        if not message.media_group_id:
            return

        try:
            self.album_data[message.media_group_id].append(message)
            raise CancelHandler()  # Tell aiogram to cancel handler for this group element
        except KeyError:
            self.album_data[message.media_group_id] = [message]
            await asyncio.sleep(self.latency)

            message.conf["is_last"] = True
            data["album"] = self.album_data[message.media_group_id]

    async def on_post_process_message(self, message: types.Message, result: dict, data: dict):
        """Clean up after handling our album."""
        if message.media_group_id and message.conf.get("is_last"):
            del self.album_data[message.media_group_id]


# @dp.message_handler(is_media_group=True, content_types=types.ContentType.PHOTO)
# async def handle_albums(message: types.Message, album: List[types.Message]):
#     """This handler will receive a complete album of any type."""
#     media_group = types.MediaGroup()
#     for obj in album:
#         if obj.photo:
#             file_id = obj.photo[-1].file_id
#         else:
#             file_id = obj[obj.content_type].file_id
#
#         try:
#             # We can also add a caption to each file by specifying `"caption": "text"`
#             media_group.attach({"media": file_id, "type": obj.content_type, "caption" : obj.caption})
#         except ValueError:
#             return await message.answer("This type of album is not supported by aiogram.")
#
#     await message.answer_media_group(media_group)
#
