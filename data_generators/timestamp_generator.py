import datetime
try:
    import pytz
except:
    pass
else:
    TIMEZONES = {
        'et': pytz.timezone('africa/addis_ababa'),  # +03:00 (africa)
        'br': pytz.timezone('america/fortaleza'),  # -03:00 (s. america)
        'jp': pytz.timezone('asia/tokyo'),  # +09:00 (asia)
        'ws': pytz.timezone('us/pacific'),  # -09:00 (n. america)
        'au': pytz.timezone('australia/north'),  # +09:30 (australia)
        'it': pytz.timezone('europe/rome'),  # +01:00 (europe)
    }

import random


def __generate_timestamp(timezone:str='utc', enable_timezone_range:bool=True)->datetime.datetime:
    """
    generate timestamp based on timezone
    :args:
        timezone:str - timezone either utc or other
        enable_timezone_range:bool - if set alter timestamp by datetime.timedelta(days=random.choice(range(-30, 31)),
                                                                                  hours=random.choice(range(-23, 24)),
                                                                                  minutes=random.choice(range(-59, 60)))
    :params:
        timestamp:str - generated timestamp
    :return:
        timestamp
    """
    timestamp = datetime.datetime.now(datetime.timezone.utc)

    if timezone in TIMEZONES: # selected timezone
        timezone = TIMEZONES[timezone]
        timestamp = timestamp.astimezone(timezone)
        if enable_timezone_range is True:
            timestamp += datetime.timedelta(days=random.choice(range(-30, 31)), hours=random.choice(range(-23, 24)),
                                            minutes=random.choice(range(-59, 60)))
        timestamp = timestamp.astimezone(timezone).isoformat().replace('t', ' ')
    elif timezone == 'local': # current timestamp as "utc"
        timestamp = datetime.datetime.now()
        if enable_timezone_range is True:
            timestamp += datetime.timedelta(days=random.choice(range(-30, 31)), hours=random.choice(range(-23, 24)),
                                            minutes=random.choice(range(-59, 60)))
    else: # actual utc value
        timestamp = datetime.datetime.utcnow()
        if enable_timezone_range is True:
            timestamp += datetime.timedelta(days=random.choice(range(-30, 31)), hours=random.choice(range(-23, 24)),
                                            minutes=random.choice(range(-59, 60)))

    return timestamp


def __timestamp_string(timestamp:datetime.datetime)->str:
    """
    Convert timestamp to string
    :args:
        timestamp:datetime.datetime - timestamp
    :return:
        timestamp as string format
    """
    try:
        timestamp = timestamp.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    except Exception as error:
        pass

    return timestamp


def generate_timestamp(timezone:str='utc', enable_timezone_range:bool=True)->str:
    """
    generate timestamp based on timezone
    :args:
        timezone:str - timezone either utc or other
        enable_timezone_range:bool - if set alter timestamp by datetime.timedelta(days=random.choice(range(-30, 31)),
                                                                                  hours=random.choice(range(-23, 24)),
                                                                                  minutes=random.choice(range(-59, 60)))
    :params:
        timestamp:str - generated timestamp
    :return:
        timestamp
    """
    timestamp = __generate_timestamp(timezone=timezone, enable_timezone_range=enable_timezone_range)
    return __timestamp_string(timestamp=timestamp)


def generate_timestamps_range(timezone:str, enable_timezone_range:bool=False, period:float=None)->(datetime.datetime, datetime.datetime):
    """
    Generate 2 timestamps that are 5 to 90 seconds apart - used in car_images data generator
    :params:
        timestamp:datetime.datetime - current timestamp
        timestamp2:datetime.datetime - current timestamp + 5 to 90 seconds into the future
        period:float - seconds to increase by
    :return: 
        timestamp, timestamp2
    """
    timestamp = __generate_timestamp(timezone=timezone, enable_timezone_range=enable_timezone_range)
    timestamp2 = timestamp + datetime.timedelta(seconds=random.choice(range(5, 90)))
    if period is not None:
        timestamp2 = timestamp + datetime.timedelta(seconds=period)
    
    return __timestamp_string(timestamp), __timestamp_string(timestamp2)


def performance_timestamp(payload:dict, total_rows:int, current_row:int=0, timezone:str=None, enable_timezone_range:bool=False):
    """
    timestamp(s) generated between 2023-06-06 00:00:00 and 2023-06-07 00:00:00
        Option 1: enable_timezone_range is False -- based on the current_row, calculate the current timestamp
        Option 2: enable_timezone_range is True -- generate a list of timestamps, and shuffle them
    :args:
        payload:dict - current row to update (used in option 1)
        total_rows:int - total number of rows
        current_row:int - current row [number] currently generated (used as a param in option 2)
        timezone:str - timezone
        enable_timezone_range:bool - whether to enable option 2 or not
    :params:
        tzinfo:pytz.timezone - timezone
        strt_timestamp:datetime.datetime - start timestamp (2023-06-06 00:00:00)
        end_timestamp:datetime.datetime - end timestamp (2023-06-07 00:00:00)
        time_interval:float - time interval
        timestamps:list - list of timestamps (used for option 2)
        timestamp:datetime.datetime - generated timestamp
    :return:
        options 1: payload with timestamp
        option 2: timestamps in randomized order
    """
    tzinfo = None
    if TIMEZONES and timezone in TIMEZONES:
        tzinfo = TIMEZONES[timezone]

    strt_timestamp = datetime.datetime(year=2023, month=6, day=6, hour=0, minute=0, second=0, microsecond=0, tzinfo=tzinfo)
    end_timestamp = datetime.datetime(year=2023, month=6, day=7, hour=0, minute=0, second=0, microsecond=0, tzinfo=tzinfo)
    time_interval = (end_timestamp - strt_timestamp) / total_rows

    if enable_timezone_range is True:
        timestamps = []
        for current_row in range(total_rows):
            timestamp = strt_timestamp + (current_row * time_interval)
            timestamps.append(__timestamp_string(timestamp=timestamp))
        random.shuffle(timestamps)
        return timestamps
    else:
        timestamp = strt_timestamp + (current_row * time_interval)
        timestamp = __timestamp_string(timestamp=timestamp)
        if isinstance(payload, list):
            for pyld in payload:
                pyld['timestamp'] = timestamp
        else:
            payload['timestamp'] = timestamp
        return payload

def include_timestamp(payload:dict, timezone:str='utc', enable_timezone_range:bool=False):
    """
    Generate timestamp for row - if performance testing is enabled, timestamps within will be within a 24 hour period.
    :args:
       payload:dict - row(s) to add timestamp for
       timezone:str - timezone for generated timestamp(s)
       enable_timezone_range:bool - whether or not to set timestamp within a "range"
       performance_testing:bool - insert all rows within a 24 hour period (if enabled, timezone params are ignored)
       base_timestamp:datetime.datetime - initial timestamp for performance testing
       base_row_time:float - timestamp incremental value for performance testing
       row_counter:int - current row -- ueed in calculating timestamp for performance
    :params:
        timestamp:str - calculated timestamp (as string)
    :return:
        updated payload
    """
    timestamp = generate_timestamp(timezone=timezone, enable_timezone_range=enable_timezone_range)
    if isinstance(payload, dict):
        payload['timestamp'] = timestamp
    else:
        for i in range(len(payload)):
            payload[i]['timestamp'] = timestamp

    return payload