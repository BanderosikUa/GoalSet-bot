from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
from ..languages import get_json_name


def inline_kb_manage(table_name: str, goal_id: int, index: int):
    del_callback = CallbackData("delete", "table_name",
                                "goal_id", "index")
    done_callback = CallbackData("done", "table_name",
                                 "goal_id", "index")
    cancel_callback = CallbackData("cancel", "table_name",
                                   "goal_id", "index")

    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text='✂', callback_data=del_callback.new(
            table_name=table_name,  goal_id=goal_id, index=index)),
        InlineKeyboardButton(text='✅', callback_data=done_callback.new(
            table_name=table_name, goal_id=goal_id, index=index
        )),
        InlineKeyboardButton(text='❌', callback_data=cancel_callback.new(
            table_name=table_name,  goal_id=goal_id, index=index))
    ]])


def inline_kb_goals(table_name, user_lang):
    callback_data = CallbackData("show_goals", "table_name", "user_lang")

    return InlineKeyboardMarkup().row(InlineKeyboardButton(
        text=f"{get_json_name(user_lang, 'show')}\
               {get_json_name(user_lang, table_name).lower()}",
        callback_data=callback_data.new(
            table_name=table_name,
            user_lang=user_lang))
            )
