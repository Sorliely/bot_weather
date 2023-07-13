from aiogram import Bot, Dispatcher, executor,types
import requests
import datetime
from config import *


bot = Bot(TOKEN_API)
dp = Dispatcher(bot)

async def on_startup(_):
    print('Бот запущен')

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply("Привет! Напиши название города и я пришлю сводку погоды")

@dp.message_handler()
async def get_weather(message: types.Message):
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
            f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={TOKEN}&units=metric"
        )
        data = r.json()


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

        await message.reply(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%m')}***\n"
              f"Погода в городе : {city}\nТемпература: {cur_weather}°C {wb}\nВлажность: {humidity}%\n"
              f"Давление: {pressure} мм.рт.ст\nСкорость ветра: {wind} м/с\n"
              f"Время рассвета: {time_sunrise}\n"
              f"Хорошего дня")

    except:
        await message.reply("\U00002620 Проверьте название города \U00002620")

if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)

