from strings import get_command
from config import BANNED_USERS, CLEANMODE_DELETE_MINS

from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from RiruruMusic import app
from RiruruMusic.utils.database import (
    add_nonadmin_chat, cleanmode_off, cleanmode_on, commanddelete_off, commanddelete_on,
    get_aud_bit_name, get_authuser, get_authuser_names, get_playmode, get_playtype,
    get_vid_bit_name, is_cleanmode_on, is_commanddelete_on, is_nonadmin_chat,
    remove_nonadmin_chat, save_audio_bitrate, save_video_bitrate, set_playmode, set_playtype
)
from RiruruMusic.utils.inline.settings import (
    audio_quality_markup, auth_users_markup, playmode_users_markup,
    setting_markup, video_quality_markup, cleanmode_settings_markup
)
from RiruruMusic.utils.inline.start import private_panel
from RiruruMusic.utils.decorators.admins import ActualAdminCB
from RiruruMusic.utils.decorators.language import language, languageCB


### Command
SETTINGS_COMMAND = get_command("SETTINGS_COMMAND")


@app.on_message(filters.command(SETTINGS_COMMAND) & filters.group & ~BANNED_USERS)
@language
async def settings_mar(client, message: Message, _):
    buttons = setting_markup(_)
    await message.reply_text(
        _["setting_1"].format(message.chat.id, message.chat.title),
        reply_markup=InlineKeyboardMarkup(buttons),
    )


@app.on_callback_query(filters.regex("settings_helper") & ~BANNED_USERS)
@languageCB
async def settings_cb(client, CallbackQuery, _):
    try:
        await CallbackQuery.answer(_["set_cb_8"], show_alert=True)
    except:
        pass
    buttons = setting_markup(_)
    return await CallbackQuery.edit_message_text(
        _["setting_1"].format(CallbackQuery.message.chat.id, CallbackQuery.message.chat.title),
        reply_markup=InlineKeyboardMarkup(buttons),
    )


@app.on_callback_query(filters.regex("settingsback_helper") & ~BANNED_USERS)
@languageCB
async def settings_back_markup(client, CallbackQuery: CallbackQuery,_):
    if CallbackQuery.message.chat.type == ChatType.PRIVATE:
        buttons = private_panel(app.username, _)
        await CallbackQuery.message.edit_caption(
            caption=_["start_2"].format(CallbackQuery.from_user.first_name, app.mention),
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    else:
        buttons = setting_markup(_)
        return await CallbackQuery.edit_message_reply_markup(InlineKeyboardMarkup(buttons))


## Audio and Video Quality
async def gen_buttons_aud(_, aud):
    if aud == "High":
        buttons = audio_quality_markup(_, high=True)
    elif aud == "Medium":
        buttons = audio_quality_markup(_, medium=True)
    elif aud == "Low":
        buttons = audio_quality_markup(_, low=True)
    return buttons


async def gen_buttons_vid(_, aud):
    if aud == "High":
        buttons = video_quality_markup(_, high=True)
    elif aud == "Medium":
        buttons = video_quality_markup(_, medium=True)
    elif aud == "Low":
        buttons = video_quality_markup(_, low=True)
    return buttons


# without admin rights
@app.on_callback_query(
    filters.regex(pattern=r"^(SEARCHANSWER|PLAYMODEANSWER|PLAYTYPEANSWER|AUTHANSWER|CMANSWER|COMMANDANSWER|CM|AQ|VQ|PM|AU)$")
    & ~BANNED_USERS
)
@languageCB
async def without_Admin_rights(client, CallbackQuery, _):
    command = CallbackQuery.matches[0].group(1)
    if command == "SEARCHANSWER":
        try:
            return await CallbackQuery.answer(_["setting_3"], show_alert=True)
        except:
            return
    elif command == "PLAYMODEANSWER":
        try:
            return await CallbackQuery.answer(_["setting_10"], show_alert=True)
        except:
            return
    elif command == "PLAYTYPEANSWER":
        try:
            return await CallbackQuery.answer(_["setting_11"], show_alert=True)
        except:
            return
    elif command == "AUTHANSWER":
        try:
            return await CallbackQuery.answer(_["setting_4"], show_alert=True)
        except:
            return
    elif command == "CMANSWER":
        try:
            return await CallbackQuery.answer(_["setting_9"].format(CLEANMODE_DELETE_MINS), show_alert=True)
        except:
            return
    elif command == "COMMANDANSWER":
        try:
            return await CallbackQuery.answer(_["setting_14"], show_alert=True)
        except:
            return
    elif command == "CM":
        try:
            await CallbackQuery.answer(_["set_cb_5"], show_alert=True)
        except:
            pass
        sta = None
        cle = None
        if await is_cleanmode_on(CallbackQuery.message.chat.id):
            cle = True
        if await is_commanddelete_on(CallbackQuery.message.chat.id):
            sta = True
        buttons = cleanmode_settings_markup(_, status=cle, dels=sta)
    elif command == "AQ":
        try:
            await CallbackQuery.answer(_["set_cb_1"], show_alert=True)
        except:
            pass
        aud = await get_aud_bit_name(CallbackQuery.message.chat.id)
        buttons = await gen_buttons_aud(_, aud)
    elif command == "VQ":
        try:
            await CallbackQuery.answer(_["set_cb_2"], show_alert=True)
        except:
            pass
        aud = await get_vid_bit_name(CallbackQuery.message.chat.id)
        buttons = await gen_buttons_vid(_, aud)
    elif command == "PM":
        try:
            await CallbackQuery.answer(_["set_cb_4"], show_alert=True)
        except:
            pass
        playmode = await get_playmode(CallbackQuery.message.chat.id)
        Direct = True if playmode == "Direct" else None
        is_non_admin = await is_nonadmin_chat(CallbackQuery.message.chat.id)
        Group = None if is_non_admin else True
        playty = await get_playtype(CallbackQuery.message.chat.id)
        Playtype = None if playty == "Everyone" else True
        buttons = playmode_users_markup(_, Direct, Group, Playtype)
    
    elif command == "AU":
        try:
            await CallbackQuery.answer(_["set_cb_3"], show_alert=True)
        except:
            pass
        is_non_admin = await is_nonadmin_chat(CallbackQuery.message.chat.id)
        if not is_non_admin:
            buttons = auth_users_markup(_, True)
        else:
            buttons = auth_users_markup(_)

    return await CallbackQuery.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(buttons))


# Audio Video Quality
@app.on_callback_query(filters.regex(pattern=r"^(LQA|MQA|HQA|LQV|MQV|HQV)$") & ~BANNED_USERS)
@ActualAdminCB
async def aud_vid_cb(client, CallbackQuery, _):
    command = CallbackQuery.matches[0].group(1)
    try:
        await CallbackQuery.answer(_["set_cb_6"], show_alert=True)
    except:
        pass
    if command == "LQA":
        await save_audio_bitrate(CallbackQuery.message.chat.id, "Low")
        buttons = audio_quality_markup(_, low=True)
    elif command == "MQA":
        await save_audio_bitrate(CallbackQuery.message.chat.id, "Medium")
        buttons = audio_quality_markup(_, medium=True)
    elif command == "HQA":
        await save_audio_bitrate(CallbackQuery.message.chat.id, "High")
        buttons = audio_quality_markup(_, high=True)
    elif command == "LQV":
        await save_video_bitrate(CallbackQuery.message.chat.id, "Low")
        buttons = video_quality_markup(_, low=True)
    elif command == "MQV":
        await save_video_bitrate(CallbackQuery.message.chat.id, "Medium")
        buttons = video_quality_markup(_, medium=True)
    elif command == "HQV":
        await save_video_bitrate(CallbackQuery.message.chat.id, "High")
        buttons = video_quality_markup(_, high=True)
    try:
        return await CallbackQuery.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(buttons))
    except:
        return


# Play Mode Settings
@app.on_callback_query(filters.regex(pattern=r"^(|MODECHANGE|CHANNELMODECHANGE|PLAYTYPECHANGE)$") & ~BANNED_USERS)
@ActualAdminCB
async def playmode_ans(client, CallbackQuery, _):
    command = CallbackQuery.matches[0].group(1)
    if command == "CHANNELMODECHANGE":
        is_non_admin = await is_nonadmin_chat(CallbackQuery.message.chat.id)
        if is_non_admin:
            await remove_nonadmin_chat(CallbackQuery.message.chat.id)
            Group = True
        else:
            await add_nonadmin_chat(CallbackQuery.message.chat.id)
            Group = None
        playmode = await get_playmode(CallbackQuery.message.chat.id)
        if playmode == "Direct":
            Direct = True
        else:
            Direct = None
        playty = await get_playtype(CallbackQuery.message.chat.id)
        if playty == "Everyone":
            Playtype = None
        else:
            Playtype = True
        buttons = playmode_users_markup(_, Direct, Group, Playtype)
    elif command == "MODECHANGE":
        try:
            await CallbackQuery.answer(_["set_cb_6"], show_alert=True)
        except:
            pass
        playmode = await get_playmode(CallbackQuery.message.chat.id)
        if playmode == "Direct":
            await set_playmode(CallbackQuery.message.chat.id, "Inline")
            Direct = None
        else:
            await set_playmode(CallbackQuery.message.chat.id, "Direct")
            Direct = True
        is_non_admin = await is_nonadmin_chat(CallbackQuery.message.chat.id)
        if is_non_admin:
            Group = None
        else:
            Group = True
        playty = await get_playtype(CallbackQuery.message.chat.id)
        if playty == "Everyone":
            Playtype = False
        else:
            Playtype = True
        buttons = playmode_users_markup(_, Direct, Group, Playtype)
    elif command == "PLAYTYPECHANGE":
        try:
            await CallbackQuery.answer(_["set_cb_6"], show_alert=True)
        except:
            pass
        playty = await get_playtype(CallbackQuery.message.chat.id)
        if playty == "Everyone":
            await set_playtype(CallbackQuery.message.chat.id, "Admin")
            Playtype = False
        else:
            await set_playtype(CallbackQuery.message.chat.id, "Everyone")
            Playtype = True
        playmode = await get_playmode(CallbackQuery.message.chat.id)
        if playmode == "Direct":
            Direct = True
        else:
            Direct = None
        is_non_admin = await is_nonadmin_chat(CallbackQuery.message.chat.id)
        if is_non_admin:
            Group = None
        else:
            Group = True
        buttons = playmode_users_markup(_, Direct, Group, Playtype)
    try:
        return await CallbackQuery.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(buttons))
    except:
        return


# Auth Users Settings
@app.on_callback_query(filters.regex(pattern=r"^(AUTH|AUTHLIST)$") & ~BANNED_USERS)
@ActualAdminCB
async def authusers_mar(client, CallbackQuery, _):
    command = CallbackQuery.matches[0].group(1)
    if command == "AUTHLIST":
        _authusers = await get_authuser_names(CallbackQuery.message.chat.id)
        if not _authusers:
            try:
                return await CallbackQuery.answer(_["setting_5"], show_alert=True)
            except:
                return
        else:
            try:
                await CallbackQuery.answer(_["set_cb_7"], show_alert=True)
            except:
                pass
            j = 0
            await CallbackQuery.edit_message_text(_["auth_6"])
            msg = _["auth_7"]
            for note in _authusers:
                _note = await get_authuser(CallbackQuery.message.chat.id, note)
                user_id = _note["auth_user_id"]
                admin_id = _note["admin_id"]
                admin_name = _note["admin_name"]
                try:
                    user = await client.get_users(user_id)
                    user = user.first_name
                    j += 1
                    msg += f"{j}➤ {user}[`{user_id}`]\n   {_['auth_8']} {admin_name}[`{admin_id}`]\n\n"
                except Exception:
                    continue

            upl = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text=_["BACK_BUTTON"], callback_data="AU"),
                        InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close")
                    ]
                ]
            )
            try:
                return await CallbackQuery.edit_message_text(msg, reply_markup=upl)
            except:
                return
    try:
        await CallbackQuery.answer(_["set_cb_6"], show_alert=True)
    except:
        pass
    if command == "AUTH":
        is_non_admin = await is_nonadmin_chat(CallbackQuery.message.chat.id)
        if is_non_admin:
            await remove_nonadmin_chat(CallbackQuery.message.chat.id)
            buttons = auth_users_markup(_, True)
        else:
            await add_nonadmin_chat(CallbackQuery.message.chat.id)
            buttons = auth_users_markup(_)
    try:
        return await CallbackQuery.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(buttons))
    except:
        return


## Clean Mode

@app.on_callback_query(filters.regex(pattern=r"^(CLEANMODE|COMMANDELMODE)$") & ~BANNED_USERS)
@ActualAdminCB
async def cleanmode_mark(client, CallbackQuery, _):
    try:
        await CallbackQuery.answer(_["set_cb_6"], show_alert=True)
    except:
        pass
    command = CallbackQuery.matches[0].group(1)

    if command == "CLEANMODE":
        sta = None
        if await is_commanddelete_on(CallbackQuery.message.chat.id):
            sta = True
        cle = None
        if await is_cleanmode_on(CallbackQuery.message.chat.id):
            await cleanmode_off(CallbackQuery.message.chat.id)
        else:
            await cleanmode_on(CallbackQuery.message.chat.id)
            cle = True
        buttons = cleanmode_settings_markup(_, status=cle, dels=sta)
        return await CallbackQuery.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(buttons))

    elif command == "COMMANDELMODE":
        cle = None
        sta = None
        if await is_cleanmode_on(CallbackQuery.message.chat.id):
            cle = True
        if await is_commanddelete_on(CallbackQuery.message.chat.id):
            await commanddelete_off(CallbackQuery.message.chat.id)
        else:
            await commanddelete_on(CallbackQuery.message.chat.id)
            sta = True
        buttons = cleanmode_settings_markup(_, status=cle, dels=sta)

    try:
        return await CallbackQuery.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(buttons))
    except:
        return
