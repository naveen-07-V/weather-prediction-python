
import requests

city = input("Enter city name: ")

url = "https://geocoding-api.open-meteo.com/v1/search"
params = {"name": city, "count": 1, "language": "en", "format": "json"}

try:
    r = requests.get(url, params=params, timeout=15)
    r.raise_for_status()
    places = r.json().get("results", [])

    if not places:
        print("City not found!")
    else:
        place = places[0]
        lat = place["latitude"]
        lon = place["longitude"]

        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "current": "temperature_2m,relative_humidity_2m,wind_speed_10m",
            "hourly": "precipitation_probability",
            "forecast_days": 1,
            "timezone": "auto"
        }

        r = requests.get(url, params=params, timeout=15)
        r.raise_for_status()
        data = r.json()

        current = data["current"]
        rain = data["hourly"]["precipitation_probability"]

        print("\n--- WEATHER REPORT ---")
        print("City:", place["name"])
        print("Temperature:", current["temperature_2m"], "C")
        print("Humidity:", current["relative_humidity_2m"], "%")
        print("Wind Speed:", current["wind_speed_10m"], "km/h")
        print("Next Hour Rain Probability:", rain[0], "%")
	
except requests.RequestException as e:
    print("Network error:", e)
