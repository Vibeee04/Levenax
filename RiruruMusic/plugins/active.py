from strings import get_command

from pyrogram import filters
from pyrogram.types import Message

from RiruruMusic import app
from RiruruMusic.misc import SUDOERS
from RiruruMusic.utils.decorators import language
from RiruruMusic.utils.database.memorydatabase import get_active_chats, get_active_video_chats

# Commands
FAST_AC = get_command("FAST_AC")
ACTIVEVC_COMMAND = get_command("ACTIVEVC_COMMAND")
ACTIVEVIDEO_COMMAND = get_command("ACTIVEVIDEO_COMMAND")


@app.on_message(filters.command(ACTIVEVC_COMMAND) & SUDOERS)
@language
async def activevc(client, message: Message, _):
    mystic = await message.reply_text(_["active_2"])
    served_chats = await get_active_chats()
    text = ""
    j = 0
    for x in served_chats:
        j += 1
        try:
            chat = await app.get_chat(x)
            if chat.username:
                text += f"<b>{j}.</b> [{chat.title}](https://t.me/{chat.username})[`{x}`]\n"
            else:
                text += f"<b>{j}. [{chat.title}]</b> [`{x}`]\n"
        except Exception:
            text += f"<b>{j}. {_['S_B_6']}</b> [`{x}`]\n"
    if text:
        await mystic.edit_text(_["active_4"].format(text), disable_web_page_preview=True)
    else:
        await mystic.edit_text(_["active_6"])


@app.on_message(filters.command(ACTIVEVIDEO_COMMAND) & SUDOERS)
@language
async def activevi_(client, message: Message, _):
    mystic = await message.reply_text(_["active_3"])
    served_chats = await get_active_video_chats()
    text = ""
    j = 0
    for x in served_chats:
        j += 1
        try:
            chat = await app.get_chat(x)
            if chat.username:
                text += f"<b>{j}.</b> [{chat.title}](https://t.me/{chat.username})[`{x}`]\n"
            else:
                text += f"<b>{j}. [{chat.title}]</b> [`{x}`]\n"
        except Exception:
            text += f"<b>{j}. {_['S_B_6']}</b> [`{x}`]\n"
    if text:
        await mystic.edit_text(_["active_5"].format(text), disable_web_page_preview=True)
    else:
        await mystic.edit_text(_["active_7"])


@app.on_message(filters.command(FAST_AC) & SUDOERS)
@language
async def littleac(client, message: Message, _):
    ac_audio = str(len(await get_active_chats()))
    ac_video = str(len(await get_active_video_chats()))
    await message.reply_text(_["active_1"].format(ac_audio, ac_video), quote=True)
