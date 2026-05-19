#!/usr/bin/env python3
"""
Консольное приложение для получения текущей погоды через API OpenWeatherMap
"""

import requests
import json
import sys
import argparse
from datetime import datetime
from typing import Dict, Any


class WeatherApp:
    """Класс для взаимодействия с метеорологическим API"""
    
    # Бесплатный API ключ (ограниченный) - для теста. Рекомендуется свой.
    API_KEY = "bd5e378503939ddaee76f12ad7a97608"  # тестовый ключ, ограничен 60 запросов/мин
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or self.API_KEY
        self.session = requests.Session()
    
    def get_weather(self, city: str, units: str = "metric") -> Dict[str, Any]:
        """
        Получение данных о погоде для города
        
        Args:
            city: Название города
            units: Единицы измерения (metric - Цельсий, imperial - Фаренгейт)
        
        Returns:
            Словарь с данными о погоде
        """
        params = {
            "q": city,
            "appid": self.api_key,
            "units": units,
            "lang": "ru"  # русскоязычное описание
        }
        
        try:
            response = self.session.get(self.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Ошибка API: {e}")
    
    def format_output(self, data: Dict[str, Any], units: str = "metric") -> str:
        """Форматирование выходных данных"""
        city_name = data.get("name", "Неизвестно")
        country = data.get("sys", {}).get("country", "")
        temp = data.get("main", {}).get("temp")
        feels_like = data.get("main", {}).get("feels_like")
        humidity = data.get("main", {}).get("humidity")
        pressure = data.get("main", {}).get("pressure")
        wind_speed = data.get("wind", {}).get("speed")
        description = data.get("weather", [{}])[0].get("description", "")
        
        # Единицы измерения
        temp_unit = "°C" if units == "metric" else "°F"
        wind_unit = "м/с" if units == "metric" else "миль/ч"
        
        output = f"""
╔══════════════════════════════════════════════════════════════╗
║                    ТЕКУЩАЯ ПОГОДА                            ║
╠══════════════════════════════════════════════════════════════╣
║ Город: {city_name}, {country}
║ Время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
║
║ Температура:      {temp}{temp_unit} (ощущается как {feels_like}{temp_unit})
║ Влажность:        {humidity}%
║ Давление:         {pressure} гПа
║ Ветер:            {wind_speed} {wind_unit}
║
║ Описание:         {description.capitalize()}
╚══════════════════════════════════════════════════════════════╝
"""
        return output
    
    def run_cli(self):
        """Запуск интерфейса командной строки"""
        parser = argparse.ArgumentParser(
            description="Получение текущей погоды для города",
            formatter_class=argparse.RawDescriptionHelpFormatter
        )
        parser.add_argument("city", nargs="?", help="Название города")
        parser.add_argument("-u", "--units", choices=["metric", "imperial"], 
                           default="metric", help="Единицы измерения")
        parser.add_argument("-k", "--api-key", help="API ключ OpenWeatherMap")
        
        args = parser.parse_args()
        
        # Если город не указан в аргументах, запрашиваем интерактивно
        city = args.city
        if not city:
            city = input("Введите название города: ").strip()
            if not city:
                print("Ошибка: название города не может быть пустым")
                sys.exit(1)
        
        try:
            if args.api_key:
                self.api_key = args.api_key
            
            print(f"\nЗапрос погоды для города: {city}...")
            weather_data = self.get_weather(city, args.units)
            print(self.format_output(weather_data, args.units))
            
        except Exception as e:
            print(f"Ошибка: {e}")
            sys.exit(1)


def main():
    app = WeatherApp()
    app.run_cli()


if __name__ == "__main__":
    main()