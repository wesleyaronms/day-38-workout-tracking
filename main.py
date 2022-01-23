from datetime import datetime
import requests
import os


APP_ID = os.getenv("WORKOUT_TRACKING_NUTRITIONIX_APP_ID")
API_KEY = os.getenv("WORKOUT_TRACKING_NUTRITIONIX_API_KEY")
SHEET_AUTH = os.getenv("SHEET_AUTH")
MY_SHEET_ENDPOINT = os.getenv("MY_SHEET_ENDPOINT")

GENDER = "male"
WEIGHT = 80
HEIGHT = 1.93
AGE = 26

user_input_query = input("Tell me which exercises you did: ")

header = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}
nat_exercises_params = {
    "query": user_input_query,
    "gender": GENDER,
    "weight_kg": WEIGHT,
    "height_cm": HEIGHT,
    "age": AGE,
}

nat_exercises_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
response = requests.post(url=nat_exercises_endpoint, json=nat_exercises_params, headers=header)
response.raise_for_status()
exercises_data = response.json()

for num_exercises_input in range(len(exercises_data["exercises"])):

    exercise_type = exercises_data["exercises"][num_exercises_input]["name"].title()
    exercise_duration = exercises_data["exercises"][num_exercises_input]["duration_min"]
    calories = exercises_data["exercises"][num_exercises_input]["nf_calories"]

    header = {
        "Authorization": SHEET_AUTH
    }
    sheet_new_row = {
        "workout": {
            "date": datetime.now().strftime("%d/%m/%Y"),
            "time": datetime.now().strftime("%X"),
            "exercise": exercise_type,
            "duration": exercise_duration,
            "calories": calories,
        }
    }

    sheety_endpoint = f"https://api.sheety.co/{MY_SHEET_ENDPOINT}"
    response = requests.post(url=sheety_endpoint, json=sheet_new_row, headers=header)
    response.raise_for_status()

