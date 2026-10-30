"""Pictures REST API. The lab intentionally keeps its data in memory."""
import json
from pathlib import Path
from threading import RLock
from flask import jsonify, request
from . import app

with (Path(__file__).parent / "data" / "pictures.json").open(encoding="utf-8") as source:
    data = json.load(source)
lock = RLock()
FIELDS = ("pic_url", "event_country", "event_state", "event_city", "event_date")


def valid_picture(payload):
    return (isinstance(payload, dict) and type(payload.get("id")) is int
            and payload["id"] > 0 and all(isinstance(payload.get(key), str)
            and payload[key].strip() for key in FIELDS))


@app.get("/health")
def health():
    return jsonify(status="OK"), 200


@app.get("/count")
def count():
    with lock:
        return jsonify(length=len(data)), 200


@app.get("/picture")
def get_pictures():
    with lock:
        return jsonify(data), 200


@app.get("/picture/<int:id>")
def get_picture_by_id(id):
    with lock:
        picture = next((p for p in data if p["id"] == id), None)
        if picture is None:
            return jsonify(message="picture not found"), 404
        return jsonify(picture), 200


@app.post("/picture")
def create_picture():
    payload = request.get_json(silent=True)
    if not valid_picture(payload):
        return jsonify(message="A positive integer id and all picture fields are required"), 400
    with lock:
        if any(p["id"] == payload["id"] for p in data):
            # Preserve the response required by the original course tests.
            return jsonify(Message=f"picture with id {payload['id']} already present"), 302
        picture = {key: payload[key] for key in ("id", *FIELDS)}
        data.append(picture)
        return jsonify(picture), 201


@app.put("/picture/<int:id>")
def update_picture(id):
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict) or payload.get("id", id) != id:
        return jsonify(message="Invalid picture or mismatched id"), 400
    with lock:
        picture = next((p for p in data if p["id"] == id), None)
        if picture is None:
            return jsonify(message="picture not found"), 404
        updated = {**picture, **{k: v for k, v in payload.items() if k in FIELDS}}
        if not valid_picture(updated):
            return jsonify(message="Picture fields must be non-empty strings"), 400
        picture.update(updated)
        return jsonify(picture), 200


@app.delete("/picture/<int:id>")
def delete_picture(id):
    with lock:
        for index, picture in enumerate(data):
            if picture["id"] == id:
                data.pop(index)
                return "", 204
        return jsonify(message="picture not found"), 404

