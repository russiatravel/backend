from flask import Flask, request

app = Flask(__name__)

places = []

@app.post('/api/places/')
def add():
    payload = request.json
    payload["uid"] = len(places)
    places.append(payload)
    return payload, 201

@app.get('/api/places/')
def get_all():
    return places, 200

@app.get('/api/places/<int:uid>')
def get_by_id(uid):
    return places[uid], 200

@app.put('/api/places/<int:uid>')
def update_by_id(uid):
    payload = request.json

    for key in payload:
        places[uid][key] = payload[key]

    return places[uid]

@app.delete('/api/places/<int:uid>')
def delete_place(uid):
    return places.pop(uid), 201
