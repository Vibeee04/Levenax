import asyncio

from datetime import datetime, timedelta

from config import adminlist, chatstats, clean, userstats, LOG_GROUP_ID, CLEANMODE_DELETE_MINS

from pyrogram.errors import FloodWait
from pyrogram.enums import ChatMembersFilter
from pyrogram.raw.types import UpdateReadChannelOutbox

from RiruruMusic import app
from RiruruMusic.utils.database import (
    get_active_chats, get_authuser_names, get_particular_top, get_user_top,
    is_cleanmode_on, set_queries, update_particular_top, update_user_top
)
from RiruruMusic.utils.formatters import alpha_to_int
from RiruruMusic.plugins.broadcast import is_broadcasting


AUTO_SLEEP = 5

cleanmode_group = 15


@app.on_raw_update(group=cleanmode_group)
async def clean_mode(client, update, users, chats):
    if is_broadcasting():
        return
    try:
        if not isinstance(update, UpdateReadChannelOutbox):
            return
    except:
        return
    if users or chats:
        return
    message_id = update.max_id
    chat_id = int(f"-100{update.channel_id}")
    if not await is_cleanmode_on(chat_id):
        return
    if chat_id not in clean:
        clean[chat_id] = []
    time_now = datetime.now()
    put = {
        "msg_id": message_id,
        "timer_after": time_now + timedelta(minutes=CLEANMODE_DELETE_MINS),
    }
    clean[chat_id].append(put)
    await set_queries(1)


async def auto_clean():
    while not await asyncio.sleep(AUTO_SLEEP):
        try:
            for chat_id in chatstats:
                for dic in chatstats[chat_id]:
                    vidid = dic["vidid"]
                    title = dic["title"]
                    chatstats[chat_id].pop(0)
                    spot = await get_particular_top(chat_id, vidid)
                    if spot:
                        spot = spot["spot"]
                        next_spot = spot + 1
                        new_spot = {"spot": next_spot, "title": title}
                        await update_particular_top(chat_id, vidid, new_spot)
                    else:
                        next_spot = 1
                        new_spot = {"spot": next_spot, "title": title}
                        await update_particular_top(chat_id, vidid, new_spot)

            for user_id in userstats:
                for dic in userstats[user_id]:
                    vidid = dic["vidid"]
                    title = dic["title"]
                    userstats[user_id].pop(0)
                    spot = await get_user_top(user_id, vidid)
                    if spot:
                        spot = spot["spot"]
                        next_spot = spot + 1
                        new_spot = {"spot": next_spot, "title": title}
                        await update_user_top(user_id, vidid, new_spot)
                    else:
                        next_spot = 1
                        new_spot = {"spot": next_spot, "title": title}
                        await update_user_top(user_id, vidid, new_spot)
        except:
            continue

        try:
            for chat_id in clean:
                if chat_id == LOG_GROUP_ID:
                    continue
                for x in clean[chat_id]:
                    if datetime.now() > x["timer_after"]:
                        try:
                            await app.delete_messages(chat_id, x["msg_id"])
                        except FloodWait as e:
                            await asyncio.sleep(e.value)
                        except:
                            continue
                    else:
                        continue
        except:
            continue
        try:
            served_chats = await get_active_chats()
            for chat_id in served_chats:
                if chat_id not in adminlist:
                    adminlist[chat_id] = []
                    async for user in app.get_chat_members(chat_id, filter=ChatMembersFilter.ADMINISTRATORS):
                        if user.privileges.can_manage_video_chats:
                            adminlist[chat_id].append(user.user.id)
                    authusers = await get_authuser_names(chat_id)
                    for user in authusers:
                        user_id = await alpha_to_int(user)
                        adminlist[chat_id].append(user_id)
        except:
            continue


asyncio.create_task(auto_clean())
