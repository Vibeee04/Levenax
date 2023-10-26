import config
import psutil
import asyncio
import platform

from config import BANNED_USERS
from strings import get_command

from sys import version as pyver
from pytgcalls.__version__ import __version__ as pytgver

from pyrogram import filters, __version__ as pyrover
from pyrogram.types import CallbackQuery, Message

from RiruruMusic import app
from RiruruMusic.plugins import ALL_MODULES
from RiruruMusic.misc import SUDOERS, pymongodb
from RiruruMusic.core.userbot import assistants
from RiruruMusic.utils.decorators.language import language, languageCB
from RiruruMusic.utils.inline.stats import (
    back_stats_buttons, back_stats_markup, get_stats_markup, stats_buttons, top_ten_stats_markup
)
from RiruruMusic.utils.database import (
    get_global_tops, get_particulars, get_queries, get_served_chats,
    get_served_users, get_sudoers, get_top_chats, get_topp_users, chattopdb
)


loop = asyncio.get_running_loop()

# Commands
STATS_COMMAND = get_command("STATS_COMMAND")
GSTATS_COMMAND = get_command("GSTATS_COMMAND")


@app.on_message(filters.command(STATS_COMMAND) & SUDOERS)
@language
async def stats_global(client, message: Message, _):
    upl = stats_buttons(_)
    await message.reply_photo(
        photo=config.STATS_IMG_URL,
        caption=_["gstats_8"].format(app.mention),
        reply_markup=upl,
    )


@app.on_message(filters.command(GSTATS_COMMAND) & filters.group & ~BANNED_USERS)
@language
async def gstats_global(client, message: Message, _):
    stats = chattopdb.count_documents({})
    if stats == 0:
        return await message.reply_text(_["gstats_2"])
    upl = get_stats_markup(_)
    await message.reply_photo(config.STATS_IMG_URL, caption=_["gstats_9"].format(app.mention), reply_markup=upl)


@app.on_callback_query(filters.regex("GetStatsNow") & ~BANNED_USERS)
@languageCB
async def top_users_ten(client, CallbackQuery: CallbackQuery, _):
    chat_id = CallbackQuery.message.chat.id
    callback_data = CallbackQuery.data.strip()
    what = callback_data.split(None, 1)[1]
    upl = back_stats_markup(_)
    try:
        await CallbackQuery.answer()
    except:
        pass
    mystic = await CallbackQuery.edit_message_text(
        _["gstats_3"].format(
            f"of {CallbackQuery.message.chat.title}" if what == "Here" else what
        )
    )
    if what == "Tracks":
        stats = await get_global_tops()
    elif what == "Chats":
        stats = await get_top_chats()
    elif what == "Users":
        stats = await get_topp_users()
    elif what == "Here":
        stats = await get_particulars(chat_id)
    if not stats:
        await asyncio.sleep(1)
        return await mystic.edit_text(_["gstats_2"], reply_markup=upl)
    queries = await get_queries()

    def get_stats():
        results = {}
        for i in stats:
            top_list = (
                stats[i]
                if what in ["Chats", "Users"]
                else stats[i]["spot"]
            )
            results[str(i)] = top_list
            list_arranged = dict(
                sorted(
                    results.items(),
                    key=lambda item: item[1],
                    reverse=True,
                )
            )
        if not results:
            return mystic.edit_text(_["gstats_2"], reply_markup=upl)
        msg = ""
        limit = 0
        total_count = 0
        if what in ["Tracks", "Here"]:
            for items, count in list_arranged.items():
                total_count += count
                if limit == 10:
                    continue
                limit += 1
                details = stats.get(items)
                title = (details["title"][:35]).title()
                if items == "telegram":
                    msg += f"🍒 [ᴛᴇʟᴇɢʀᴀᴍ ᴍᴇᴅɪᴀ](https://t.me/AltronChats) ** ᴩʟᴀʏᴇᴅ {count} ᴛɪᴍᴇs**\n\n"
                else:
                    msg += f"📌 [{title}](https://www.youtube.com/watch?v={items}) ** ᴩʟᴀʏᴇᴅ {count} ᴛɪᴍᴇs**\n\n"

            temp = (
                _["gstats_4"].format(queries, app.mention, len(stats), total_count, limit)
                if what == "Tracks"
                else _["gstats_7"].format(len(stats), total_count, limit)
            )
            msg = temp + msg
        return msg, list_arranged

    try:
        msg, list_arranged = await loop.run_in_executor(None, get_stats)
    except Exception as e:
        print(e)
        return
    limit = 0
    if what in ["Users", "Chats"]:
        for items, count in list_arranged.items():
            if limit == 10:
                break
            try:
                extract = (
                    (await app.get_users(items)).first_name
                    if what == "Users"
                    else (await app.get_chat(items)).title
                )
                if extract is None:
                    continue
                await asyncio.sleep(0.5)
            except:
                continue
            limit += 1
            msg += f"💖 `{extract}` ᴩʟᴀʏᴇᴅ {count} ᴛɪᴍᴇs ᴏɴ ʙᴏᴛ.\n\n"
        temp = (
            _["gstats_5"].format(limit, app.mention)
            if what == "Chats"
            else _["gstats_6"].format(limit, app.mention)
        )
        msg = temp + msg

    try:
        await CallbackQuery.edit_message_caption(msg, reply_markup=upl)
    except:
        await CallbackQuery.message.reply_photo(photo=config.STATS_IMG_URL, caption=msg, reply_markup=upl)


@app.on_callback_query(filters.regex("TopOverall") & ~BANNED_USERS)
@languageCB
async def overall_stats(client, CallbackQuery: CallbackQuery, _):
    if CallbackQuery.from_user.id not in SUDOERS:
        return await CallbackQuery.answer("Only for Sudo Users.", show_alert=True)

    upl = back_stats_buttons(_)
    try:
        await CallbackQuery.answer()
    except:
        pass
    await CallbackQuery.edit_message_text(_["gstats_1"])
    served_chats = len(await get_served_chats())
    served_users = len(await get_served_users())
    total_queries = await get_queries()
    blocked = len(BANNED_USERS)
    sudoers = len(SUDOERS)
    mod = len(ALL_MODULES)
    assistant = len(assistants)
    playlist_limit = config.SERVER_PLAYLIST_LIMIT
    fetch_playlist = config.PLAYLIST_FETCH_LIMIT
    song = config.SONG_DOWNLOAD_DURATION
    play_duration = config.DURATION_LIMIT_MIN
    if config.AUTO_LEAVING_ASSISTANT == str(True):
        ass = "ʏᴇs"
    else:
        ass = "ɴᴏ"
    cm = config.CLEANMODE_DELETE_MINS
    text = f"""**<u>ʙᴏᴛ's sᴛᴀᴛs ᴀɴᴅ ɪɴғᴏ:</u>**

**ᴍᴏᴅᴜʟᴇs:** {mod}
**ᴄʜᴀᴛs:** {served_chats} 
**ᴜsᴇʀs:** {served_users} 
**ʙʟᴏᴄᴋᴇᴅ:** {blocked} 
**sᴜᴅᴏᴇʀs:** {sudoers} 
    
**ǫᴜᴇʀɪᴇs:** {total_queries} 
**ᴀssɪsᴛᴀɴᴛs:** {assistant}
**ᴀss ᴀᴜᴛᴏ ʟᴇᴀᴠᴇ:** {ass}
**ᴄʟᴇᴀɴᴍᴏᴅᴇ:** {cm} ᴍɪɴᴜᴛᴇs

**ᴅᴜʀᴀᴛɪᴏɴ ʟɪᴍɪᴛ:** {play_duration} ᴍɪɴᴜᴛᴇs
**ᴅᴏᴡɴʟᴏᴀᴅ ʟɪᴍɪᴛ:** {song} ᴍɪɴᴜᴛᴇs
**ᴩʟᴀʏʟɪsᴛ ʟɪᴍɪᴛ:** {playlist_limit}
**ᴩʟᴀʏʟɪsᴛ ᴩʟᴀʏ ʟɪᴍɪᴛ:** {fetch_playlist}"""
    try:
        await CallbackQuery.edit_message_caption(text, reply_markup=upl)
    except:
        await CallbackQuery.message.reply_photo(photo=config.STATS_IMG_URL, caption=text, reply_markup=upl)


@app.on_callback_query(filters.regex("bot_stats_sudo"))
@languageCB
async def overall_stats(client, CallbackQuery: CallbackQuery, _):
    if CallbackQuery.from_user.id not in SUDOERS:
        return await CallbackQuery.answer("Only for Sudo Users.", show_alert=True)

    upl = back_stats_buttons(_)
    try:
        await CallbackQuery.answer()
    except:
        pass
    await CallbackQuery.edit_message_text(_["gstats_1"])
    sc = platform.system()
    p_core = psutil.cpu_count(logical=False)
    t_core = psutil.cpu_count(logical=True)
    ram = (
        str(round(psutil.virtual_memory().total / (1024.0**3)))
        + " ɢʙ"
    )
    try:
        cpu_freq = psutil.cpu_freq().current
        if cpu_freq >= 1000:
            cpu_freq = f"{round(cpu_freq / 1000, 2)}ɢʜᴢ"
        else:
            cpu_freq = f"{round(cpu_freq, 2)}ᴍʜᴢ"
    except:
        cpu_freq = "Unable to Fetch"
    hdd = psutil.disk_usage("/")
    total = hdd.total / (1024.0**3)
    total = str(total)
    used = hdd.used / (1024.0**3)
    used = str(used)
    free = hdd.free / (1024.0**3)
    free = str(free)
    mod = len(ALL_MODULES)

    try:
        call = pymongodb.command("dbstats")
    except:
        await CallbackQuery.message.reply_text(_["error_2"])
        await CallbackQuery.message.delete()
        return

    datasize = call["dataSize"] / 1024
    datasize = str(datasize)
    storage = call["storageSize"] / 1024
    objects = call["objects"]
    collections = call["collections"]
    served_chats = len(await get_served_chats())
    served_users = len(await get_served_users())
    total_queries = await get_queries()
    blocked = len(BANNED_USERS)
    sudoers = len(await get_sudoers())
    text = f"""<u><b>ʙᴏᴛ's sᴛᴀᴛs ᴀɴᴅ ɪɴғᴏ:</b></u>

       <u><b>ʜᴀʀᴅᴡᴀʀᴇ</b></u>
**ᴍᴏᴅᴜʟᴇs:** {mod}
**ᴩʟᴀᴛғᴏʀᴍ:** {sc}
**ʀᴀᴍ:** {ram}
**ᴩʜʏsɪᴄᴀʟ ᴄᴏʀᴇs:** {p_core}
**ᴛᴏᴛᴀʟ ᴄᴏʀᴇs:** {t_core}
**ᴄᴩᴜ ғʀᴇǫᴜᴇɴᴄʏ:** {cpu_freq}

       <u><b>sᴏғᴛᴡᴀʀᴇ</b></u>
**ᴩʏᴛʜᴏɴ :** {pyver.split()[0]}
**ᴩʏʀᴏɢʀᴀᴍ :** {pyrover}
**ᴩʏ-ᴛɢᴄᴀʟʟs :** {pytgver}

        <u><b>sᴛᴏʀᴀɢᴇ</b></u>
**ᴀᴠᴀɪʟᴀʙʟᴇ:** {total[:4]} GiB
**ᴜsᴇᴅ:** {used[:4]} GiB
**ғʀᴇᴇ:** {free[:4]} GiB
        
      <u><b>ᴄᴜʀʀᴇɴᴛ sᴛᴀᴛs</b></u>
**ᴄʜᴀᴛs:** {served_chats} 
**ᴜsᴇʀs:** {served_users} 
**ʙʟᴏᴄᴋᴇᴅ:** {blocked} 
**sᴜᴅᴏᴇʀs:** {sudoers} 

      <u><b>ᴍᴏɴɢᴏ ᴅᴀᴛᴀʙᴀsᴇ</b></u>
**sɪᴢᴇ:** {datasize[:6]} Mb
**sᴛᴏʀᴀɢᴇ:** {storage} Mb
**ᴄᴏʟʟᴇᴄᴛɪᴏɴs:** {collections}
**ᴋᴇʏs:** {objects}
**ʙᴏᴛ ǫᴜᴇʀɪᴇs:** `{total_queries}`"""

    try:
        await CallbackQuery.edit_message_caption(text, reply_markup=upl)
    except:
        await CallbackQuery.message.reply_photo(photo=config.STATS_IMG_URL, caption=text, reply_markup=upl)


@app.on_callback_query(
    filters.regex(pattern=r"^(TOPMARKUPGET|GETSTATS|GlobalStats)$")
    & ~BANNED_USERS
)
@languageCB
async def back_buttons(client, CallbackQuery: CallbackQuery, _):
    try:
        await CallbackQuery.answer()
    except:
        pass

    command = CallbackQuery.matches[0].group(1)
    if command == "TOPMARKUPGET":
        upl = top_ten_stats_markup(_)
        try:
            await CallbackQuery.edit_message_caption(_["gstats_10"], reply_markup=upl)
        except:
            await CallbackQuery.message.reply_photo(
                photo=config.STATS_IMG_URL, caption=_["gstats_10"], reply_markup=upl,
            )

    elif command == "GlobalStats":
        upl = get_stats_markup(_)
        try:
            await CallbackQuery.edit_message_caption(_["gstats_9"].format(app.mention), reply_markup=upl)
        except:
            await CallbackQuery.message.reply_photo(config.STATS_IMG_URL, caption=_["gstats_9"].format(app.mention), reply_markup=upl)

    elif command == "GETSTATS":
        upl = stats_buttons(_)
        try:
            await CallbackQuery.edit_message_caption(_["gstats_8"].format(app.mention), reply_markup=upl)
        except:
            await CallbackQuery.message.reply_photo(
                photo=config.STATS_IMG_URL,
                caption=_["gstats_8"].format(app.mention),
                reply_markup=upl,
            )
