import os

from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from pathlib import Path

from src.db import db

from dotenv import load_dotenv

load_dotenv()

storage = MemoryStorage()

bot = Bot(os.getenv('bot_key'))
dp = Dispatcher(bot, storage=storage)
BASE_DIR = Path(__file__).resolve().parent
lang_dir = BASE_DIR.joinpath('src').joinpath('languages') / 'languages.json'
