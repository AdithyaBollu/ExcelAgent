import requests
import json
import os

def get_nutrition_info (food):
    api_url = f"https://api.calorieninjas.com/v1/nutrition?query={food}"

    response = requests.get(api_url, headers={"X-API-Key": os.environ["NUTRITION_API_KEY"]})

    if response.status_code == requests.codes.ok:
        data = json.loads(response.text)
        print(data)
        return json.dumps(data["items"])
    else:
        print("Error:", response.status_code, response.text )
        return json.dumps({"error": f"API request failed with status {response.status_code}"})