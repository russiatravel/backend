from flask import Flask, request
from typing import Any

app = Flask(__name__)

Json = dict[int, Any]
class Storage:
    def __init__(self):

        self.places: dict[int, Json] = {}
        self.last_uid = 0

    def add(self, place: Json) -> Json:
        self.last_uid += 1
        place["uid"] = self.last_uid
        self.places[self.last_uid] = place
        return place

    def get_all(self) -> list[Json]:
        return list(self.places.values())

    def get_by_id(self, uid:int) -> Json:
        return self.places[uid]

    def update(self, uid: int, place: Json) -> Json:
        self.places[uid] = place
        return place

    def delete(self, uid: int) -> None:
        self.places.pop(uid)

storage = Storage()

@app.post('/api/places/')
def add():
    place = request.json
    return storage.add(place), 201

@app.get('/api/places/')
def get_all():
    return storage.get_all(), 200

@app.get('/api/places/<int:uid>')
def get_by_id(uid):
    return storage.get_by_id(uid), 200

@app.put('/api/places/<int:uid>')
def update_by_id(uid):
    place = request.json
    return storage.update(uid, place), 200

@app.delete('/api/places/<int:uid>')
def delete_place(uid):
    storage.delete(uid)
    return {}, 204
