from datetime import datetime

import geocoder
import requests
from django.db.models import Q
from django.http import HttpResponse
from django.template import loader

from temperature_app.models import Worldcities

TEMPERATURE_API_ENDPOINT = 'https://api.open-meteo.com/v1/forecast'
AIR_QUALITY_API_ENDPOINT = 'https://air-quality-api.open-meteo.com/v1/air-quality'


def temperature_here(request):
    location: list[str] = geocoder.ip('me').latlng
    temperature = get_temperature(location[0], location[1])

    world_city = get_city(float(location[0]), float(location[1]))
    context = {'country': world_city.country, 'city': world_city.city, 'temperature': temperature}
    template = loader.get_template('index.html')
    return HttpResponse(template.render(context, request))


def temperature_random(request):
    random_city = Worldcities.objects.order_by('?').first()
    temperature = get_temperature(random_city.lat, random_city.lng)

    context = {'country': random_city.country, 'city': random_city.city, 'temperature': temperature}
    template = loader.get_template('index.html')
    return HttpResponse(template.render(context, request))


def get_temperature(lat: str, lng: str) -> str:
    api_request = f'{TEMPERATURE_API_ENDPOINT}?latitude={lat}&longitude={lng}&hourly=temperature_2m'
    meteo_data = requests.get(api_request).json()
    hour = datetime.now().hour

    return meteo_data['hourly']['temperature_2m'][hour]


def get_air_quality(lat: str, lng: str) -> str:
    api_request = f'{AIR_QUALITY_API_ENDPOINT}?latitude={lat}&longitude={lng}&hourly=european_aqi'
    meteo_data = requests.get(api_request).json()
    hour = datetime.now().hour

    return meteo_data['hourly']['european_aqi'][hour]


def get_city(lat: float, lng: float) -> Worldcities:
    return Worldcities.objects.filter(Q(lat__gte=lat - 0.01) & Q(lat__lte=lat + 0.01),
                                      Q(lng__gte=lng - 0.01) & Q(lng__lte=lng + 0.01)).first()
