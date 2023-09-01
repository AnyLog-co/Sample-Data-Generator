import cv2
import numpy as np
import os
import tensorflow as tf
import time


def calculate_speed(displacement, elapsed_time):
    """
    Calculate the speed based on displacement and elapsed time.
    :param displacement: Tuple (dx, dy) representing displacement
    :param elapsed_time: Elapsed time in seconds
    :return: Speed in units per second
    """
    dx, dy = displacement
    speed = np.sqrt(dx ** 2 + dy ** 2) / elapsed_time
    return speed


def calculate_displacement(new_position, old_position):
    """
    Calculate the displacement between two bounding box positions.
    :param new_position: New bounding box position (x_min, y_min, x_max, y_max)
    :param old_position: Old bounding box position (x_min, y_min, x_max, y_max)
    :return: Displacement as a tuple (dx, dy)
    """
    new_center_x = (new_position[0] + new_position[2]) / 2
    new_center_y = (new_position[1] + new_position[3]) / 2
    old_center_x = (old_position[0] + old_position[2]) / 2
    old_center_y = (old_position[1] + old_position[3]) / 2

    dx = new_center_x - old_center_x
    dy = new_center_y - old_center_y

    return dx, dy


def calculate_elapsed_time(prev_frame_time):
    """
    Calculate the elapsed time since the previous frame.
    :param prev_frame_time: Time of the previous frame
    :return: Elapsed time in seconds
    """
    return time.time() - prev_frame_time


class VideoProcessing:
    def __init__(self, model_file:str,  video:str=None, labels:list=["0 person"], img_process:str='people', label_file:str=None,
                 exception:bool=False):
        """
        Declare file params + echeck if they exist
        :args:
            self.model_file:str - model file
            self.video_file:str - video to analyze
            self.img_process:str - whether processing people or vehicles
            self.labels:list - label to search for
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
        self.grid_rows = 10
        self.grid_cols = 10
        self.inp_mean = 127.5
        self.inp_std = 127.5

        self.exception = exception
        self.img_process = img_process
        if self.img_process not in ['person', 'vehicle']:
            self.img_process = 'person'

        self.model_file = os.path.expanduser(os.path.expandvars(model_file))
        self.video_file = os.path.expanduser(os.path.expandvars(video))
        self.labels = labels
        if not os.path.isfile(self.model_file):
            self.status = False
            if self.exception is True:
                print(f"Failed to locate model file {model_file}")

        if os.path.isfile(self.video_file):
            self.__read_video()
        elif not os.path.isfile(self.video_file):
            self.status = False
            if self.exception is True:
                print(f"Failed to locate video filfe {video}")

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

    def __set_grid_size(self, video_height, video_width):
        """
        Calculate the grid size based on video dimensions
        :param video_height: Height of the video frame
        :param video_width: Width of the video frame
        :return: Initialized car_count_grid
        """
        try:
            cell_height = video_height / self.grid_rows
            cell_width = video_width / self.grid_cols
            return np.zeros((int(self.grid_rows), int(self.grid_cols))), cell_height, cell_width
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
        car_speed = []
        ret, img2 = self.cap.read()
        if not ret:
            return
        video_height, video_width, _ = img2.shape
        car_count_grid, cell_height, cell_width = self.__set_grid_size(video_height, video_width)
        if car_count_grid is None or self.status is False:
            return

        prev_frame_time = None
        prev_frame_positions = {}

        while True:
            ret, img2 = self.cap.read()
            if not ret:
                break

            img = cv2.resize(img2, (300, 300))
            if self.input_details[0]['dtype'] == np.uint8:
                input_data = np.array((img / self.inp_std) + self.inp_mean, dtype=np.uint8)
            elif self.input_details[0]['dtype'] == np.float32:
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
                                prev_frame_positions[i] = newbox

            for row, col in moving_cars:
                x1 = int(col * cell_width)
                y1 = int(row * cell_height)
                x2 = int((col + 1) * cell_width)
                y2 = int((row + 1) * cell_height)
                cv2.rectangle(img2, (x1, y1), (x2, y2), (0, 250, 0), 2)

            fps = round(cv2.getTickFrequency() / (cv2.getTickCount() - t_in), 2)
            cv2.putText(img2, 'FPS : {}'.format(fps), (280, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255),
                        lineType=cv2.LINE_AA)
            cv2.imshow(' ', np.asarray(img2))
            cv2.waitKey(1)

            if prev_frame_time is not None:
                elapsed_time = time.time() - prev_frame_time
                for i, prev_position in prev_frame_positions.items():
                    displacement = calculate_displacement(predictions[i], prev_position)
                    if displacement is not None:
                        car_speed.append(calculate_speed(displacement, elapsed_time))

            prev_frame_time = time.time()

        self.cap.release()
        cv2.destroyAllWindows()

        self.obj_count = np.sum(car_count_grid)
        if len(car_speed) > 0:
            self.confidence = (sum(car_speed)/len(car_speed)) * 10

    def get_values(self):
        return self.obj_count, self.confidence

