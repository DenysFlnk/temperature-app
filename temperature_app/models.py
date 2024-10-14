from django.db import models


class Worldcities(models.Model):
    id = models.TextField(primary_key=True)
    city = models.TextField(null=False)
    country = models.TextField(null=False)
    lat = models.FloatField(null=False)
    lng = models.FloatField(null=False)

    class Meta:
        managed = False
        db_table = 'worldcities'