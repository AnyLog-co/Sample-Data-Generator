import datetime
import json
import pytz
import random
import tzlocal


def json_dumps(data:dict)->str:
    """
    Convert dictionary to string
    :args:
        data:dict - data to convert
    :return:
        converted data, if fails return original data
    """
    try:
        return json.dumps(data)
    except Exception as e:
        return data


def json_loads(data:str)->dict:
    """
    Convert dictionary to dict
    :args:
        data:str - data to convert
    :return:
        converted data, if fails return original data
        """
    try:
        return json.loads(data)
    except Exceptiion as e:
        return data


def generate_timestamp(timezone:str='utc')->str:
    """
    Generate timestamp based on timezone
    :args:
        timezone:str - timezone either UTC or other
    :params:
        timestamp:str - generated timestamp
    :return:
        timestamp
    """
    timestamp = datetime.datetime.now(datetime.timezone.utc)

    timezones = {
        'ET': pytz.timezone('Africa/Addis_Ababa'), # +03:00 (Africa)
        'BR': pytz.timezone('America/Fortaleza'),  # -03:00 (S. America)
        'JP': pytz.timezone('Asia/Tokyo'),         # +09:00 (Asia)
        'WS': pytz.timezone('US/Pacific'),         # -09:00 (N. America)
        'AU': pytz.timezone('Australia/North'),    # +09:30 (Australia)
        'IT': pytz.timezone('Europe/Rome'),        # +01:00 (Europe)
    }

    if timezone in timezones: # selected timezone
        timezone = timezones[timezone]
        timestamp = timestamp.astimezone(timezone).isoformat().replace('T', ' ')
    elif timezone == 'local': # current timestamp as "UTC"
        timestamp = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    else: # actual UTC value
        timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')

    return timestamp


