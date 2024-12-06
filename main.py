import requests
from requests.auth import HTTPBasicAuth
import datetime as dt
import os

APP_ID = os.environ.get("APP_ID")
API_KEY = os.environ.get("API_KEY")

# Sheety API credentials
USERNAME = os.environ.get("USERNAME")
PASSWORD = os.environ.get("PASSWORD")

SHEETY_POST_ENDPOINT = os.environ.get("SHEETY_POST_ENDPOINT")

exercise_headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY
}

# Check if environment variables are set
if not all([APP_ID, API_KEY, USERNAME, PASSWORD, SHEETY_POST_ENDPOINT]):
    raise ValueError("One or more environment variables are missing. Please set APP_ID, API_KEY, USERNAME, PASSWORD, and SHEETY_POST_ENDPOINT.")

exercise_parameters = {
    "query": input("Tell me which exercises you did:")
}

exercise_response = requests.post(url="https://trackapi.nutritionix.com/v2/natural/exercise", json=exercise_parameters,
                                  headers=exercise_headers)
# print(exercise_response.status_code)
exercise_data = exercise_response.json()['exercises']


for i in range(0, len(exercise_data)):
    today = dt.datetime.now()

    workouts_parameters = {
        "workout": {
            "date": today.strftime("%d/%m/%Y"),
            "time": today.strftime("%X"),
            "exercise": exercise_data[i]["name"],
            "duration": round(exercise_data[i]["duration_min"]),
            "calories": round(exercise_data[i]["nf_calories"])
        }
    }

    sheety_adding_row = requests.post(
        url=SHEETY_POST_ENDPOINT,
        json=workouts_parameters,
        auth=HTTPBasicAuth(USERNAME, PASSWORD)
    )
    sheety_adding_row.raise_for_status()  # Raise an exception for HTTP errors
    print(f"Successfully posted to Sheety: {sheety_adding_row.status_code}")

