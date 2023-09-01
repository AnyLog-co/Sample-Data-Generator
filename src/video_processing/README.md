# Vehicle & People Count 

Following is intended to support video analysis of (counting) people or cars. The code uses pre-defined TenserFlow 
models created by third-parties.
* [people.tflite](models/people.tflite) - model used for analyzing number of people in a video
* [vehicle.tflite](models/vehicle.tflite) - model used for analyzing number of cars in a video. 


## Requirements 
* [TensorFlow](https://www.tensorflow.org/install/pip) 
* [opencv-python](https://pypi.org/project/opencv-python/)
* [NumPy](https://numpy.org/)

## How Code Works 
[Video Processing](video_processing.py) analyzes videos and provides insight about it. 
* [process_video](video_processing.py#L152) method takes 
* [process_video](video_processing.py#L152)  

