import time

from calendar import monthrange


def month_len() -> int:
    date = time.localtime(time.time())
    year, month = date.tm_year, date.tm_mon
    return monthrange(year, month)[1]

def days_len(table_name) -> int:
    from_verbally_to_int_dict = {
        'today_goals': 0,
        'tomorrow_goals': 1,
        'week_goals': 7,
        'month_goals': month_len(),
        'year_goals': 365
        }

    if table_name in from_verbally_to_int_dict:
        return from_verbally_to_int_dict[table_name]
