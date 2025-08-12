import requests
import json
import os

def get_weather_data(location):

    api_url = f"http://api.weatherapi.com/v1/current.json?key={os.environ['WEATHER_API_KEY']}&q={location}&aqi=yes"

    response = requests.get(api_url)

    if response.status_code == requests.codes.ok:
        data = json.loads(response.text)
        return data
    else:
        print("Error:", response.status_code, response.text)
        return None