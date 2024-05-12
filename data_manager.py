import requests
from pprint import pprint


my_file = open(".env", "r")
content = my_file.read().split('\n')
SHEETY_ID = content[0].split('=')[1]
SHEETY_TOKEN = content[1].split('=')[1]
my_file.close()

sheety_url = f'https://api.sheety.co/{SHEETY_ID}/flightDeals/prices'
sheety_headers={
"Authorization": f"Bearer {SHEETY_TOKEN}"
}

class DataManager:
    #This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.destination_data={}

    def get_destination_data(self):
        sheety_response = requests.get(url=sheety_url, headers=sheety_headers)
        sheety_data = sheety_response.json()
        self.destination_data = sheety_data["prices"]
        pprint(sheety_data)
        return self.destination_data

    def update_destination_data(self):
        for city in self.destination_data:
            body={
                "price":{
                    "iataCode": city["iataCode"]
                }
            }
            sheety_response = requests.put(url=f"{sheety_url}/{city['id']}", json=body, headers=sheety_headers)
    pass