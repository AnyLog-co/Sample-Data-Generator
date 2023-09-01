import time
import os
from vehicle_new import VideoProcessing

ROOT_PATH = os.path.dirname(os.path.expanduser(os.path.expanduser(os.path.abspath(__file__))))
# MODEL_FILE = os.path.join(ROOT_PATH, 'models', 'vehicle.tflite')
# MODEL_FILE = os.path.join(ROOT_PATH, 'models', 'model_float.tflite')
LABEL_FILE = os.path.join(ROOT_PATH, 'models', 'vehicle_coco_labels.txt')
VIDEO_DIR = os.path.expanduser(os.path.expandvars('$HOME/Downloads/sample_data/videos'))

# -- video_new --
# detect not working with B-images and A-images
# float returns "odd" values with B-images
# model_float.tflite works "ok" for A-images
# vehicle.tflite works "ok" for B-images

# -- video --


def main():
    for file in os.listdir(VIDEO_DIR):
        for model in ['model_float.tflite']:
            MODEL_FILE = os.path.join(ROOT_PATH, 'models', model)
            num_cars={}
            avg_speed={}
            if 'mp4' in file:
                video_file = os.path.join(VIDEO_DIR, file)
                total_time = 0
                start_time = time.time()
                for label in ["car", "truck", "bus"]:
                    vp = VideoProcessing(model_file=MODEL_FILE, labels=[f"0 {label}"], video=video_file, exception=True)
                    if vp.status is True:
                        vp.set_interpreter()
                    if vp.status is True:
                        vp.process_video(min_confidence=0.25)
                        total_time += time.time() - start_time
                        cars, speed = vp.get_values()
                        num_cars[label] = cars
                        avg_speed[label] = speed
                print(total_time, model, file, num_cars, avg_speed)


if __name__ == '__main__':
    main()