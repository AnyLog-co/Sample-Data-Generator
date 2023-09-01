import os
import time
import random

from video_processing import VideoProcessing

ROOT_PATH = os.path.dirname(os.path.expanduser(os.path.expanduser(os.path.abspath(__file__))))
# CAR_MODEL_FILE = os.path.join(ROOT_PATH, 'models', 'model_float.tflite')
# PERSON_MODEL_FILE =

FILES = {'person': {'content': os.path.expanduser(os.path.expandvars('$HOME/Downloads/sample_data/edgex-demo')),
                    'model': os.path.join(ROOT_PATH, 'models', 'people.tflite')
                    },
         'vehicle': {'content': os.path.expanduser(os.path.expandvars('$HOME/Downloads/sample_data/videos')),
                     'model': os.path.join(ROOT_PATH, 'models', 'model_float.tflite')
                     },
        }


def __person_video(file_path:str, model_file:str):
    start_time = time.time()
    vp = VideoProcessing(model_file=model_file, video=file_path, labels=["0 person"],  exception=True)
    if vp.status is True:
        vp.set_interpreter()
    if vp.status is True:
        vp.analyze_data(min_confidence=0.5)
    return time.time() - start_time, vp.get_values()


def __vehicle_video(file_path:str, model_file:str):
    total_time = 0
    confidence = 0.25
    num_cars = {}
    avg_speed = {}

    if 'B' in file_path:
        confidence = 0.1
    for label in ["car", "truck", "bus"]:
        start_time = time.time()
        vp = VideoProcessing(model_file=model_file, labels=[f"0 {label}"], img_process='vehicle', video=file_path, exception=True)
        if vp.status is True:
            vp.set_interpreter()
        if vp.status is True:
            vp.process_video(min_confidence=confidence)
            total_time += time.time() - start_time
            cars, speed = vp.get_values()
            num_cars[label] = cars
            avg_speed[label] = speed
    if 'A.mp4':
        total_cars = int(sum(num_cars.values()))
    else:
        total_cars = int(sum(num_cars.values()) / len(num_cars))
    avg_speed = sum(avg_speed.values())/len(avg_speed)
    return total_time, total_cars, avg_speed


def main():
    for i in range(10):
        # select img_type and file
        img_type = random.choice(list(FILES))
        file = ""
        while "mp4" not in file:
            file = random.choice(os.listdir(FILES[img_type]['content']))

        file_path = os.path.join(FILES[img_type]['content'], file)
        print(file)
        if img_type == 'person':
            process_time, (num_people, accuracy) = __person_video(file_path=file_path, model_file=FILES[img_type]['model'])
            print(process_time, num_people, accuracy)
        elif img_type == 'vehicle':
            total_time, total_cars, avg_speed = __vehicle_video(file_path=file_path, model_file=FILES[img_type]['model'])
            print(file, total_time, total_cars, avg_speed)


if __name__ == '__main__':
    main()
