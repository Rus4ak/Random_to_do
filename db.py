import sqlite3
from datetime import datetime

class RandomToDoDB:
    ''' class for database management. 
    The "create" method creates a database if it does not exist and adds a new activity to it, 
    the "show_activities" method shows the last 5 activities stored in the database '''

    def create(self, activity_json):
        try:
            connect = sqlite3.connect('RandomToDo.sql')

            create_table = '''
                CREATE TABLE IF NOT EXISTS random_to_do (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    activity TEXT NOT NULL,
                    type TEXT NOT NULL,
                    participants INTEGER NOT NULL,
                    price REAL NOT NULL,
                    link TEXT,
                    key TEXT,
                    accessibility REAL NOT NULL,
                    created_at DATETIME NOT NULL
                );
            '''

            cursor = connect.cursor()
            cursor.execute(create_table)

            insert_random_to_do = '''
                INSERT INTO
                    random_to_do(activity, type, participants, price, link, key, accessibility, created_at)
                VALUES(?, ?, ?, ?, ?, ?, ?, ?)
            '''

            cursor.execute(insert_random_to_do, (
                activity_json['activity'],
                activity_json['type'],
                activity_json['participants'],
                activity_json['price'],
                activity_json['link'],
                activity_json['key'],
                activity_json['accessibility'],
                datetime.now()
            ))

            connect.commit()
            cursor.close()
        
        except sqlite3.Error as error:
            print('The error', error)
        
        finally:
            if connect:
                connect.close()

    
    def show_activities(self):
        try:
            connect = sqlite3.connect('RandomToDo.sql')

            select_activities = '''
                SELECT activity, type, participants, price, link, key, accessibility
                FROM random_to_do
                ORDER BY created_at DESC
                LIMIT 5
            '''

            cursor = connect.cursor()
            cursor.execute(select_activities)
            data = cursor.fetchall()

            return data
        
        except sqlite3.Error as error:
            print('The error', error)

        finally:
            if connect:
                connect.close()

        return None
