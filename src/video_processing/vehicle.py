import cv2
import numpy as np
import os
import tensorflow as tf
import time


class VideoProcessing:
    def __init__(self, model_file:str,  video:str=None, img_process:str='people', label_file:str=None,
                 exception:bool=False):
        """
        Declare file params + echeck if they exist
        :args:
            self.model_file:str - model file
            self.video_file:str - video to analyze
            self.img_process:str - whether processing people or vehicles
            self.label_file:str - label file
            self.exception:bool - whether to print exceptions
        :params:
            self.status:bool
            self.obj_count:int - number of people
            self.confidence:int - confidence
            self.grid_rows / self.grid_cols:int - breakdown of grid rows and columns
        """
        self.status = True
        self.obj_count = 0
        self.confidence = 0 # used for speed when dealing with vehicles
        self.grid_rows = 2
        self.grid_cols = 2
        self.inp_mean = 127.5
        self.inp_std = 127.5

        self.exception = exception
        self.img_process = img_process
        if self.img_process not in ['person', 'vehicle']:
            self.img_process = 'person'

        self.model_file = os.path.expanduser(os.path.expandvars(model_file))
        self.video_file = os.path.expanduser(os.path.expandvars(video))
        if not os.path.isfile(self.model_file):
            self.status = False
            if self.exception is True:
                print(f"Failed to locate model file {model_file}")
        if label_file is not None:
            self.label_file = os.path.expanduser(os.path.expandvars(label_file))
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

    def __set_grid_size(self):
        """
        Based on the rows and columns break video into grids
        :re
        """
        try:
            return np.zeros((int(self.grid_rows), int(self.grid_cols)))
        except Exception as error:
            self.status = False
            if self.exception is True:
                print(f"Failed to set grid size (Error: {error}")

    def set_interpreter(self):
        try:
            self.interpreter = tf.lite.Interpreter(model_path=self.model_file)
            self.interpreter.allocate_tensors()
            self.input_details = self.interpreter.get_input_details()
            self.output_details = self.interpreter.get_output_details()
        except Exception as error:
            self.status = False
            if self.exception is True:
                print(f"Failed to declare interpreter (Error: {error})")

    def process_video(self, min_confidence: float = 0.1):
        cell_height = 0  # Initialize cell_height
        cell_width = 0  # Initialize cell_width
        car_count_grid = self.__set_grid_size()
        if car_count_grid is None or self.status is False:
            return
        while True:
            ret, img2 = self.cap.read()
            if ret:
                img = cv2.resize(img2, (300, 300))

                input_data = (abs((np.array(img) - self.inp_mean) / self.inp_std) - 1).astype(np.float32)
                input_data = np.expand_dims(input_data, axis=0)

                self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
                t_in = time.time()
                self.interpreter.invoke()
                output_data = self.interpreter.get_tensor(self.output_details[0]['index'])

                predictions = np.squeeze(output_data)
                confidence_scores = np.squeeze(self.interpreter.get_tensor(self.output_details[2]['index']))

                moving_cars = []

                for i, newbox in enumerate(predictions):
                    if confidence_scores[i] > min_confidence:
                        y_min = int(newbox[0] * img.shape[0])
                        x_min = int(newbox[1] * img.shape[1])
                        y_max = int(newbox[2] * img.shape[0])
                        x_max = int(newbox[3] * img.shape[1])

                        if cell_height == 0:
                            cell_height = img.shape[0] // self.grid_rows
                            cell_width = img.shape[1] // self.grid_cols

                        for row in range(self.grid_rows):
                            for col in range(self.grid_cols):
                                cell_x_min = col * cell_width
                                cell_y_min = row * cell_height
                                cell_x_max = (col + 1) * cell_width
                                cell_y_max = (row + 1) * cell_height

                                if (cell_x_min < x_max < cell_x_max) and (cell_y_min < y_max < cell_y_max):
                                    moving_cars.append((row, col))
                                    car_count_grid[row, col] += 1

                for row, col in moving_cars:
                    cell_x_min = col * cell_width
                    cell_y_min = row * cell_height
                    cell_x_max = (col + 1) * cell_width
                    cell_y_max = (row + 1) * cell_height
                    cv2.rectangle(img2, (cell_x_min, cell_y_min), (cell_x_max, cell_y_max), (0, 255, 0), 2)

                fps = round(cv2.getTickFrequency() / (cv2.getTickCount() - t_in), 2)
                cv2.putText(img2, 'FPS : {}'.format(fps), (280, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255),
                            lineType=cv2.LINE_AA)
                cv2.imshow(' ', np.asarray(img2))
                cv2.waitKey(1)
            else:
                break

        self.cap.release()
        cv2.destroyAllWindows()

        total_cars = np.sum(car_count_grid)
        average_speed = np.mean(car_count_grid)
        print("Total cars detected:", total_cars)
        if average_speed < 1:
            average_speed = average_speed * 100
        print("Average of moving cars:", average_speed)

    def get_values(self):
        return self.obj_count, self.confidence
