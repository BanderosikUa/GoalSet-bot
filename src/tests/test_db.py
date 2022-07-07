import unittest

from datetime import date
from unittest import mock

from ..db import *

class TestDb(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.test_db = Database(is_test=True)
        cls.cur = cls.test_db.cur

    def test_connection(self):
        self.cur.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='User' ''')
        if self.cur.fetchone()[0] == 1:
            print('User table exists.')
        for goal in self.test_db._goals_tables:
            self.cur.execute(f''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='{goal}' ''')
            if self.cur.fetchone()[0] == 1:
                print(f'{goal.capitalize()} table exists.')
            
        
        self.cur.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='statistic' ''')
        if self.cur.fetchone()[0] == 1:
            print('statistic table exists.')

    def test_register_user(self):
        register = self.test_db.register
        id = 1
        language = 'english'
        cache = ''
        register(id, language, cache)

        self.cur.execute(f"SELECT * FROM User WHERE id ={id}")

        response = self.cur.fetchone()
        self.assertTrue(response)

    def test_make_and_get_goals(self):
        user_id = 1
        table_name = 'today_goals'
        goal = 'Make something'

        self.test_db.make_goal(
            user=user_id,
            table_name=table_name,
            goal=goal
        )
        expected_response = [(1, goal)]
        real_response = self.test_db.get_goals(
            user=user_id,
            table_name=table_name
        )
        self.assertEqual(expected_response, real_response)

    def test_delete_goal(self):
        goal_id = 1
        user_id = 1
        table_name = 'today_goals'
        goal = 'Make something'

        self.test_db.make_goal(
            user=user_id,
            table_name=table_name,
            goal=goal
        )
        
        self.test_db.delete_goal(user_id, table_name, goal_id)
        real_response = self.test_db.get_goals(
            user=user_id,
            table_name=table_name,
            goal_id=goal_id
        )
        self.assertFalse(real_response)
