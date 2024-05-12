
class FlightData:
    #This class is responsible for structuring the flight data.
    def __init__(self, price, departure_code, departure_city, date_from, date_to, destination_city, destination_code, stop_overs=0, via_city=""):
        self.price = price
        self.departure_code = departure_code
        self.departure_city = departure_city
        self.date_from = date_from
        self.date_to = date_to
        self.destination_city = destination_city
        self.destination_code = destination_code
        self.stop_overs = stop_overs
        self.via_city = via_city