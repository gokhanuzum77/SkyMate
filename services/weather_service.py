import requests
from models.weather import Weather


class WeatherService:
    def __init__(self, api_key):
        self.__api_key = api_key

    def get_weather(self, city_name):
        url = (
            f"https://api.openweathermap.org/data/2.5/weather"
            f"?q={city_name}&appid={self.__api_key}&units=metric&lang=tr"
        )

        response = requests.get(url)
        data = response.json()

        if data.get("cod") != 200:
            return None

        return Weather(
            city=data["name"],
            temp=str(int(data["main"]["temp"])) + "°C",
            desc=data["weather"][0]["description"].capitalize(),
            humidity="Nem: %" + str(data["main"]["humidity"]),
            wind="Rüzgar: " + str(data["wind"]["speed"]) + " m/s"
        )

    def get_forecast(self, city_name):
        url = (
            f"https://api.openweathermap.org/data/2.5/forecast"
            f"?q={city_name}&appid={self.__api_key}&units=metric&lang=tr"
        )

        response = requests.get(url)
        data = response.json()

        if data.get("cod") != "200":
            return []

        forecast_list = []
        used_dates = []

        for item in data["list"]:
            date_text = item["dt_txt"].split(" ")[0]
            hour_text = item["dt_txt"].split(" ")[1]

            if date_text not in used_dates and hour_text == "12:00:00":
                temp = int(item["main"]["temp"])
                desc = item["weather"][0]["description"].capitalize()

                forecast_list.append({
                    "date": date_text,
                    "temp": temp,
                    "desc": desc
                })

                used_dates.append(date_text)

            if len(forecast_list) == 5:
                break

        return forecast_list