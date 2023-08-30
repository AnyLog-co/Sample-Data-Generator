import time
import os
from video_processing import VideoProcessing

model_file = '$HOME/Sample-Data-Generator/ml_ai/detect.tflite'
label_file = '$HOME/Sample-Data-Generator/ml_ai/coco_labels.txt'
video_dir = os.path.expanduser(os.path.expandvars('$HOME/Downloads/sample_data/edgex-demo'))


def main():
    for video in os.listdir(video_dir):
        if 'mp4' in video:
            video_file = os.path.join(video_dir, video)
            start_time = time.time()
            vp = VideoProcessing(model_file=model_file, label_file=label_file, video=video_file, exception=True)
            if vp.status is True:
                vp.set_interpreter()
            if vp.status is True:
                vp.analyze_data()
                print(time.time() - start_time, video, vp.get_values())


if __name__ == '__main__':
    main()