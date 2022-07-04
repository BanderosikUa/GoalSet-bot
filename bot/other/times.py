import time

from calendar import monthrange


def month_len() -> int:
    date = time.localtime(time.time())
    year, month = date.tm_year, date.tm_mon
    return monthrange(year, month)[1]


def days_len(table_name) -> int:
    if table_name == 'today_goals':
        return 0
    if table_name == 'tomorrow_goals':
        return 1
    if table_name == 'week_goals':
        return 7
    if table_name == 'month_goals':
        return month_len()
    if table_name == 'year_goals':
        return 365

