from video_processing import VideoProcessing

model_file = '$HOME/Sample-Data-Generator/ml_ai/detect.tflite'
label_file = '$HOME/Sample-Data-Generator/ml_ai/coco_labels.txt'
video_file = '$HOME/Downloads/sample_data/edgex-demo/edgex7.mp4'

def main():
    vp = VideoProcessing(model_file=model_file, label_file=label_file, video=video_file, exception=True)
    if vp.status is True:
        vp.set_interpreter()
    if vp.status is True:
        vp.analyze_data()
    if vp.status is True:
        print(vp.get_values())

if __name__ == '__main__':
    main()