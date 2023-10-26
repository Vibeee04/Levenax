from strings import get_command
from config import YTDOWNLOADER

from pyrogram import filters
from pyrogram.types import Message

from RiruruMusic import app
from RiruruMusic.misc import SUDOERS
from RiruruMusic.utils.database import add_off, add_on
from RiruruMusic.utils.decorators.language import language

VIDEOMODE_COMMAND = get_command("VIDEOMODE_COMMAND")


@app.on_message(filters.command(VIDEOMODE_COMMAND) & SUDOERS)
@language
async def videoloaymode(client, message: Message, _):
    usage = _["vidmode_1"]
    if len(message.command) != 2:
        return await message.reply_text(usage)
    state = message.text.split(None, 1)[1].strip()
    state = state.lower()
    if state == "download":
        await add_on(YTDOWNLOADER)
        await message.reply_text(_["vidmode_2"])
    elif state == "m3u8":
        await add_off(YTDOWNLOADER)
        await message.reply_text(_["vidmode_3"])
    else:
        await message.reply_text(usage)
