import json
from config import lang_dir


def get_json_name(user_lang, *args):
    buttons = []
    for i in args:
        buttons.append(json.load(open(lang_dir))[user_lang][i])
    if len(buttons) == 1:
        return buttons[0]
    return buttons  
