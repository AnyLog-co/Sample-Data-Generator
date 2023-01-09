import random
import timestamp_generator


def car_counter(timezone:str, enable_timezone_range:bool=False) -> dict:
    """
    Generate car insight information
    :params:
        start_ts:datetime.datetime - UTC current timestamp
        end_ts:datetime.datetime - current timestamp + 5 to 90 seconds into the future
        hours:int - hour based on start_ts
        cars:int - number of cars passed at a given hour
        speed:float - avg car speed
    :return:
        dictionary object of
            - start_ts
            - end_ts
            - cars
            - speed
    """
    start_ts, end_ts = timestamp_generator.cars_timestamps(timezone=timezone, enable_timezone_range=enable_timezone_range)
    hours = start_ts.hour

    if 5 <= hours < 7:
        speed = round(random.choice(range(60, 80)) + random.random(), 2)
        cars = int(random.choice(range(10, 30)))
    elif 7 <= hours < 10:
        speed = round(random.choice(range(45, 65)) - random.random(), 2)
        cars = int(random.choice(range(40, 60)))
    elif 10 <= hours < 16:
        cars = int(random.choice(range(5, 20)))
        speed = round(random.choice(range(60, 80)) + random.random(), 2)
    elif 16 <= hours < 20:
        speed = round(random.choice(range(45, 65)) - random.random(), 2)
        cars = int(random.choice(range(40, 60)))
    elif 20 <= hours < 23:
        cars = int(random.choice(range(5, 20)))
        speed = round(random.choice(range(60, 80)) + random.random(), 2)
    else:  # 23:00 to 5:00
        cars = int(random.choice(range(0, 15)))
        speed = round(random.choice(range(60, 80)) + random.random(), 2)
    if cars == 0:
        speed = 0

    return {
        'start_ts': timestamp_generator.__timestamp_string(timestamp=start_ts),
        'end_ts': timestamp_generator.__timestamp_string(timestamp=end_ts),
        'cars': cars,
        'speed': speed
    }
