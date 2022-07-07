from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from ..languages import get_json_name

# --- Language setup ---
b_rus = KeyboardButton('🇷🇺 russian')
b_eng = KeyboardButton('🏴󠁧󠁢󠁥󠁮󠁧󠁿 english')
kb_language = ReplyKeyboardMarkup(resize_keyboard=True, ).row(b_rus, b_eng)


# --- Main display ---
def kb_menu(user_lang):
    b_menu = KeyboardButton(get_json_name(user_lang, 'menu'))
    b_setting_lang = KeyboardButton(get_json_name(user_lang, 'languages'))
    b_statistic = KeyboardButton(get_json_name(user_lang, 'statistic'))
    return ReplyKeyboardMarkup(resize_keyboard=True, )\
        .row(b_menu, b_setting_lang).row(b_statistic)

# --- Menu buttons ---

def kb_menu_details(user_lang):
    b_settings = KeyboardButton(get_json_name(user_lang, 'settings'))
    menu_buttons = get_json_name(user_lang, 'year_goals',
                                 'month_goals', 'week_goals',
                                 'tomorrow_goals', 'today_goals')
    menu_buttons = [KeyboardButton(i) for i in menu_buttons]
    return ReplyKeyboardMarkup(resize_keyboard=True, ).row(
        menu_buttons[1], menu_buttons[0])\
        .row(menu_buttons[3], menu_buttons[2])\
        .row(menu_buttons[4], b_settings)


def kb_cancel(user_lang):
    b_cancel = KeyboardButton(get_json_name(user_lang, 'cancel'))
    return ReplyKeyboardMarkup(resize_keyboard=True, ).row(b_cancel)

# --- Nav_menu_but ---add, delete goals

def kb_nav(user_lang):
    b_back = KeyboardButton(get_json_name(user_lang, 'back'))
    b_add = KeyboardButton(get_json_name(user_lang, 'add_goal'))
    b_get_goals = KeyboardButton(get_json_name(user_lang, 'get_goals'))
    return ReplyKeyboardMarkup(resize_keyboard=True, )\
        .row(b_add).row(b_back, b_get_goals)
