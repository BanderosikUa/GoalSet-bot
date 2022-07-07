import string

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from random import choice

from ..keyboards import *
from ..db import db
from ..other import days_len, show_goals
from ..languages import get_json_name
from config import bot


class FSMAdmin(StatesGroup):
    goal = State()


async def command_start(message: types.Message):
    await message.answer(get_json_name('english', 'startup'),
                         disable_notification=True)
    await message.answer(get_json_name('english', 'language_setting'),
                         reply_markup=kb_language,
                         disable_notification=True)


async def command_menu(message: types.Message):
    user_id = message.from_user.id
    user_lang = db.show_lang(user_id)
    if not user_lang:
        user_lang = db.show_lang(message.from_user.id)
    await message.answer(get_json_name(user_lang, 'menu'),
                         reply_markup=kb_menu(user_lang))


async def commands(message: types.Message):
    user_id = message.from_user.id
    message_id = message.message_id
    user_lang = db.show_lang(user_id)

    # ---kb_menu---
    if message.text == '🇷🇺 russian':
        db.register(user_id, 'russian')
        await message.answer(message.text, 
                             reply_markup=kb_menu('russian'),
                             disable_notification=True)
    elif message.text == '🏴󠁧󠁢󠁥󠁮󠁧󠁿 english':
        db.register(user_id, 'english')
        await message.answer(message.text,
                             reply_markup=kb_menu('english'),
                             disable_notification=True)
    elif message.text == get_json_name(user_lang, 'languages'):
        await message.answer(message.text, 
                             reply_markup=kb_language,
                             disable_notification=True)
    elif message.text == get_json_name(user_lang, 'settings'):
        await message.answer(message.text,
                             reply_markup=kb_menu(user_lang),
                             disable_notification=True)
    # --- Menu_details ---
    elif message.text == get_json_name(user_lang, 'menu'):
        await message.answer(message.text,
                             reply_markup=kb_menu_details(user_lang),
                             disable_notification=True)
    elif message.text == get_json_name(user_lang, 'back'):
        db.pop_cache(user_id)
        await message.answer(message.text,
                             reply_markup=kb_menu_details(user_lang),
                             disable_notification=True)
    elif message.text == get_json_name(user_lang, 'statistic'):
        await message.answer(f"✅ {get_json_name(user_lang, 'amount_of_completed_goals')}: {db.get_statistic(user_id)[0][1]}",
                             disable_notification=True)
        await message.answer(f"❌ {get_json_name(user_lang, 'amount_of_denied_goals')}: {db.get_statistic(user_id)[0][0]}",
                             reply_markup=kb_menu(user_lang),
                             disable_notification=True)

    # --- kb_nav ---
    buttons = ['year_goals', 'month_goals', 'week_goals',
               'tomorrow_goals', 'today_goals']
    menu_buttons = get_json_name(user_lang, *buttons)
    if message.text in menu_buttons:
        for ind, val in enumerate(menu_buttons):
            if val == message.text:
                db.append_cache(user_id, buttons[ind])
                await message.answer(message.text,
                                     reply_markup=kb_nav(user_lang),
                                     disable_notification=True)

    elif message.text == get_json_name(user_lang, 'add_goal'):
        await FSMAdmin.goal.set()
        await message.answer(get_json_name(user_lang, 'make_goal_user'),
                             reply_markup=kb_cancel(user_lang),
                             disable_notification=True)

    elif message.text == get_json_name(user_lang, 'get_goals'):
        table_name = db.get_cache(user_id)
        await show_goals(user_id, user_lang, table_name)


async def make_goal(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user_lang = db.show_lang(user_id)
    table_name = db.get_cache(user_id)
    text = message.text
    db.make_goal(user_id, table_name, text)
    await message.reply('👍',
                        reply_markup=kb_nav(user_lang),
                        disable_notification=True)
    await state.finish()


async def cancel_get_goal(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user_lang = db.show_lang(user_id)
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.answer(get_json_name(user_lang, 'cancel'),
                         reply_markup=kb_menu_details(user_lang))


def register_handler_commands(dp: Dispatcher):
    dp.register_message_handler(command_start, commands='start')
    dp.register_message_handler(command_menu, commands='menu')
    dp.register_message_handler(commands)
    dp.register_message_handler(cancel_get_goal, 
                                Text(equals=['Cancel', 'Отмена']),
                                state='*')
    dp.register_message_handler(make_goal, state=FSMAdmin.goal)
