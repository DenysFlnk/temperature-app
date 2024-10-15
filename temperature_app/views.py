import geocoder
from django.http import HttpResponse
from django.template import loader

from temperature_app import meteo_service, repository


def temperature_here(request):
    location: list[str] = geocoder.ip('me').latlng
    world_city = repository.get_city(float(location[0]), float(location[1]))

    temperature = meteo_service.get_temperature(location[0], location[1])
    air_quality_index = meteo_service.get_air_quality_index(location[0], location[1])
    air_quality_definition = meteo_service.get_air_quality_definition(air_quality_index)

    context = {'country': world_city.country,
               'city': world_city.city,
               'temperature': temperature,
               'air_quality_index': air_quality_index,
               'air_quality_definition': air_quality_definition}

    template = loader.get_template('index.html')
    return HttpResponse(template.render(context, request))


def temperature_random(request):
    random_city = repository.get_random_city()

    temperature = meteo_service.get_temperature(random_city.lat, random_city.lng)
    air_quality_index = meteo_service.get_air_quality_index(random_city.lat, random_city.lng)
    air_quality_definition = meteo_service.get_air_quality_definition(air_quality_index)

    context = {'country': random_city.country,
               'city': random_city.city,
               'temperature': temperature,
               'air_quality_index': air_quality_index,
               'air_quality_definition': air_quality_definition}

    template = loader.get_template('index.html')
    return HttpResponse(template.render(context, request))
