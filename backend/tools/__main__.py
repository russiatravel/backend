import csv
from typing import Any
from backend.database import db_session
from backend.models import Place, City


def read_csv(filename: str) -> list[dict[str, Any]]:
    with open(filename, 'r', encoding='utf-8') as f:
        fields = ['city_name', 'place_name', 'place_description']
        reader = csv.DictReader(f, fields, delimiter=',')
        travels_data = []
        for row in reader:
            travels_data.append(row)
        return travels_data


def get_unique_cities(data):
    cities = {}
    for row in data:
        name = row['city_name']
        if name not in cities:
            city = {'name': name}
            cities[name] = city

    return cities


def save_cities(cities):
    db_session.bulk_insert_mappings(City, cities.values(), return_defaults=True)
    db_session.commit()


def get_unique_places(data, cities):
    places = {}

    for row in data:
        city_name = row['city_name']
        place_name = row['place_name']
        if place_name not in places:
            place = {
                "name": place_name,
                "description": row["place_description"],
                "city_id": cities[city_name]['uid']
            }
            places[place_name] = place

    return places


def save_places(places):
    db_session.bulk_insert_mappings(Place, places.values(), return_defaults=True)
    db_session.commit()


if __name__ == '__main__':
    all_data = read_csv('.data/result.csv')
    cities = get_unique_cities(all_data)
    save_cities(cities)

    places = get_unique_places(all_data, cities)
    save_places(places)
