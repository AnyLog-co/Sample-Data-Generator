import os
import cv2
import numpy as np
import tensorflow as tf

class VideoProcessing:
    """
    Count number of people in a given video
    """
    def __init__(self, model_file:str, label_file:str, video:str, exception:bool=False):
        """
        Declare file params + echeck if they exist
        :params:
            self.status:bool
            self.exception:bool - whether to print exceptions
            self.model_file:str - model file
            self.label_file:str - label file
            self.video_file:str - video to analyze
            self.num_people:int - number of people
            self.confidence:int - confidence
        """
        self.status = True
        self.exception = exception
        self.num_people = 0
        self.confidence = 0
        self.model_file = os.path.expanduser(os.path.expandvars(model_file))
        self.label_file = os.path.expanduser(os.path.expandvars(label_file))
        self.video_file = os.path.expanduser(os.path.expandvars(video))

        if not os.path.isfile(self.model_file):
            self.status = False
            if self.exception is True:
                print(f"Failed to locate model file {model_file}")
        if os.path.isfile(self.label_file):
            self.__read_label_file()
        elif not os.path.isfile(self.label_file):
            self.status = False
            if self.exception is True:
                print(f"Failed to locate model file {label_file}")
        if os.path.isfile(self.video_file):
            self.__read_video()
        elif not os.path.isfile(self.video_file):
            self.status = False
            if self.exception is True:
                print(f"Failed to locate video filfe {video}")

    def __read_label_file(self):
        """
        read content in labels
        :params:
            self.labels:list  - content in file
        """
        try:
            with open(self.label_file, 'r') as f:
                self.labels = f.read().strip().split('\n')
        except Exception as error:
            self.status = False
            if self.exception is True:
                print(f"Failed to read content in {self.label_file} (Error: {error})")

    def __read_video(self):
        """
        read content in video file
        :params:
            self.cap:VideoCapture - content in video file
        """
        try:
            self.cap = cv2.VideoCapture(self.video_file)
        except Exception as error:
            self.status =  False
            if self.exception is True:
                print(f"Failed to read content in {self.video_file} (Error: {error})")

    def set_interpreter(self):
        """
        Set interpreter configs
        :args:
            self.interpreter: - interpreter
            self.input_details - input details
            self.output_details - output details
        """
        try:
            self.interpreter = tf.lite.Interpreter(model_path=self.model_file)
            self.interpreter.allocate_tensors()
            self.input_details = self.interpreter.get_input_details()
            self.output_details = self.interpreter.get_output_details()
        except Exception as error:
            self.status = False
            if self.exception is True:
                print(f"Failed to declare interpreter (Error: {error})")

    def analyze_data(self, min_confidence:float=0.5):
        # num_people = 0
        # confidence = 0
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break

            # Preprocess the frame
            resized_frame = cv2.resize(frame, (300, 300))
            input_data = resized_frame.astype(np.uint8)  # Convert to UINT8
            input_data = np.expand_dims(input_data, axis=0)
            self.interpreter.set_tensor(self.input_details[0]['index'], input_data)

            # Run inference
            self.interpreter.invoke()
            output_data = self.interpreter.get_tensor(self.output_details[0]['index'])

            num_people = 0

            # Post-process detection results
            for detection in output_data[0]:
                confidence = detection[2]
                class_id = int(detection[1])
                if confidence > min_confidence and self.labels[class_id].split(" ")[-1] == 'person':
                    num_people += 1

            if cv2.waitKey(1) & 0xFF == ord('q'):
                return

        self.cap.release()
        cv2.destroyAllWindows()

        self.num_people = num_people
        self.confidence = confidence

    def get_values(self)->(int, float):
        return self.num_people, self.confidence