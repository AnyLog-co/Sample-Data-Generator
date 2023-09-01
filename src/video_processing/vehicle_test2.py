import time
import os
from vehicle import VideoProcessing

ROOT_PATH = os.path.dirname(os.path.expanduser(os.path.expanduser(os.path.abspath(__file__))))
MODEL_FILE = os.path.join(ROOT_PATH, 'models', 'vehicle.tflite')
LABEL_FILE = os.path.join(ROOT_PATH, 'models', 'vehicle_coco_labels.txt')
VIDEO_DIR = os.path.expanduser(os.path.expandvars('$HOME/Downloads/sample_data/videos'))


def main():
    for video in os.listdir(VIDEO_DIR):
        if 'mp4' in video:
            video_file = os.path.join(VIDEO_DIR, video)
            start_time = time.time()
            vp = VideoProcessing(model_file=MODEL_FILE, label_file=LABEL_FILE, video=video_file, exception=True)
            if vp.status is True:
                vp.set_interpreter()
            if vp.status is True:
                vp.analyze_data(min_confidence=0.5)
                print(time.time() - start_time, video, vp.get_values())


if __name__ == '__main__':
    main()