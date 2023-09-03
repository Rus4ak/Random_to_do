import sqlite3
import requests
import unittest
from unittest.mock import Mock
from db import RandomToDoDB
from api import ApiCall

class TestRandomToDoDB(unittest.TestCase):
    def setUp(self):
        # Create a temporary test database in memory
        self.connect = sqlite3.connect('RandomToDo.sql')
        self.cursor = self.connect.cursor()
        self.db = RandomToDoDB()
        self.api_call = ApiCall()

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

    def test_api_call(self):
        # Create a mock response to simulate the API call
        mock_response = Mock()
        mock_response.json.return_value = {
            'activity': 'Test Activity',
            'type': 'Test Type',
            'participants': 2,
            'price': 0.5,
            'link': 'https://example.com',
            'key': 'test-key',
            'accessibility': 0.7
        }

        # Mock the requests.get method to return the mock response
        with unittest.mock.patch('requests.get', return_value=mock_response) as mock_get:
            kwargs = {
                'type': 'Test Type',
                'price': 0.5
            }

            # Call the new_activity method with specific arguments
            result = self.api_call.new_activity(**kwargs)
            mock_get.assert_called_once_with('http://www.boredapi.com/api/activity', params=kwargs)
            self.assertEqual(result, mock_response.json())


if __name__ == '__main__':
    unittest.main()
