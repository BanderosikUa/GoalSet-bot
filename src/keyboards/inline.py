from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
from ..languages import get_json_name


def inline_kb_manage(table_name, string, index):
    del_callback = CallbackData("delete", "table_name", "deleted_string", "index")
    done_callback = CallbackData("done", "table_name", "done_string", "index")
    cancel_callback = CallbackData("cancel", "table_name", "done_string", "index")

    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text='✂', callback_data=del_callback.new(
            table_name=table_name, deleted_string=string, index=index)),
        InlineKeyboardButton(text='✅', callback_data=done_callback.new(
            table_name=table_name, done_string=string, index=index
        )),
        InlineKeyboardButton(text='❌', callback_data=cancel_callback.new(
            table_name=table_name, done_string=string, index=index))
    ]])


def inline_kb_goals(table_name, user_lang):
    callback_data = CallbackData("show_goals", "table_name", "user_lang")

    return InlineKeyboardMarkup().row(InlineKeyboardButton(
        text=f"{get_json_name(user_lang, 'show')} {get_json_name(user_lang, table_name).lower()}",
        callback_data=callback_data.new(table_name=table_name, user_lang=user_lang)))
