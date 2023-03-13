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
            'title_ru': pokemon.title,
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
                "title_ru": requested_pokemon.title,
                "title_en": "Bulbasaur",
                "title_jp": "フシギダネ",
                "description": "cтартовый покемон двойного травяного и ядовитого типа из первого поколения и региона "
                               "Канто. В национальном покедексе под номером 1. На 16 уровне эволюционирует в "
                               "Ивизавра. Ивизавр на 32 уровне эволюционирует в Венузавра. Наряду с Чармандером и "
                               "Сквиртлом, Бульбазавр является одним из трёх стартовых покемонов региона Канто.",
                "img_url": request.build_absolute_uri(f'/media/{requested_pokemon.image}'),
                "next_evolution": {
                    "title_ru": "Ивизавр",
                    "pokemon_id": 2,
                    "img_url": "https://vignette.wikia.nocookie.net/pokemon/images/7/73/002Ivysaur.png/revision"
                               "/latest/scale-to-width-down/200?cb=20150703180624&path-prefix=ru "
                }
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
