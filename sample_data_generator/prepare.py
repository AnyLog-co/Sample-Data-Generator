import os.path
import random
import numpy as np

DATA_DIR = os.path.expanduser(os.path.expandvars('$HOME/Sample-Data-Generator/data/videos'))
OUTPUT = []

for fn in os.listdir(DATA_DIR):
    if 'A' in fn:
        car_count = random.random() * random.choice(list(range(30, 50)))
        avg_speed = random.random() * random.choice(list(range(0, 30)))

        if car_count < 30:
            car_count += random.choice(list(range(30, 50)))
        if avg_speed < 15:
            avg_speed += random.choice(list(range(10, 15)))

    else:
        car_count = random.random() * random.choice(list(range(1, 25)))
        avg_speed = random.random() * random.choice(list(range(45, 75)))

        if car_count < 5:
            car_count += random.choice(list(range(1, 25)))
        if avg_speed < 20:
            avg_speed += random.choice(list(range(45, 75)))

    OUTPUT.append({
        'video': fn if fn.endswith('.mp4') else f'{fn}.mp4',
        'car_count': int(car_count),
        "avg_speed": float(avg_speed)
    })


data_array = np.array([(item['video'], item['car_count'], item['avg_speed']) for item in OUTPUT],
                      dtype=[('video', 'U10'), ('car_count', int), ('avg_speed', float)])

np.savetxt('../data/models/cars.csv', data_array, delimiter=',', header='video,car_count,avg_speed', comments='', fmt='%s,%d,%f')


