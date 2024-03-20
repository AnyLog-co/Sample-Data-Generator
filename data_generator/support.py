import datetime
import json


def create_timestamp():
    return datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')


def serialize_data(payload):
    return json.dumps(payload)