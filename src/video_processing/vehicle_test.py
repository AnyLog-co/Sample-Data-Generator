import time
import os
from video_processing import VideoProcessing

ROOT_PATH = os.path.dirname(os.path.expanduser(os.path.expanduser(os.path.abspath(__file__))))
MODEL_FILE = os.path.join(ROOT_PATH, 'models', 'vehicle.tflite')
LABEL_FILE = os.path.join(ROOT_PATH, 'models', 'coco_labels.txt')
VIDEO_DIR = os.path.expanduser(os.path.expandvars('$HOME/Downloads/sample_data/videos/'))


def main():
    for file in os.listdir(VIDEO_DIR):
        if 'A.mp4' in file:
            video_file = os.path.join(VIDEO_DIR, file)
            start_time = time.time()
            vp = VideoProcessing(model_file=MODEL_FILE, label_file=LABEL_FILE, video=video_file, exception=True)
            if vp.status is True:
                vp.set_interpreter()
            if vp.status is True:
                vp.analyze_data(min_confidence=0.0, img_process='vehicle')
                print(time.time() - start_time, file, vp.get_values())


if __name__ == '__main__':
    main()