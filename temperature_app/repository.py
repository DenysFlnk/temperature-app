from django.db.models import Q

from temperature_app.models import Worldcities


def get_city(lat: float, lng: float) -> Worldcities:
    return Worldcities.objects.filter(Q(lat__gte=lat - 0.01) & Q(lat__lte=lat + 0.01),
                                      Q(lng__gte=lng - 0.01) & Q(lng__lte=lng + 0.01)).first()


def get_random_city() -> Worldcities:
    return Worldcities.objects.order_by('?').first()