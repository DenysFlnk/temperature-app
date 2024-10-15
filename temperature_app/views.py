from datetime import datetime

import geocoder
import requests
from django.db.models import Q
from django.http import HttpResponse
from django.template import loader

from temperature_app.models import Worldcities

TEMPERATURE_API_ENDPOINT = 'https://api.open-meteo.com/v1/forecast'
AIR_QUALITY_API_ENDPOINT = 'https://air-quality-api.open-meteo.com/v1/air-quality'

POLLUTANT_DICT = {20: 'Good',
                  40: 'Fair',
                  60: 'Moderate',
                  80: 'Poor',
                  100: 'Very Poor',}


def temperature_here(request):
    location: list[str] = geocoder.ip('me').latlng
    world_city = get_city(float(location[0]), float(location[1]))

    temperature = get_temperature(location[0], location[1])
    air_quality_index = get_air_quality_index(location[0], location[1])
    air_quality_definition = get_air_quality_definition(air_quality_index)

    context = {'country': world_city.country,
               'city': world_city.city,
               'temperature': temperature,
               'air_quality_index': air_quality_index,
               'air_quality_definition': air_quality_definition}

    template = loader.get_template('index.html')
    return HttpResponse(template.render(context, request))


def temperature_random(request):
    random_city = Worldcities.objects.order_by('?').first()

    temperature = get_temperature(random_city.lat, random_city.lng)
    air_quality_index = get_air_quality_index(random_city.lat, random_city.lng)
    air_quality_definition = get_air_quality_definition(air_quality_index)

    context = {'country': random_city.country,
               'city': random_city.city,
               'temperature': temperature,
               'air_quality_index': air_quality_index,
               'air_quality_definition': air_quality_definition}

    template = loader.get_template('index.html')
    return HttpResponse(template.render(context, request))


def get_temperature(lat: str, lng: str) -> str:
    api_request = f'{TEMPERATURE_API_ENDPOINT}?latitude={lat}&longitude={lng}&hourly=temperature_2m'
    meteo_data = requests.get(api_request).json()
    hour = datetime.now().hour

    return meteo_data['hourly']['temperature_2m'][hour]


def get_air_quality_index(lat: str, lng: str) -> int:
    api_request = f'{AIR_QUALITY_API_ENDPOINT}?latitude={lat}&longitude={lng}&hourly=european_aqi'
    meteo_data = requests.get(api_request).json()
    hour = datetime.now().hour

    return meteo_data['hourly']['european_aqi'][hour]


def get_air_quality_definition(index: int) -> str:
    for range in POLLUTANT_DICT:
        if index <= range:
            return POLLUTANT_DICT[range]

    return 'Extremely poor'


def get_city(lat: float, lng: float) -> Worldcities:
    return Worldcities.objects.filter(Q(lat__gte=lat - 0.01) & Q(lat__lte=lat + 0.01),
                                      Q(lng__gte=lng - 0.01) & Q(lng__lte=lng + 0.01)).first()
