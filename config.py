import os

from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from bot.db import db


storage = MemoryStorage()


proxy_url = 'http://proxy.server:3128'
bot = Bot('5172445766:AAES3ZLKjSL38Q7PC5ucUzLBJYYo7jeqme8', proxy=proxy_url)
dp = Dispatcher(bot, storage=storage)
lang_dir = os.getcwd() + "/bot/languages/languages.json"
