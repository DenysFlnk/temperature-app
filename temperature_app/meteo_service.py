from datetime import datetime

import requests


TEMPERATURE_API_ENDPOINT = 'https://api.open-meteo.com/v1/forecast'
AIR_QUALITY_API_ENDPOINT = 'https://air-quality-api.open-meteo.com/v1/air-quality'

HOURLY = 'hourly'
TEMPERATURE_2M = 'temperature_2m'
EUROPEAN_AQI = 'european_aqi'
EXTREMELY_POOR = 'Extremely poor'

POLLUTANT_DICT = {20: 'Good',
                  40: 'Fair',
                  60: 'Moderate',
                  80: 'Poor',
                  100: 'Very Poor'}


def get_temperature(lat, lng) -> float:
    api_request = f'{TEMPERATURE_API_ENDPOINT}?latitude={lat}&longitude={lng}&hourly=temperature_2m'
    meteo_data = requests.get(api_request).json()
    hour = datetime.now().hour

    return meteo_data[HOURLY][TEMPERATURE_2M][hour]


def get_air_quality_index(lat, lng) -> int:
    api_request = f'{AIR_QUALITY_API_ENDPOINT}?latitude={lat}&longitude={lng}&hourly=european_aqi'
    meteo_data = requests.get(api_request).json()
    hour = datetime.now().hour

    return meteo_data[HOURLY][EUROPEAN_AQI][hour]


def get_air_quality_definition(index: int) -> str:
    for range in POLLUTANT_DICT:
        if index <= range:
            return POLLUTANT_DICT[range]

    return EXTREMELY_POOR
