from logging import exception
from flask import Flask, request
from pydantic import BaseModel, ValidationError


app = Flask(__name__)

class AppError(Exception):
    code = 500
    def __init__(self, reason: str) -> None:
        super().__init__(reason)
        self.reason = reason

class NotFoundError(AppError):
    code = 404
    def __init__(self, name: str, uid: int) -> None:
        super().__init__(f'{name} [{uid}] not found')
        self.name = name
        self.uid = uid

def handle_app_error(e: AppError):
    return {'error': str(e)}, e.code

def handle_validation_error(e: ValidationError):
    return {'error': str(e)}, 400

app.register_error_handler(AppError, handle_app_error)
app.register_error_handler(ValidationError, handle_validation_error)

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
        return [place.dict() for place in self.places.values()]

    def get_by_id(self, uid:int) -> Place:
        return self.places[uid]

    def update(self, uid: int, place: Place) -> Place:
        if uid not in self.places:
            raise NotFoundError('places', uid)

        self.places[uid] = place
        return place

    def delete(self, uid: int) -> None:
        self.places.pop(uid)


storage = LocalStorage()


@app.post('/api/places/')
def add():
    payload = request.json
    payload["uid"] = -1

    place = Place(**payload)

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
        return {'error': str(err)}, 404

    return place.dict(), 200


@app.put('/api/places/<int:uid>')
def update_by_id(uid):
    payload = request.json

    payload['uid'] = uid

    place = Place(**payload)

    place = storage.update(uid, place)

    return place.dict(), 200


@app.delete('/api/places/<int:uid>')
def delete_place(uid):
    try:
        storage.delete(uid)
    except KeyError as err:
        return {'error': str(err)}, 404

    return {}, 204
