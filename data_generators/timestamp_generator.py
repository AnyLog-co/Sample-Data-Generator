import datetime
import pytz
import random


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

def performance_timestamp(microseconds:int, second_increments:float)->str:
    """
    Calculate timestamp for performance testing
    :args:
        microseconds:str - base microseconds (calculated as global value)
        second_increments:str - how much to increment by
    :params:
       timestamp:datetime.datetime - calculated timestamp
    :return:
         timestamp as string
    """
    # calculate the base timestamp
    timestamp = datetime.datetime(year=2022, month=8, day=27, hour=15, minute=50, second=12) + datetime.timedelta(microseconds=microseconds)
    
    # update based on second_increments
    timestamp += datetime.timedelta(seconds=second_increments)
    
    return __timestamp_string(timestamp=timestamp)


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
    timestamp = datetime.datetime.now(datetime.timezone.utc)

    timezones = {
        'et': pytz.timezone('africa/addis_ababa'), # +03:00 (africa)
        'br': pytz.timezone('america/fortaleza'),  # -03:00 (s. america)
        'jp': pytz.timezone('asia/tokyo'),         # +09:00 (asia)
        'ws': pytz.timezone('us/pacific'),         # -09:00 (n. america)
        'au': pytz.timezone('australia/north'),    # +09:30 (australia)
        'it': pytz.timezone('europe/rome'),        # +01:00 (europe)
    }

    if timezone in timezones: # selected timezone
        timezone = timezones[timezone]
        timestamp = timestamp.astimezone(timezone)
        if enable_timezone_range is true:
            timestamp += datetime.timedelta(days=random.choice(range(-30, 31)), hours=random.choice(range(-23, 24)),
                                            minutes=random.choice(range(-59, 60)))
        timestamp = timestamp.astimezone(timezone).isoformat().replace('t', ' ')
    elif timezone == 'local': # current timestamp as "utc"
        timestamp = datetime.datetime.now()
        if enable_timezone_range is True:
            timestamp += datetime.timedelta(days=random.choice(range(-30, 31)), hours=random.choice(range(-23, 24)),
                                            minutes=random.choice(range(-59, 60)))
        timestamp = timestamp.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    else: # actual utc value
        timestamp = datetime.datetime.utcnow()
        if enable_timezone_range is True:
            timestamp += datetime.timedelta(days=random.choice(range(-30, 31)), hours=random.choice(range(-23, 24)),
                                            minutes=random.choice(range(-59, 60)))
        timestamp = timestamp.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

    return __timestamp_string(timestamp=timestamp)


def cars_timestamps()->(datetime.datetime, datetime.datetime):
    """
    Generate 2 timestamps that are 5 to 90 seconds apart - used in car_images data generator
    :params:
        timestamp:datetime.datetime - current timestamp
        timestamp2:datetime.datetime - current timestamp + 5 to 90 seconds into the future 
    :return: 
        timestamp, timestamp2
    """
    timestamp = datetime.datetime.utcnow()
    timestamp2 = timestamp + datetime.timedelta(seconds=random.choice(range(5, 90)))
    
    return timestamp, timestamp2
