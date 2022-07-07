import enum
import asyncio
import aioschedule
from datetime import date, timedelta

from config import bot
from ..languages import get_json_name
from ..other import show_goals
from src.db import db
from ..keyboards import inline_kb_goals


class Days(enum.Enum):
    Tommorow = 1
    Week = 7
    Month = 31
    Year = 365


async def update():
    tables = ['tomorrow_goals', 'week_goals', 'month_goals', 'year_goals']
    time = [Days.Tommorow, Days.Week, Days.Month, Days.Year]
    for user in db.get_users():
        user = user[0]
        user_lang = db.show_lang(user)
        for index, table in enumerate(tables):
            if table == 'tomorrow_goals':
                tomorrow_goals = db.get_goals(user, 'tomorrow_goals')
                if tomorrow_goals:
                    for goal in tomorrow_goals:
                        goal = goal[1]
                        time_created = goal[2] 
                        db.make_goal(user, 'today_goals', goal, time_created)
                    db.delete_all(user, 'tomorrow_goals')
                    name = await bot.get_chat_member(user, user)
                    await bot.send_message(user,
                                           get_json_name(user_lang, "new_day").replace('@%', name.user.first_name),
                                           reply_markup=inline_kb_goals('today_goals', user_lang))

                    await asyncio.sleep(30)
    await asyncio.sleep(60)


async def update():
    for user in db.get_users():
        user = user[0]
        user_lang = db.show_lang(user)


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
    aioschedule.every().day.at("21:00").do(update_end_day)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_startup(_):
    asyncio.create_task(scheduler())
