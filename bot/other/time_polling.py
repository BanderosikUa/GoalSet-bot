import time
import asyncio
import aioschedule
from config import bot
from ..languages import get_json_name
from aiogram.types import User

from bot.db import db

from ..keyboards import inline_kb_goals
from ..other import show_goals

async def update():
    tables = ['tomorrow_goals', 'week_goals', 'month_goals', 'year_goals']
    for user in db.get_users():
        user = user[0]
        user_lang = db.show_lang(user)
        for table in tables:
            days_to_goal = db.get_time(user, table)
            if days_to_goal:
                new_days_to_goal = int(days_to_goal) - 1
                if new_days_to_goal == 0:
                    if table == 'tomorrow_goals':
                        tomorrow_goals = db.get_goals(user, 'tomorrow_goals')
                        if tomorrow_goals:
                            db.make_goal(user, 'today_goals', ";".join(tomorrow_goals[1:]), tomorrow_goals[0])
                            db.delete_all(user, 'tomorrow_goals')
                            name = await bot.get_chat_member(user, user)
                            await bot.send_message(user,
                                                   get_json_name(user_lang, "new_day").replace('@%', name.user.first_name),
                                                   reply_markup=inline_kb_goals('today_goals', user_lang))

                            await asyncio.sleep(30)
                    else:
                        await bot.send_message(user, get_json_name(user_lang, table+'_reached'),
                                               reply_markup=inline_kb_goals(table, db.show_lang(user)))
                else:
                    db.new_time(user, table, new_days_to_goal)

    await asyncio.sleep(60)


async def update_end_day():
    table = 'today_goals'
    for user in db.get_users():
        user = user[0]
        user_lang = db.show_lang(user)
        goals = db.get_goals(user, table)
        if goals:
            await bot.send_message(user, get_json_name(user_lang, 'end_of_day'),
                                   reply_markup=inline_kb_goals(table, db.show_lang(user)))

    await asyncio.sleep(60)


async def scheduler():
    aioschedule.every().day.at("7:00").do(update)
    aioschedule.every().day.at("19:00").do(update_end_day)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_startup(_):
    asyncio.create_task(scheduler())
