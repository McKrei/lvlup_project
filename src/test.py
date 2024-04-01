import aiohttp
import asyncio

async def get_weather(city: str, country: str) -> str:
    api_key = "ec8459e3a3dd4544bd691405240104"  # Ваш API ключ от WeatherAPI
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city} {country}&lang=ru"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()

            if response.status == 200:
                # Собираем информацию о погоде
                temp_c = data['current']['temp_c']
                condition_text = data['current']['condition']['text']
                humidity = data['current']['humidity']

                weather_info = (f"Погода в {city}, {country}: {condition_text}. "
                                f"Температура: {temp_c}°C, Влажность: {humidity}%.")
                return weather_info
            else:
                return "Ошибка при получении данных о погоде."


# Пример использования функции

async def main():
    city = "москва"
    country = "россия"
    weather_info = await get_weather(city, country)
    print(weather_info)

asyncio.run(main())
