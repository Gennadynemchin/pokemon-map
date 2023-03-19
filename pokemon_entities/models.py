from django.db import models


class Pokemon(models.Model):
    title_ru = models.CharField(max_length=200, verbose_name='название на русском')
    title_en = models.CharField(max_length=200, null=True, blank=True, verbose_name='название на английском')
    title_jp = models.CharField(max_length=200, null=True, blank=True, verbose_name='название на японском')
    image = models.ImageField(null=True, blank=True, verbose_name='изображение')
    description = models.TextField(default='Pokemon description coming soon', blank=True, verbose_name='описание')
    previous_evolution = models.ForeignKey("self",
                                           related_name="next_evolutions",
                                           null=True,
                                           blank=True,
                                           on_delete=models.SET_NULL, verbose_name='предыдущий класс покемона')

    def __str__(self):
        return self.title_en


class PokemonEntity(models.Model):
    lat = models.FloatField(verbose_name='широта')
    lon = models.FloatField(verbose_name='долгота')
    pokemon = models.ForeignKey(Pokemon,
                                on_delete=models.PROTECT,
                                related_name='entities',
                                verbose_name='отношение к покемону')
    appeared_at = models.DateTimeField(null=True, blank=True, verbose_name='время появления на карте')
    disappeared_at = models.DateTimeField(null=True, blank=True, verbose_name='время исчезновения с карты')
    level = models.IntegerField(null=True, blank=True, verbose_name='уровень')
    health = models.IntegerField(null=True, blank=True, verbose_name='здоровье')
    strength = models.IntegerField(null=True, blank=True, verbose_name='сила')
    defence = models.IntegerField(null=True, blank=True, verbose_name='защита')
    stamina = models.IntegerField(null=True, blank=True, verbose_name='выносливость')

    def __str__(self):
        return f'{self.pokemon}, {self.lat}, {self.lon}, {self.appeared_at}, {self.disappeared_at}'
