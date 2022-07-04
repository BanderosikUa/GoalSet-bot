from aiogram.utils import executor
from config import dp
from logging import basicConfig, DEBUG
from bot.other.time_polling import on_startup

basicConfig(format=u'%(filename)+13s [ LINE:%(lineno)-4s] %(levelname)-8s [%(asctime)s] %(message)s',
                    level=DEBUG)


from bot.handlers import commands, callquery

if __name__ == '__main__':
    commands.register_handler_commands(dp)
    callquery.register_callback_handler(dp)

    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)