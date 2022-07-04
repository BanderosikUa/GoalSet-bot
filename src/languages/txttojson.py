import json


dict_eng = {}
dict_rus = {}

__all__ = ['lang_dir']

with open('english.txt', 'r', encoding='UTF-8') as english, open('russian.txt', 'r', encoding='UTF-8') as russian:
    for string in english:
        key, desc = string.strip().split('; ', 1)
        dict_eng[key] = desc
    for string in russian:
        key, desc = string.strip().split('; ', 1)
        dict_rus[key] = desc

dictionary = {'english': dict_eng, 'russian': dict_rus}

with open('languages.json', 'w') as ouf:
    json.dump(dictionary, ouf)

lang_dir = json.load(open('languages.json'))