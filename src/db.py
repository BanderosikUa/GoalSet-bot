from datetime import datetime, date
import sqlite3

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

class BaseDatabase():

    __DB_LOCATION = BASE_DIR.joinpath('src') / 'database.sqlite3'
    _goals_tables = (
        'today_goals',
        'tomorrow_goals',
        'week_goals',
        'month_goals',
        'year_goals'
    )

    def __init__(self, is_test=False):

        if is_test:
            self._db_connection = sqlite3.connect(':memory:')
        else:
            self._db_connection = sqlite3.connect(self.__DB_LOCATION,
                                                  check_same_thread=False)
        
        self.cur = self._db_connection.cursor()
        try:
            with self._db_connection:
                self._db_connection.execute('''CREATE TABLE IF NOT EXISTS User (
                    id INTEGER PRIMARY KEY,
                    language TEXT,
                    cache TEXT
                )''')
                for goal_table_name in self._goals_tables:
                    self._db_connection.execute(f'''CREATE TABLE IF NOT EXISTS {goal_table_name} (
                        id INTEGER PRIMARY KEY,
                        goal TEXT,
                        time_created DATE,
                        userId INT,
                        FOREIGN KEY(userId) REFERENCES User(id)
                    )''')

                self._db_connection.execute('''CREATE TABLE IF NOT EXISTS statistic (
                            userId INT,
                            completed_goals INT,
                            denied_goals INT,
                            FOREIGN KEY(userId) REFERENCES User(id)
                        )''')
                self._db_connection.commit()
        except sqlite3.IntegrityError:
            print("couldn't add Python twice")

    def __del__(self):
        self._db_connection.close()


class BaseDbRegistration(BaseDatabase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def register(self, user, language,
                 cache=''):
        self.cur.execute(f"SELECT id FROM User WHERE id ={user}")
        if self.cur.fetchone() is None:
            self.cur.execute("INSERT INTO User VALUES (?, ?, ?)",
                             (user, language, cache)
                             )
            self._db_connection.commit()
        else:
            self.cur.execute("Update User SET language = ? where id = ?",
                             (language, user,))
            self._db_connection.commit()

        self.cur.execute(f"SELECT userId FROM statistic WHERE userId = {user}")
        if self.cur.fetchone() is None:
            self.cur.execute("INSERT INTO statistic VALUES (?, ?, ?)",
                             (user, 0, 0))
            self._db_connection.commit()


class DatabaseGoals(BaseDbRegistration):
    def make_goal(self, user: int,
                  table_name: str, goal: str,
                  time=None):
        """Create goal """
        if not time:
            time = date.strftime(date.today(), '%Y-%m-%d')
        self.cur.execute(f"INSERT INTO {table_name} (goal, time_created, userId) VALUES (?, ?, ?)",
                         (goal, time, user))

        self._db_connection.commit()

    def get_goals(self, user: int, table_name: str, goal_id=None):
        self.cur.execute(
            f"SELECT id, goal, time_created FROM {table_name} WHERE userId = ? {'AND id = ' + str(goal_id) if goal_id else ''}",
            (user,))

        return self.cur.fetchall()

    def delete_goal(self, user: int, table_name: str, deleted_id: int):
        self.cur.execute(f"DELETE FROM {table_name} WHERE id = ?",
                         (deleted_id,))


class DatabaseCache(BaseDbRegistration):
    def append_cache(self, user, cache):
        self.cur.execute("UPDATE User SET cache = ? WHERE id = ?",
                         (cache, user))
        self._db_connection.commit()

    def pop_cache(self, user):
        cache = ''
        self.cur.execute("UPDATE User SET cache = ? WHERE id = ?",
                         (cache, user))
        self._db_connection.commit()

    def get_cache(self, user):
        self.cur.execute("SELECT cache FROM User WHERE id = ?",
                         (user, ))
        cache = self.cur.fetchone()
        if cache:
            return cache[0]
        return None

class DatabaseStatistic(BaseDbRegistration):
    def add_statistic(self, user, denied_or_completed):
        self.cur.execute(f"SELECT {denied_or_completed} FROM statistic\
                         WHERE userId = ?", (user,))
        amount = self.cur.fetchone()[0] + 1
        self.cur.execute(f"UPDATE statistic SET {denied_or_completed} = ?\
                         WHERE userId = ?", (amount, user))
        self._db_connection.commit()

    def get_statistic(self, user):
        self.cur.execute("SELECT denied_goals, completed_goals\
                         FROM statistic WHERE userId = ?", (user,))
        return self.cur.fetchall()



class Database(DatabaseGoals, DatabaseCache, DatabaseStatistic):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def delete_all(self, user: int, table_name: str):
        """ Delete all user goals, only working if you admin"""
        self.cur.execute(f"DELETE FROM {table_name} WHERE userId = ?",
                         (user,))
        self._db_connection.commit()

    def show_lang(self, user):
        self.cur.execute("SELECT language FROM User WHERE id = ?",
                         (user, ))
        lang = self.cur.fetchone()
        if lang:
            return lang[0]
        else:
            return None

    def get_users(self):
        self.cur.execute("SELECT id FROM User")
        return self.cur.fetchall()


db = Database()
