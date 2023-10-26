from RiruruMusic import app
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def back_stats_markup(_):
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text=_["BACK_BUTTON"], callback_data="TOPMARKUPGET"),
                InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close")
            ]
        ]
    )
    return upl


def get_stats_markup(_):
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text=_["SA_B_7"], callback_data="TOPMARKUPGET")
            ],
            [
                InlineKeyboardButton(text=_["SA_B_6"], url=f"https://t.me/{app.username}?start=stats"),
                InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close")
            ]
        ]
    )
    return upl


def stats_buttons(_):
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text=_["SA_B_8"], callback_data="bot_stats_sudo"),
                InlineKeyboardButton(text=_["SA_B_5"], callback_data="TopOverall")
            ],
            [
                InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close")
            ]
        ]
    )
    return upl


def back_stats_buttons(_):
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text=_["BACK_BUTTON"], callback_data="GETSTATS"),
                InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close")
            ]
        ]
    )
    return upl


def top_ten_stats_markup(_):
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text=_["SA_B_2"], callback_data="GetStatsNow Tracks"),
                InlineKeyboardButton(text=_["SA_B_4"], callback_data="GetStatsNow Here")
            ],
            [
                InlineKeyboardButton(text=_["SA_B_1"], callback_data="GetStatsNow Chats"),
                InlineKeyboardButton(text=_["SA_B_3"], callback_data="GetStatsNow Users")
            ],
            [
                InlineKeyboardButton(text=_["BACK_BUTTON"], callback_data="GlobalStats"),
                InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close")
            ]
        ]
    )
    return upl
