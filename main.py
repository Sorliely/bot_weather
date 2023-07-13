from pprint import pprint
import datetime
import requests
from config import TOKEN


def get_weather(city, TOKEN):
    code_to_weather = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Олачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снего \U0001F328",
        "Mist": "Туман \U0001F32B"
    }
    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={TOKEN}&units=metric"
        )
        data = r.json()
        pprint(data)

        city = data["name"]
        cur_weather = data['main']['temp']
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        wind = data["wind"]['speed']
        time_sunrise = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        weather_description = data["weather"][0]["main"]
        """Если хоть одно условие совпадет с выдоваемым информации о погоде
        то мы выведем смайл, если нет то выведет исулючение"""
        if weather_description in code_to_weather:
            wb = code_to_weather[weather_description]
        else:
            wb = "Посмотри в окно, может там конец света))"

        print(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%m')}***\n"
              f"Погода в городе : {city}\nТемпература: {cur_weather}°C {wb}\nВлажность: {humidity}%\n"
              f"Давление: {pressure} мм.рт.ст\nСкорость ветра: {wind} м/с\n"
              f"Время рассвета: {time_sunrise}\n"
              f"Хорошего дня")

    except Exception as ex:
        print(ex)
        print("Проверьте название города")


def main():
    city = input('Введите город')
    get_weather(city, TOKEN)


if __name__ == '__main__':
    main()
