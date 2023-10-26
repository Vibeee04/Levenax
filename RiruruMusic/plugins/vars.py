import config
import asyncio

from pyrogram import filters
from strings import get_command

from RiruruMusic import app
from RiruruMusic.misc import SUDOERS
from RiruruMusic.utils.formatters import convert_bytes
from RiruruMusic.utils.database.memorydatabase import get_video_limit

VARS_COMMAND = get_command("VARS_COMMAND")


@app.on_message(filters.command(VARS_COMMAND) & SUDOERS)
async def varsFunc(client, message):
    mystic = await message.reply_text("ᴩʟᴇᴀsᴇ ᴡᴀɪᴛ... ɢᴇᴛᴛɪɴɢ ʏᴏᴜʀ ᴄᴏɴғɪɢ ᴠᴀʀɪᴀʙʟᴇs...")
    v_limit = await get_video_limit()
    up_r = f"[ʀᴇᴩᴏ]({config.UPSTREAM_REPO})"
    up_b = config.UPSTREAM_BRANCH
    auto_leave = config.AUTO_LEAVE_ASSISTANT_TIME
    yt_sleep = config.YOUTUBE_DOWNLOAD_EDIT_SLEEP
    tg_sleep = config.TELEGRAM_DOWNLOAD_EDIT_SLEEP
    playlist_limit = config.SERVER_PLAYLIST_LIMIT
    fetch_playlist = config.PLAYLIST_FETCH_LIMIT
    song = config.SONG_DOWNLOAD_DURATION
    play_duration = config.DURATION_LIMIT_MIN
    cm = config.CLEANMODE_DELETE_MINS

    if config.AUTO_LEAVING_ASSISTANT == str(True):
        ass = "ʏᴇs"
    else:
        ass = "ɴᴏ"
    if config.AUTO_DOWNLOADS_CLEAR == str(True):
        down = "ʏᴇs"
    else:
        down = "ɴᴏ"
    if config.START_IMG_URL:
        start = f"[ɪᴍᴀɢᴇ]({config.START_IMG_URL})"
    else:
        start = "ɴᴏ"
    if config.SUPPORT_GROUP:
        s_g = f"[sᴜᴩᴩᴏʀᴛ](https://t.me/{config.SUPPORT_GROUP})"
    else:
        s_g = "ɴᴏ"
    if config.GIT_TOKEN:
        token = "ʏᴇs"
    else:
        token = "ɴᴏ"
    if config.SPOTIFY_CLIENT_ID and config.SPOTIFY_CLIENT_SECRET:
        sotify = "ʏᴇs"
    else:
        sotify = "ɴᴏ"
    tg_aud = convert_bytes(config.TG_AUDIO_FILESIZE_LIMIT)
    tg_vid = convert_bytes(config.TG_VIDEO_FILESIZE_LIMIT)
    text = f"""**ᴍᴜsɪᴄ ʙᴏᴛ ᴄᴏɴғɪɢ ᴠᴀʀɪᴀʙʟᴇs:**

**<u>ʙᴀsɪᴄ ᴠᴀʀɪᴀʙʟᴇs:</u>**
**ᴅᴜʀᴀᴛɪᴏɴ_ʟɪᴍɪᴛ** : `{play_duration} ᴍɪɴᴜᴛᴇs`
**sᴏɴɢ_ᴅᴏᴡɴʟᴏᴀᴅ_ᴅᴜʀᴀᴛɪᴏɴ_ʟɪᴍɪᴛ** :` {song} ᴍɪɴᴜᴛᴇs`
**ᴏᴡɴᴇʀ_ɪᴅ** : `{config.OWNER_ID}`
    
**<u>ʀᴇᴩᴏsɪᴛᴏʀʏ ᴠᴀʀɪᴀʙʟᴇs:</u>**
**ᴜᴩsᴛʀᴇᴀᴍ_ʀᴇᴩᴏ** : {up_r}
**ᴜᴩsᴛʀᴇᴀᴍ_ʙʀᴀɴᴄʜ** : `{up_b}`
**ɢɪᴛʜᴜʙ_ʀᴇᴩᴏ** : {up_r}
**ɢɪᴛ_ᴛᴏᴋᴇɴ**: `{token}`


**<u>ʙᴏᴛ ᴠᴀʀɪᴀʙʟᴇs:</u>**
**ᴀᴜᴛᴏ_ʟᴇᴀᴠɪɴɢ_ᴀssɪsᴛᴀɴᴛ** : `{ass}`
**ᴀssɪsᴛᴀɴᴛ_ʟᴇᴀᴠᴇ_ᴛɪᴍᴇ** : `{auto_leave} sᴇᴄᴏɴᴅs`
**ᴀᴜᴛᴏ_ᴅᴏᴡɴʟᴏᴀᴅs_ᴄʟᴇᴀʀ** : `{down}`
**ʏᴏᴜᴛᴜʙᴇ_ᴇᴅɪᴛ_sʟᴇᴇᴩ** : `{yt_sleep} sᴇᴄᴏɴᴅs`
**ᴛᴇʟᴇɢʀᴀᴍ_ᴇᴅɪᴛ_sʟᴇᴇᴩ** :` {tg_sleep} sᴇᴄᴏɴᴅs`
**ᴄʟᴇᴀɴᴍᴏᴅᴇ_ᴍɪɴs** : `{cm} ᴍɪɴᴜᴛᴇs`
**ᴠɪᴅᴇᴏ_sᴛʀᴇᴀᴍ_ʟɪᴍɪᴛ** : `{v_limit} ᴄʜᴀᴛs`
**sᴇʀᴠᴇʀ_ᴩʟᴀʏʟɪsᴛ_ʟɪᴍɪᴛ** :` {playlist_limit}`
**ᴩʟᴀʏʟɪsᴛ_ғᴇᴛᴄʜ_ʟɪᴍɪᴛ** :` {fetch_playlist}`

**<u>sᴩᴏᴛɪғʏ ᴠᴀʀɪᴀʙʟᴇs:</u>**
**sᴩᴏᴛɪғʏ_ᴄʟɪᴇɴᴛ_ɪᴅ** :` {sotify}`
**sᴩᴏᴛɪғʏ_ᴄʟɪᴇɴᴛ_sᴇᴄʀᴇᴛ** : `{sotify}`

**<u>ᴘʟᴀʏꜱɪᴢᴇ ᴠᴀʀꜱ:</u>**
**ᴛɢ_ᴀᴜᴅɪᴏ_ғʟɪᴇsɪᴢᴇ_ʟɪᴍɪᴛ** :` {tg_aud}`
**ᴛɢ_ᴠɪᴅᴇᴏ_ғɪʟᴇsɪᴢᴇ_ʟɪᴍɪᴛ** :` {tg_vid}`

**<u>ᴇxᴛʀᴀ ᴠᴀʀɪᴀʙʟᴇs:</u>**
**ᴜᴘᴅᴀᴛᴇꜱ_ᴄʜᴀɴɴᴇʟ** :  [ᴄʜᴀɴɴᴇʟ](https://t.me/TheAltron)
**sᴜᴩᴩᴏʀᴛ_ɢʀᴏᴜᴩ** :  {s_g}
**sᴛᴀʀᴛ_ɪᴍɢ_ᴜʀʟ** :  {start}"""
    await asyncio.sleep(1)
    await mystic.edit_text(text, disable_web_page_preview=True)
