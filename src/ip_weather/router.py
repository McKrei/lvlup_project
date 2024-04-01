import aiohttp
import asyncio
from fastapi import Depends, HTTPException, APIRouter
from starlette.requests import Request


router = APIRouter(prefix="/weather", tags=["weather"])


async def get_weather(city: str, country: str) -> str:
    api_key = "ec8459e3a3dd4544bd691405240104"  # Ваш API ключ от WeatherAPI
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city} {country}&lang=ru"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            # Собираем информацию о погоде
            temp_c = data["current"]["temp_c"]
            condition_text = data["current"]["condition"]["text"]
            humidity = data["current"]["humidity"]

            weather_info = (
                f"Погода в {city}, {country}: {condition_text}. "
                f"Температура: {temp_c}°C, Влажность: {humidity}%."
            )
            return weather_info


async def get_area_by_ip(ip_address):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"http://ip-api.com/json/{ip_address}") as response:
            data = await response.json()
        # Проверяем статус ответа
        if data["status"] == "success":
            return (
                data["city"],
                data["countryCode"],
            )  # Возвращаем название города и страны
        else:
            return "Город не найден или ошибка запроса", None


async def get_ip_address(request: Request) -> str:
    client_host = request.client.host
    return client_host


@router.get("/weather")
async def read_weather(request: Request):
    ip = request.client.host
    city, country = await get_area_by_ip(ip)
    weather_info = await get_weather(city, country)
    return {"weather_info": weather_info}


async def get_city_country(ip: str = Depends(get_ip_address)):
    return await get_area_by_ip(ip)


async def dependency_get_weather(
    city_country: tuple[str, str] = Depends(get_city_country)
):
    city, country = city_country
    return await get_weather(city, country)


# async def dependency_get_weather(ip: str = Depends(get_ip_address)):
#     city, country = await get_area_by_ip(ip)
#     if country is None:
#         raise HTTPException(status_code=404, detail=f"Город не найден, ваш IP {ip}")
#     return await get_weather(city, country)


@router.get("/weather")
async def read_weather(
    weather: str = Depends(dependency_get_weather),
    city_country: tuple[str, str] = Depends(get_city_country),
    ip: str = Depends(get_ip_address),
):
    return {
        "weather_info": weather,
        "city": city_country[0],
        "country": city_country[1],
        "ip": ip,
    }
