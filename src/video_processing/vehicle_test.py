import time
import os
from vehicle import VideoProcessing

ROOT_PATH = os.path.dirname(os.path.expanduser(os.path.expanduser(os.path.abspath(__file__))))
# MODEL_FILE = os.path.join(ROOT_PATH, 'models', 'vehicle.tflite')
# MODEL_FILE = os.path.join(ROOT_PATH, 'models', 'model_float.tflite')
MODEL_FILE = os.path.join(ROOT_PATH, 'models', 'model_float.tflite')
LABEL_FILE = os.path.join(ROOT_PATH, 'models', 'vehicle_coco_labels.txt')
VIDEO_DIR = os.path.expanduser(os.path.expandvars('$HOME/Downloads/sample_data/videos'))


def main():
    for file in os.listdir(VIDEO_DIR):
        num_cars={}
        avg_speed={}
        if 'B.mp4' in file:
            video_file = os.path.join(VIDEO_DIR, file)
            total_time = 0
            start_time = time.time()
            for label in ["car", "truck", "bus"]:
                vp = VideoProcessing(model_file=MODEL_FILE, labels=[f"0 {label}"], img_process='vehicle', video=video_file, exception=True)
                if vp.status is True:
                    vp.set_interpreter()
                if vp.status is True:
                    vp.process_video(min_confidence=0.1)
                    total_time += time.time() - start_time
                    cars, speed = vp.get_values()
                    num_cars[label] = cars
                    avg_speed[label] = speed
            if 'A.mp4':
                total_cars = int(sum(num_cars.values()))
            else:
                total_cars = int(sum(num_cars.values())/len(num_cars))

            print(total_time, file, total_cars, sum(avg_speed.values())/len(avg_speed))


if __name__ == '__main__':
    main()