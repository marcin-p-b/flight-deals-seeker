import requests
from flight_data import FlightData
from pprint import pprint

my_file = open(".env", "r")
content = my_file.read().split('\n')
TEQUILA_ID = content[2].split('=')[1]
my_file.close()

tequila_url = f'https://api.tequila.kiwi.com'

class FlightSearch:

    #This class is responsible for talking to the Flight Search API.
    def get_destination_code(self, city_name):
        location_endpoint = f"{tequila_url}/locations/query"
        headers = {"apikey": TEQUILA_ID}
        query = {"term": city_name, "location_types": "city"}
        tequila_response = requests.get(url=location_endpoint, headers=headers, params=query)
        result = tequila_response.json()["locations"]
        code = result[0]["code"]
        return code

    def get_flight_prices(self, origin_city_code, destination_code, date_from, date_to, curr, time_there_from, time_there_to):
        tequila_headers = {
            "apikey": f'{TEQUILA_ID}'
        }
        query = {
            "fly_from": origin_city_code,
            "fly_to": destination_code,
            "date_from": date_from,
            "date_to": date_to,
            "curr": curr,
            "max_stopovers": "0",
            "nights_in_dst_from": time_there_from,
            "nights_in_dst_to": time_there_to,
            "flight_type": "round",
            "one_for_city": "1",
        }

        tequila_response = requests.get(
            url=f"{tequila_url}/v2/search",
            headers=tequila_headers,
            params=query,
        )
        try:
            data = tequila_response.json()["data"][0]
            pprint(data)
        except KeyError:
            print(f"Flight to {destination_code} not found")
            return None
        except:
            query["max_stopovers"] = 1

            tequila_response = requests.get(
                url=f"{tequila_url}/v2/search",
                headers=tequila_headers,
                params=query,
            )

            data = tequila_response.json()["data"][0]
            flight_data = FlightData(
                price=data["price"],
                departure_code=data["route"][0]["cityFrom"],
                departure_city=data["route"][0]["flyFrom"],
                destination_city=data["route"][1]["cityTo"],
                destination_code=data["route"][1]["flyTo"],
                date_from=data["route"][0]["local_arrival"].split("T")[0],
                date_to=data["route"][2]["local_departure"].split("T")[0],
                via_city = data["route"][0]["cityTo"]
            )
            print(f"{flight_data.destination_city}: £{flight_data.price}")
            return flight_data
        else:
            flight_data = FlightData(
                price=data["price"],
                departure_code=data["cityFrom"],
                departure_city=data["flyFrom"],
                destination_city=data["cityTo"],
                destination_code=data["flyTo"],
                date_from=data["route"][0]["local_arrival"].split("T")[0],
                date_to=data["route"][1]["local_departure"].split("T")[0]
            )
            print(f"{flight_data.destination_city}: £{flight_data.price}")
            return flight_data
