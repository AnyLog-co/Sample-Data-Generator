import numpy as np
import tensorflow as tf
import cv2
import time
import os

# Load TFLite model and allocate tensors.
interpreter = tf.lite.Interpreter(model_path="models/model_float.tflite")
interpreter.allocate_tensors()

# Get input and output tensors.
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

height = input_details[0]['shape'][1]
width = input_details[0]['shape'][2]

inp_mean = 127.5
inp_std = 127.5

path_to_video = os.path.expanduser(os.path.expandvars('$HOME/Downloads/sample_data/videos/video24B.mp4'))

cap = cv2.VideoCapture(path_to_video)

grid_rows = 5  # Number of grid rows
grid_cols = 5  # Number of grid columns

# Initialize a grid to keep track of car counts in each cell
car_count_grid = np.zeros((grid_rows, grid_cols))

while True:
    ret, img2 = cap.read()

    if ret:
        img = cv2.resize(img2, (300, 300))

        input_data = (abs((np.array(img) - inp_mean) / inp_std) - 1).astype(np.float32)
        input_data = np.expand_dims(input_data, axis=0)

        interpreter.set_tensor(input_details[0]['index'], input_data)
        t_in = time.time()
        interpreter.invoke()
        output_data = interpreter.get_tensor(output_details[0]['index'])

        predictions = np.squeeze(output_data)
        confidence_scores = np.squeeze(interpreter.get_tensor(output_details[2]['index']))

        moving_cars = []  # List to store moving cars' bounding boxes

        for i, newbox in enumerate(predictions):
            if confidence_scores[i] > 0.1:
                y_min = int(newbox[0] * img.shape[0])
                x_min = int(newbox[1] * img.shape[1])
                y_max = int(newbox[2] * img.shape[0])
                x_max = int(newbox[3] * img.shape[1])

                # Check if the box falls within any grid cell
                cell_height = img.shape[0] // grid_rows
                cell_width = img.shape[1] // grid_cols
                for row in range(grid_rows):
                    for col in range(grid_cols):
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

cap.release()
cv2.destroyAllWindows()

total_cars = np.sum(car_count_grid)
average_speed = np.mean(car_count_grid)
print("Total cars detected:", total_cars)
if average_speed < 1:
    average_speed = average_speed * 100
print("Average of moving cars:", average_speed)
