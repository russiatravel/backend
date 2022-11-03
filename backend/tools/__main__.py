import csv
import os

from backend.database import db_session
from backend.models import Place, City

db_data = os.environ['DB_DATA']


def read_csv(filename):
    with open(filename, 'r', encoding= 'utf-8') as f:
        fields = ['city_name', 'place_name', 'place_description']
        reader = csv.DictReader(f, fields, delimiter=',')
        travels_data = []
        for row in reader:
            travels_data.append(row)
        return travels_data


def save_cities(data):
    processed = []
    unique_cities = []
    for row in data:
        if row['city_name'] not in processed:
            city = {"name": row["city_name"]}
            unique_cities.append(city)
            processed.append(city["name"])
    db_session.bulk_insert_mappings(City, unique_cities, return_defaults=True)
    db_session.commit()
    return unique_cities


def get_city_by_id(cities, city_name):
    for city in cities:
        if city["name"] == city_name:
            return city["uid"]


def save_places(data, cities):
    processed = []
    unique_places = []
    for row in data:
        if row["place_name"] not in processed:
            place = {"name": row["place_name"], "description": row["place_description"],
            "city_id": get_city_by_id(cities, row["city_name"])}
            unique_places.append(place)
            processed.append(place["name"])
    db_session.bulk_insert_mappings(Place, unique_places, return_defaults=True)
    db_session.commit()
    return unique_places


if __name__ == '__main__':
    all_data = read_csv(db_data)
    cities = save_cities(all_data)
    places = save_places(all_data, cities)
