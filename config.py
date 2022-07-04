import os

from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from pathlib import Path

from src.db import db

storage = MemoryStorage()

proxy_url = 'http://proxy.server:3128'
bot = Bot('5172445766:AAES3ZLKjSL38Q7PC5ucUzLBJYYo7jeqme8') 
dp = Dispatcher(bot, storage=storage)
BASE_DIR = Path(__file__).resolve().parent
lang_dir = BASE_DIR.joinpath('src').joinpath('languages') / 'languages.json'
