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


def generate_timestamp(timezone:str='utc', enable_timezone_range:bool=True)->str:
    """
    Generate timestamp based on timezone
    :args:
        timezone:str - timezone either UTC or other
        enable_timezone_range:bool - if set alter timestamp by datetime.timedelta(days=random.choice(range(-30, 31)),
                                                                                  hours=random.choice(range(-23, 24)),
                                                                                  minutes=random.choice(range(-59, 60)))
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
        timestamp = timestamp.astimezone(timezone)
        if enable_timezone_range is True:
            timestamp += datetime.timedelta(days=random.choice(range(-30, 31)), hours=random.choice(range(-23, 24)),
                                            minutes=random.choice(range(-59, 60)))
        timestamp = timestamp.astimezone(timezone).isoformat().replace('T', ' ')
    elif timezone == 'local': # current timestamp as "UTC"
        timestamp = datetime.datetime.now()
        if enable_timezone_range is True:
            timestamp += datetime.timedelta(days=random.choice(range(-30, 31)), hours=random.choice(range(-23, 24)),
                                            minutes=random.choice(range(-59, 60)))
        timestamp = timestamp.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    else: # actual UTC value
        timestamp = datetime.datetime.utcnow()
        if enable_timezone_range is True:
            timestamp += datetime.timedelta(days=random.choice(range(-30, 31)), hours=random.choice(range(-23, 24)),
                                            minutes=random.choice(range(-59, 60)))
        timestamp = timestamp.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

    return timestamp


def payload_conversions(payloads:dict, dbms:str, table:str)->list:
    """
    For POST & MQTT functions, convert the content to have complete dicts
    :args:
        payloads:dict - either a dictionary or list of content to be stored in database
        dbms:str - logical database name
        table:str - table name, if payloads is dict use keys as table name
    :params:
        update_payloads:list - list of updated payloads
    """
    updated_payloads = []
    if isinstance(payloads, dict):
        for table in payloads:
            for row in payloads[table]:
                row['dbms'] = dbms
                row['table'] = table
                updated_payloads.append(json_dumps(data=row))
    elif isinstance(payloads, list):
        for row in payloads:
            row['dbms'] = dbms
            row['table'] = table
            updated_payloads.append(json_dumps(data=row))

    return updated_payloads
