from flask import Flask, request
from typing import Any
from pydantic import BaseModel, ValidationError


app = Flask(__name__)

Json = dict[int, Any]

class Place(BaseModel):
    uid: int
    name: str
    description: str

class LocalStorage:
    def __init__(self):
        self.places: dict[int, Place] = {}
        self.last_uid = 0

    def add(self, place: Place) -> Place:
        self.last_uid += 1
        place.uid = self.last_uid
        self.places[self.last_uid] = place
        return place

    def get_all(self) -> list[Place]:
        return list(self.places.values())

    def get_by_id(self, uid:int) -> Place:
        return self.places[uid]

    def update(self, uid: int, place: Place) -> Place:
        self.places[uid] = place
        return place

    def delete(self, uid: int) -> None:
        self.places.pop(uid)

storage = LocalStorage()


@app.post('/api/places/')
def add():
    payload = request.json
    payload["uid"] = -1

    try:
        place = Place(**payload)
    except ValidationError as err:
        return {'error': str(err)}, 400

    place = storage.add(place)
    return place.dict(), 201


@app.get('/api/places/')
def get_all():
    return storage.get_all(), 200


@app.get('/api/places/<int:uid>')
def get_by_id(uid):
    try:
        place = storage.get_by_id(uid)
    except KeyError as err:
        return {'error': f'There is no uid {err} in database'}, 400

    return place.dict(), 200


@app.put('/api/places/<int:uid>')
def update_by_id(uid):
    payload = request.json

    try:
        storage.get_by_id(uid)
    except KeyError as err:
        return {'error': f'There is no uid {err} in database'}, 400

    payload['uid'] = uid

    try:
        place = Place(**payload)
    except ValidationError as err:
        return {'error': str(err)}, 400

    place = storage.update(uid, place)
    return place.dict(), 200


@app.delete('/api/places/<int:uid>')
def delete_place(uid):
    try:
        storage.delete(uid)
    except KeyError as err:
        return {'error': f'There is no uid {err} in database'}, 400

    return {}, 204
