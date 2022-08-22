import requests
from os import environ


class PositionStack:

    def __init__(self):
        # prod
        # self.base_url = 'http://api.positionstack.com/v1'
        self.base_url = 'http://localhost:5000'
        self.api_key = environ.get('POSITIONSTACK_API_KEY')

    def geocode(self, address):
        response = requests.get(f'{self.base_url}/forward', params={
            'access_key': self.api_key,
            'query': address
        })
        return response
