# © @xMiHiR & @MR_RAICHU

import os

from asyncio import sleep
from traceback import format_exc

from strings import get_command
from config import LOG_GROUP_ID, OWNER_ID

from pyrogram import filters
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import UserDeactivated, UserNotParticipant, FloodWait
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from RiruruMusic import app
from RiruruMusic.misc import SUDOERS
from RiruruMusic.utils.decorators.language import language
from RiruruMusic.utils.database import get_served_chats, get_client


# Commands
FC_COMMAND = get_command("FC_COMMAND")
LINK_COMMAND = get_command("LINK_COMMAND")
CHECK_COMMAND = get_command("CHECK_COMMAND")
TRACK_COMMAND = get_command("TRACK_COMMAND")


# Check Every Userbots & Bot
@app.on_message(filters.command(CHECK_COMMAND) & SUDOERS & ~filters.forwarded)
@language
async def systest(client, message: Message, _):
    mys = await message.reply_text(_["extra_1"])
    await app.send_message(LOG_GROUP_ID, _["extra_2"])

    from RiruruMusic.core.userbot import assistants

    suspendedacc = []
    for num in assistants:
        ass = await get_client(num)
        try:
            await ass.send_message(LOG_GROUP_ID, _["extra_3"].format(num))
        except UserDeactivated:
            suspendedacc.append(f"Assistant {num}")

    await sleep(1)
    mtext = _["extra_4"].format(assistants[-1], len(suspendedacc))
    if len(suspendedacc) > 0:
        mtext += _["extra_5"].format(", ".join(suspendedacc))
    await mys.edit_text(mtext)


# Logs, Temps Etc Cleaner Without Restarting Bot
@app.on_message(filters.command(FC_COMMAND) & SUDOERS & ~filters.forwarded)
async def clearLogs(_, message: Message):
    try:
        os.system('rm -rf cache')
        os.system('rm AltLogs.txt')
        os.system('mkdir cache')
        for i in range(11):
            if os.path.exists(f"AltLogs.txt.{i}"):
                os.system(f'rm AltLogs.txt.{i}')
        await message.reply_text(f"**Deleted Below Folders & Files:**\n - Cache\n - Logs", quote=True)
    except:
        await message.reply_text(f"**Failed To Delete Some Files !!**\n\nPlease Read:\n`{format_exc()}`", quote=True)


#Link Creater
@app.on_message(filters.command(LINK_COMMAND) & filters.user(OWNER_ID) & ~filters.forwarded)
async def new_link_getter(client, message: Message):
    try:
        chat_id = int(message.text.split(" ", maxsplit=1)[1])
    except:
        await message.reply_text("**Usage:** /link [ᴄʜᴀᴛ-ɪᴅ]")
        return

    try:
        chat = await app.get_chat(chat_id)
        if chat.username:
            link = f"https://t.me/{chat.username}"
        elif chat.invite_link:
            link = chat.invite_link
        else:
            raise Exception
        btn = InlineKeyboardMarkup([[InlineKeyboardButton("• ᴄʜᴀᴛ ʟɪɴᴋ •", url=link)]])
        await message.reply_text("🔗 **ᴄʜᴀᴛ-ʟɪɴᴋ ᴇxᴘᴏʀᴛᴇᴅ.**", quote=True, reply_markup=btn)
    except:
        try:
            link = await app.export_chat_invite_link(chat_id)
            btn = InlineKeyboardMarkup([[InlineKeyboardButton("• ᴄʜᴀᴛ ʟɪɴᴋ •", url=link)]])
            await message.reply_text("🔗 **ᴄʜᴀᴛ-ʟɪɴᴋ ᴇxᴘᴏʀᴛᴇᴅ.**", quote=True, reply_markup=btn)
        except:
            try:
                link = await app.create_chat_invite_link(chat_id)
                btn = InlineKeyboardMarkup([[InlineKeyboardButton("• ᴄʜᴀᴛ ʟɪɴᴋ •", url=link)]])
                await message.reply_text("🔗 **ᴄʜᴀᴛ-ʟɪɴᴋ ᴄʀᴇᴀᴛᴇᴅ.**", quote=True, reply_markup=btn)
            except:
                await message.reply_text("⚠ **ERROR:** ᴍᴀʏʙᴇ ʙᴏᴛ ʜᴀᴠᴇ ɴᴏᴛ ᴘᴇʀᴍɪꜱꜱɪᴏɴ ᴏꜰ **ɪɴᴠɪᴛᴇ ᴜꜱᴇʀꜱ ᴠɪᴀ ʟɪɴᴋ** ᴏʀ ʙᴏᴛ ʀᴇᴍᴏᴠᴇᴅ!", quote=True)


@app.on_message(filters.command(TRACK_COMMAND) & filters.user(OWNER_ID) & ~filters.forwarded)
@language
async def tracking_user(client, message: Message, _):
    if message.reply_to_message:
        userx = message.reply_to_message.from_user.id
    else:
        try:
            userx = message.text.split(" ", maxsplit=2)[1]
        except:
            await message.reply_text("**Usage:**\n/track [ᴜsᴇʀ_ɪᴅ | ʀᴇᴘʟʏ_ᴛᴏ_ᴜsᴇʀ]")
            return

    replyreport = await message.reply_text("🏷 **ᴛʀʏɪɴɢ ᴛᴏ ᴠᴀʟɪᴅᴀᴛᴇ ᴛʜᴇ ᴜꜱᴇʀ...**")
    await sleep(1)
    try:
        await app.resolve_peer(userx)
        validated_user = await app.get_users(userx)
    except:
        return await replyreport.edit_text("❌ **ʙᴏᴛ ɴᴇᴠᴇʀ ᴍᴇᴛ ᴛʜɪꜱ ᴜꜱᴇʀ!**\n\nᴘʟᴇᴀꜱᴇ ꜰᴏʀᴄᴇ ᴛʜᴀᴛ ᴜꜱᴇʀ ᴛᴏ ꜱᴛᴀʀᴛ ʏᴏᴜʀ ʙᴏᴛ ᴇᴠᴇɴ ɪꜰ ʙᴏᴛ ɪꜱ ɴᴏᴛ ᴏɴʟɪɴᴇ.")

    if validated_user.is_self:
        return await replyreport.edit_text("**__ɪ ᴄᴀɴ'ᴛ ᴛʀᴀᴄᴋ ᴍʏsᴇʟғ.__**")

    await replyreport.edit_text("✅ **ᴜꜱᴇʀ ᴠᴀʟɪᴅᴀᴛᴇᴅ!\n\n🔄 ᴛʀᴀᴄᴋɪɴɢ ɴᴏᴡ...**")
    await sleep(3)
    dbchat = await get_served_chats()
    user_id = validated_user.id
    addmintext = ""
    foundtext = ""
    ownertext = ""
    addminfoundin = 0
    foundin = 0
    ownerin = 0

    for chat in dbchat:
        chat_id = int(chat["chat_id"])
        try:
            user = await app.get_chat_member(chat_id, user_id)
            if user.status == ChatMemberStatus.OWNER:
                ownerin += 1
                ownertext += f"\n {ownerin}. {chat_id}"
            elif user.status == ChatMemberStatus.ADMINISTRATOR:
                addminfoundin += 1
                addmintext += f"\n {addminfoundin}. {chat_id}"
            elif user.status == ChatMemberStatus.MEMBER:
                foundin += 1
                foundtext += f"\n {foundin}. {chat_id}"
            await sleep(0.2)
        except UserNotParticipant:
            continue
        except FloodWait as e:
            flood_time = int(e.value)
            if flood_time > 200:
                continue
            await sleep(flood_time)
        except:
            pass

    await sleep(1)
    ran_hash = f"\\cache\\UserChats{user_id}.txt"
    data = f"OwnerGroupsID:\n{ownertext}\n\n\nAdminGroupsID:\n{addmintext}\n\n\nMemberGroupsID:\n{foundtext}"
    with open(ran_hash, "w") as lyr:
        lyr.write(data)
    mtext = f"""✅ **Tracking Completed!**

✨ **User Info!**
**‣ ɴᴀᴍᴇ:** {validated_user.mention}
**‣ ᴜsᴇʀ_ɪᴅ:** `{validated_user.id}`
**‣ ᴜsᴇʀɴᴀᴍᴇ:** @{validated_user.username}

**Common Chats** = {ownerin + addminfoundin + foundin}
**Owner In** = {ownerin} Groups
**Admin In** = {addminfoundin} Groups
**Member In** = {foundin} Groups"""

    try:
        await message.reply_document(ran_hash, caption=mtext, file_name="UserChats.txt")
        await replyreport.delete()
    except Exception as e:
        await replyreport.edit_text(_["error_1"].format(str(e)))
    finally:
        os.remove(ran_hash)
