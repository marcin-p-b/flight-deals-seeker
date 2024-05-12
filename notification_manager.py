import smtplib
import requests

my_file = open(".env", "r")
content = my_file.read().split('\n')
SHEETY_ID = content[0].split('=')[1]
SHEETY_TOKEN = content[1].split('=')[1]
email = content[3].split('=')[1]
password = content[4].split('=')[1][1:-1].strip()
my_file.close()

sheety_url = f"https://api.sheety.co/{SHEETY_ID}/flightDeals/users"
sheety_headers={
"Authorization": f"Bearer {SHEETY_TOKEN}"
}


class NotificationManager:
    #This class is responsible for sending notifications with the deal flight details.
    def __init__(self):
        pass

    def send_email(self, message):
        message = f"{message}"
        sheety_response = requests.get(url=sheety_url, headers=sheety_headers)
        sheety_data = sheety_response.json()
        with smtplib.SMTP("smtp.poczta.onet.pl", port=587) as connection:
            connection.starttls()
            connection.login(user=email, password=password)
            for users in sheety_data["users"]:
                connection.sendmail(from_addr=email, to_addrs=users["email"], msg=f"Subject: Flight deals for today\n\n{message}".encode('utf-8'))
        pass

