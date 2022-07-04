from aiogram import types, Dispatcher
from config import bot
from ..db import db
from typing import NamedTuple

from ..languages import get_json_name
from ..keyboards import inline_kb_manage
from ..other import show_goals

class Calldict(NamedTuple):
    table_name: str
    deleted_str: str
    index: int

async def del_callback(call: types.CallbackQuery):
    cdict = Calldict(*call.data.split(':')[1:])
    user_id = call.from_user.id

    await call.answer('✂_Deleted_✂')
    await bot.delete_message(user_id, call.message.message_id)

    db.delete_goal(user_id, cdict.table_name, cdict.deleted_str)
    goals_list = db.get_goals(user_id, cdict.table_name)
    if len(goals_list) == 1:
        db.delete_all(user_id, cdict.table_name)
        await bot.delete_message(user_id, call.message.message_id - cdict.index)


async def done_callback(call: types.CallbackQuery):
    cdict = Calldict(*call.data.split(':')[1:])
    user_id = call.from_user.id

    await call.answer('✅_Done_✅')
    await bot.delete_message(user_id, call.message.message_id)

    db.add_statistic(user_id, 'completed_goals')
    db.delete_goal(user_id, cdict.table_name, cdict.deleted_str)
    goals_list = db.get_goals(user_id, cdict.table_name)
    if len(goals_list) == 1:
        db.delete_all(user_id, cdict.table_name)
        await bot.delete_message(user_id, call.message.message_id - cdict.index)


async def cancel_callback(call: types.CallbackQuery):
    cdict = Calldict(*call.data.split(':')[1:])
    user_id = call.from_user.id

    await call.answer('❌❌Cancel❌❌')
    await bot.delete_message(user_id, call.message.message_id)

    db.add_statistic(user_id, 'denied_goals')
    db.delete_goal(user_id, cdict.table_name, cdict.deleted_str)
    goals_list = db.get_goals(user_id, cdict.table_name)

    if len(goals_list) == 1:
        db.delete_all(user_id, cdict.table_name)
        await bot.delete_message(user_id, call.message.message_id - cdict.index)


async def show_goals_callback(call: types.CallbackQuery):
    user_id = call.from_user.id
    table_name = call.data.split(":")[1]
    user_lang = call.data.split(':')[2]

    await show_goals(user_id, user_lang, table_name)


def register_callback_handler(dp: Dispatcher):
    dp.register_callback_query_handler(del_callback, text_contains='delete')
    dp.register_callback_query_handler(done_callback, text_contains='done')
    dp.register_callback_query_handler(cancel_callback, text_contains='cancel')
    dp.register_callback_query_handler(show_goals_callback, text_contains='show_goals')