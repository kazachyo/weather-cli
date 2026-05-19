# Weather CLI App

Консольное приложение для получения текущей погоды через OpenWeatherMap API.

## Установка

```bash
# Клонирование репозитория
git clone https://github.com/kazachyo/weather-cli.git
cd weather-cli

# Установка зависимостей
pip install -r requirements.txt


# Базовый запрос
python weather_cli.py Москва

# С указанием единиц измерения (metric/imperial)
python weather_cli.py London -u imperial

# Интерактивный режим (без аргументов)
python weather_cli.py

# Со своим API ключом
python weather_cli.py Paris -k YOUR_API_KEY