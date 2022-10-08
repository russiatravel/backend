from flask import Flask, request
from pydantic import ValidationError

from backend.errors import AppError
from backend.places.schemas import Place
from backend.places.storages import LocalStorage

app = Flask(__name__)


def handle_app_error(err: AppError):
    return {'error': str(err)}, err.code


def handle_validation_error(err: ValidationError):
    return {'error': str(err)}, 400


app.register_error_handler(AppError, handle_app_error)
app.register_error_handler(ValidationError, handle_validation_error)

storage = LocalStorage()


@app.post('/api/places/')
def add():
    payload = request.json

    if not payload:
        raise AppError('empty payload')

    payload['uid'] = -1

    place = Place(**payload)

    place = storage.add(place)
    return place.dict(), 201


@app.get('/api/places/')
def get_all():
    places = storage.get_all()
    return [place.dict() for place in places], 200


@app.get('/api/places/<int:uid>')
def get_by_id(uid):
    place = storage.get_by_id(uid)

    return place.dict(), 200


@app.put('/api/places/<int:uid>')
def update_by_id(uid):
    payload = request.json

    if not payload:
        raise AppError('empty payload')

    payload['uid'] = uid
    place = Place(**payload)
    place = storage.update(uid, place)

    return place.dict(), 200


@app.delete('/api/places/<int:uid>')
def delete_place(uid):
    storage.delete(uid)

    return {}, 204
