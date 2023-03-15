import folium
import json
from pokemon_entities.models import Pokemon, PokemonEntity
from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.utils.timezone import localtime


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    pokemons = PokemonEntity.objects.filter(appeared_at__lt=localtime(), disappeared_at__gt=localtime())
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon in pokemons:
        pokemon_img = Pokemon.objects.get(title=pokemon.pokemon).image
        add_pokemon(folium_map, pokemon.lat, pokemon.lon, request.build_absolute_uri(f'/media/{pokemon_img}'))

    pokemons_on_page = []
    pokemons_from_db = Pokemon.objects.all()
    for pokemon in pokemons_from_db:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': request.build_absolute_uri(f'/media/{pokemon.image}'),
            'title_ru': pokemon.title_ru,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    pokemons = Pokemon.objects.all()
    for pokemon in pokemons:
        if pokemon.id == int(pokemon_id):
            requested_pokemon = pokemon
            pokemon = {
                "pokemon_id": requested_pokemon.id,
                "title_ru": requested_pokemon.title_ru,
                "title_en": requested_pokemon.title_en,
                "title_jp": requested_pokemon.title_jp,
                "description": requested_pokemon.description,
                "img_url": request.build_absolute_uri(f'/media/{requested_pokemon.image}')
            }
            if requested_pokemon.previous_evolution:
                pokemon['previous_evolution'] = {
                    "title_ru": requested_pokemon.previous_evolution,
                    "pokemon_id": requested_pokemon.id,
                    "img_url": request.build_absolute_uri(f'/media/{requested_pokemon.previous_evolution.image}')
                }
            if requested_pokemon.next_evolution.first():
                next_pokemon = requested_pokemon.next_evolution.first()
                pokemon['next_evolution'] = {
                    "title_ru": next_pokemon.title_ru,
                    "pokemon_id": next_pokemon.id,
                    "img_url": request.build_absolute_uri(f'/media/{next_pokemon.image}')
                }
            break
    else:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemon_entities = PokemonEntity.objects.filter(appeared_at__lt=localtime(),
                                                    disappeared_at__gt=localtime(),
                                                    pokemon=requested_pokemon)
    for pokemon_entity in pokemon_entities:
        add_pokemon(folium_map,
                    pokemon_entity.lat,
                    pokemon_entity.lon,
                    request.build_absolute_uri(f'/media/{requested_pokemon.image}')
                    )

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon
    })
