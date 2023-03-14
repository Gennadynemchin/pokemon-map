from django.db import models


class Pokemon(models.Model):
    title_ru = models.CharField(max_length=200, blank=True)
    title_en = models.CharField(max_length=200, blank=True)
    title_jp = models.CharField(max_length=200, blank=True)
    image = models.ImageField(null=True, blank=True)
    description = models.TextField(default='Pokemon description coming soon', blank=True)
    previous_evolution = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.title_en}'


class PokemonEntity(models.Model):
    lat = models.FloatField()
    lon = models.FloatField()
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    appeared_at = models.DateTimeField(null=True, blank=True)
    disappeared_at = models.DateTimeField(null=True, blank=True)
    level = models.IntegerField(null=True, blank=True)
    health = models.IntegerField(null=True, blank=True)
    strength = models.IntegerField(null=True, blank=True)
    defence = models.IntegerField(null=True, blank=True)
    stamina = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.pokemon}, {self.lat}, {self.lon}, {self.appeared_at}, {self.disappeared_at}'
