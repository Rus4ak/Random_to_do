import unittest
import sqlite3
import requests
from db import RandomToDoDB

class TestRandomToDoDB(unittest.TestCase):
    def setUp(self):
        # Create a temporary test database in memory
        self.connect = sqlite3.connect('RandomToDo.sql')
        self.cursor = self.connect.cursor()
        self.db = RandomToDoDB()

    def tearDown(self):
        # Close the database connection and clean up
        self.cursor.execute('''
                            DELETE FROM random_to_do 
                            WHERE id = (SELECT MAX(id) 
                            FROM random_to_do)''')
        self.connect.commit()
        self.cursor.close()
        self.connect.close()

    def test_db(self):
        r = requests.get('http://www.boredapi.com/api/activity/')
        activity_json = r.json()

        # Test the create method
        self.db.create(activity_json)
        self.cursor.execute('SELECT * FROM random_to_do ORDER BY id DESC LIMIT 1')

        result = self.cursor.fetchone()
        self.assertIsNotNone(result)
        self.assertEqual(result[1], activity_json['activity'])
        self.assertEqual(result[2], activity_json['type'])

        # Test the show_activities method
        activities = self.db.show_activities()
        self.assertIn(len(activities), list(range(6)))


if __name__ == '__main__':
    unittest.main()
