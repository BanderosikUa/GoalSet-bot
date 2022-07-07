from config import bot
from ..languages import get_json_name
from ..keyboards import inline_kb_manage
from ..db import db


async def show_goals(user_id: int, user_lang: str, table_name: str):
    goals_list = db.get_goals(user_id, table_name)
    
    if goals_list:
        await bot.send_message(user_id, get_json_name(
                user_lang, 'answer_get_goals')
                )
        for index, goal in enumerate(goals_list):
            goal_id = goal[0]
            goal_text = goal[1]
            await bot.send_message(user_id, f'{index+1}.{goal_text.capitalize()}',
                                   reply_markup=inline_kb_manage(table_name,
                                   goal_id, index+1))
    
    else:
        await bot.send_message(user_id, get_json_name(
                user_lang, 'get_goals_empty')
                )
