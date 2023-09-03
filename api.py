import requests
from db import RandomToDoDB

class ApiCall:
    ''' this class returns a random activity with the ability to 
    filter activities by type, number of participants, price range, 
    and accessibility range. '''

    def new_activity(self, **kwargs):
        r = requests.get('http://www.boredapi.com/api/activity', params=(kwargs))

        db = RandomToDoDB()
        db.create(r.json())

        return r.json()
