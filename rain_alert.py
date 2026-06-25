import requests
from twilio.rest import Client
import os

OWM_Endpoint = "https://api.openweathermap.org/data/2.5/forecast"
api_key = os.environ.get("OWM_api_key")
account_sid = os.environ.get("OWM_account_sid")
auth_token = os.environ.get("OWM_auth_token")

weather_parameters = {
    "lat": 39.0997,
    "lon": -94.5786,
    "appid": api_key,
    "cnt": 4,
}

response = requests.get(OWM_Endpoint, params=weather_parameters)
response.raise_for_status()
weather_data = response.json()
# print(weather_data["list"][0]["weather"][0]["id"])

will_rain = False
for hour_data in weather_data["list"]:
    condition_code = hour_data["weather"][0]["id"]
    if int(condition_code) < 700:
        will_rain = True
        break

if will_rain:
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        from_="whatsapp:+14155238886",
        body="It's going to rain today. Remember to bring an ☔️",
        to="whatsapp:+17473290982"
    )
    print(message.status)
