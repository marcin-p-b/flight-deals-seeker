from data_manager import DataManager
from flight_search import FlightSearch
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from notification_manager import NotificationManager

data_manager = DataManager()
notification_manager = NotificationManager()
flight_search = FlightSearch()
sheety_data = data_manager.get_destination_data()

origin_city_code = "LON"
TODAY = datetime.now()
SIX_MONTHS_FROM_TODAY = TODAY + relativedelta(months=6)
departure_date = TODAY.strftime("%d/%m/%Y"),
return_date = SIX_MONTHS_FROM_TODAY.strftime("%d/%m/%Y")


if sheety_data[0]["iataCode"] == "":
    for row in sheety_data:
        row["iataCode"] = flight_search.get_destination_code(row["city"])
    print(f"sheet_data:\n {sheety_data}")
    data_manager.destination_data = sheety_data
    data_manager.update_destination_data()

for destination in sheety_data:
        flight = flight_search.get_flight_prices(
            origin_city_code=origin_city_code,
            destination_code=destination["iataCode"],
            date_from=departure_date,
            date_to=return_date,
            curr="GBP",
            time_there_from="7",
            time_there_to="28",
        )
        if flight is None:
            continue

        try:
            if destination["lowestPrice"] > flight.price:
                if flight.stop_overs == 0:
                    message = f"Low price alert! Only {flight.price}{"£"} to fly from {flight.departure_city}-{flight.departure_code} to {flight.destination_city}-{flight.destination_code}, from {flight.date_from} to {flight.date_to}."
                else:
                    message = f"Low price alert! Only {flight.price}{"£"} to fly from {flight.departure_city}-{flight.departure_code} to {flight.destination_city}-{flight.destination_code}, from {flight.date_from} to {flight.date_to}.\n\n Flight has {flight.stop_overs} stop over, via {flight.via_city}."
                notification_manager.send_email(message=message)
        except TypeError:
            print("Please don't leave an empty space in the spreadsheet")
            continue


