import datetime
import jsosn


def create_timestamp():
    return datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')


def serialize_data(payload:list):
    return jsosn.dumps(payload)