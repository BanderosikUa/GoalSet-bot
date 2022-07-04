from config import bot
from ..languages import get_json_name
from ..keyboards import inline_kb_manage
from ..db import db


async def show_goals(user_id, user_lang, table_name):
    goals_list = db.get_goals(user_id, table_name)[1:]  # because of 1 elem is time
    if goals_list:
        await bot.send_message(user_id, get_json_name(user_lang, 'answer_get_goals'))
        for index, goal in enumerate(goals_list):
            callback = goal.split('@', 2)[1]  # it's our password
            text = goal.split('@', 2)[2]  # our text
            await bot.send_message(user_id, f'{index+1}.{text.capitalize()}',
                                    reply_markup=inline_kb_manage(table_name,
                                    callback, index+1))
    else:
        await bot.send_message(user_id, get_json_name(user_lang, 'get_goals_empty'))