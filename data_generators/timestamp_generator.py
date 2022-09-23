import datetime
import pytz
import random


def performance_start_timestamp()->datetime.datetime:
    """
    Create the initial timestamp
    :return:
        2022-08-27 15:50:12.XXXXXX
    """
    return datetime.datetime(year=2022, month=8, day=27, hour=15, minute=50, second=12) + datetime.timedelta(microseconds=random.choice(range(100, 300000)))


def base_row_time(total_rows:int)->float:
    """
    calculate number of (sub) second between each timestamp value
    :args:
        total_rows:int - total number of rows to insert
    :params:
        rows_24h_increments:int - base number of rows over 24 hours for calculation
        second_increments:float - number of (sub) seconds between each row
    :return:
        increment of number of seconds between row
    """
    rows_24h_increments = 100000
    second_increments = 0.864

    return second_increments * (rows_24h_increments / total_rows)


def performance_timestamps(timestamp:datetime.datetime, base_row_time:float, row_counter:int)->str:
    """
    Calculate the current timestamp for row
    :args:
        timestamp:datetime.datetime - initial timestamp (performance_start_timestamp)
        base_row_time:float -  incremental seconds value (base_row_time)
        row_counter:int -- current row
    :params:
        seconds:float - calculate incremental seconds
    :return:
         timestamp + seconds (in string format)
    """
    seconds = base_row_time * row_counter
    timestamp =+ datetime.timedelta(seconds=seconds)
    return timestamp.strftime('%Y-%M-%DT%h:%m:%s.%fZ')


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
        if enable_timezone_range is true:
            timestamp += datetime.timedelta(days=random.choice(range(-30, 31)), hours=random.choice(range(-23, 24)),
                                            minutes=random.choice(range(-59, 60)))
        timestamp = timestamp.strftime('%y-%m-%dT%h:%m:%s.%fZ')
    else: # actual utc value
        timestamp = datetime.datetime.utcnow()
        if enable_timezone_range is true:
            timestamp += datetime.timedelta(days=random.choice(range(-30, 31)), hours=random.choice(range(-23, 24)),
                                            minutes=random.choice(range(-59, 60)))
        timestamp = timestamp.strftime('%y-%m-%dT%h:%m:%s.%fZ')

    return timestamp
