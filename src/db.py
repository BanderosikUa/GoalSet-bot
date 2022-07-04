import sqlite3

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


class DataBase:
    def __init__(self, dir=BASE_DIR.joinpath('src') / 'database.db'):
        self.db = sqlite3.connect(dir, check_same_thread=False)
        self.sql = self.db.cursor()
        self.db.execute('''CREATE TABLE IF NOT EXISTS settings (
            user INTEGER PRIMARY KEY,
            language TEXT,
            cache TEXT
        )''')
        self.db.execute('''CREATE TABLE IF NOT EXISTS goals (
            user INTEGER PRIMARY KEY,
            today_goals TEXT,
            tomorrow_goals TEXT,
            week_goals TEXT,
            month_goals TEXT,
            year_goals TEXT
        )''')
        self.db.execute('''CREATE TABLE IF NOT EXISTS statistic (
                    user INTEGER PRIMARY KEY,
                    completed_goals INT,
                    denied_goals INT
                )''')
        self.db.commit()

    def register(self, user, language,
                 cache='', daygoal='', tomorrowgoal='',
                 weakgoal='', monthgoal='', yeargoal=''):
        self.sql.execute(f"SELECT user FROM settings WHERE user ={user}")
        if self.sql.fetchone() is None:
            self.sql.execute("INSERT INTO settings VALUES (?, ?, ?)",
                             (user, language, cache)
                            )
            self.db.commit()
        else:
            self.sql.execute("Update settings SET language = ? where user = ?",
                             (language, user,))
            self.db.commit()
        self.sql.execute(f"SELECT user FROM goals WHERE user = {user}")
        if self.sql.fetchone() is None:
            self.sql.execute("INSERT INTO goals VALUES (?, ?, ?, ?, ?, ?)",
                             (user, daygoal, tomorrowgoal,
                              weakgoal, monthgoal, yeargoal))
            self.db.commit()
        self.sql.execute(f"SELECT user FROM statistic WHERE user = {user}")
        if self.sql.fetchone() is None:
            self.sql.execute("INSERT INTO statistic VALUES (?, ?, ?)",
                             (user, 0, 0))
            self.db.commit()

    def make_goal(self, user, table_name, goal, date: str):
        self.sql.execute(f"SELECT {table_name} FROM goals WHERE user = ?",
                         (user, ))
        previous_daygoal = self.sql.fetchone()
        if previous_daygoal[0] != '':
            string = " ".join(str(x) for x in previous_daygoal)
            user_daygoal = string + goal + ';'
        else:
            user_daygoal = date + ';' + goal + ';'
        self.sql.execute(f"UPDATE goals SET {table_name} = ? WHERE user = ?",
                         (user_daygoal, user))
        self.db.commit()

    def delete_all(self, user, table_name):
        self.sql.execute(f"UPDATE goals SET {table_name} = ? WHERE user = ?",
                         ('', user))
        self.db.commit()

    def append_cache(self, user, cache):
        self.sql.execute("UPDATE settings SET cache = ? WHERE user = ?",
                         (cache, user))
        self.db.commit()

    def pop_cache(self, user):
        cache = ''
        self.sql.execute("UPDATE settings SET cache = ? WHERE user = ?",
                         (cache, user))
        self.db.commit()

    def get_cache(self, user):
        self.sql.execute("SELECT cache FROM settings WHERE user = ?",
                         (user, ))
        cache = self.sql.fetchone()
        if cache:
            return cache[0]
        return None

    def get_goals(self, user, table_name, if_string: bool = False):
        self.sql.execute(f"SELECT {table_name} FROM goals WHERE user = ?",
                         (user, ))
        fetch_one = self.sql.fetchone()
        if fetch_one:
            string = fetch_one[0]
            if not if_string:
                List = list(string.split(';'))
                if List:
                    List.pop()
                    return List
                else:
                    return None
            return string
        else:
            return None

    def delete_goal(self, user, table_name, deleted_str):
        goals = self.get_goals(user, table_name)
        for goal in goals:
            if deleted_str in goal:
                goals.remove(goal)
                self.sql.execute(f"UPDATE goals SET {table_name} = ?\
                                 WHERE user = ?", (";".join(goals)+';', user))
                self.db.commit()
                return

    def show_lang(self, user):
        self.sql.execute("SELECT language FROM settings WHERE user = ?",
                         (user, ))
        lang = self.sql.fetchone()
        if lang:
            return lang[0]
        else:
            return None

    def add_statistic(self, user, denied_or_completed):
        self.sql.execute(f"SELECT {denied_or_completed} FROM statistic\
                         WHERE user = ?", (user,))
        amount = self.sql.fetchone()[0] + 1
        self.sql.execute(f"UPDATE statistic SET {denied_or_completed} = ?\
                         WHERE user = ?", (amount, user))
        self.db.commit()

    def get_statistic(self, user):
        self.sql.execute("SELECT denied_goals, completed_goals\
                         FROM statistic WHERE user = ?", (user,))
        return self.sql.fetchall()

    def get_time(self, user, table_name):
        time = self.get_goals(user, table_name)
        if time:
            return time[0]
        else:
            return None

    def get_users(self):
        self.sql.execute("SELECT user FROM goals")
        return self.sql.fetchall()

    def update_time(self, user, table_name, new_time):
        goals = self.get_goals(user, table_name)
        goals[0] = str(new_time)
        self.sql.execute(f"UPDATE goals SET {table_name} = ?\
                         WHERE user = ?",
                         (";".join(goals)+';', user))
        self.db.commit()

db = DataBase()
