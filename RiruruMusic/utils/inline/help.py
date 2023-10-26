from typing import Union
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def help_pannel(_, START: Union[bool, int] = None):
    mark = [
        InlineKeyboardButton(text=_["BACK_BUTTON"], callback_data=f"settingsback_helper")
        if START
        else
        InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close")
    ]

    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="ᴀᴅᴍɪɴ", callback_data="help_callback hb1"),
                InlineKeyboardButton(text="ᴀᴜᴛʜ", callback_data="help_callback hb2"),
                InlineKeyboardButton(text="ʙʟᴀᴄᴋʟɪsᴛ", callback_data="help_callback hb3")
            ],
            [
                InlineKeyboardButton(text="ʙʀᴏᴀᴅᴄᴀsᴛ", callback_data="help_callback hb4"),
                InlineKeyboardButton(text="ɢʙᴀɴ", callback_data="help_callback hb12"),
                InlineKeyboardButton(text="ᴇxᴛʀᴀs", callback_data="help_callback hb5")
            ],
            [
                InlineKeyboardButton(text="ᴏᴡɴᴇʀ", callback_data="help_callback hb7"),
                InlineKeyboardButton(text="ᴩʟᴀʏ", callback_data="help_callback hb8"),
                InlineKeyboardButton(text="ᴩʟᴀʏʟɪsᴛ", callback_data="help_callback hb6")
            ],
            [
                InlineKeyboardButton(text="ᴠɪᴅᴇᴏᴄʜᴀᴛs", callback_data="help_callback hb10"),
                InlineKeyboardButton(text="sᴛᴀʀᴛ", callback_data="help_callback hb11"),
                InlineKeyboardButton(text="sᴜᴅᴏ", callback_data="help_callback hb9")
            ],
            mark,
        ]
    )
    return upl


def help_back_markup(_):
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text=_["BACK_BUTTON"], callback_data=f"settings_back_helper")
            ]
        ]
    )
    return upl


def private_help_panel(BOT_USERNAME):
    buttons = [
        [
            InlineKeyboardButton(text="˹ʜᴇʟᴘ ᴍᴇɴᴜ˼", url=f"https://t.me/{BOT_USERNAME}?start=help")
        ]
    ]
    return buttons
