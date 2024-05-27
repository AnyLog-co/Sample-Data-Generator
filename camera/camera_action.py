import argparse
import cv2
import datetime
import os
import time
import threading

ROOT_PATH = os.path.dirname(__file__)

def get_default_camera_id():
    camera_id = None
    for i in range(10):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            cap.release()
            camera_id = i
            break

    if camera_id is None:
        raise Exception("Error: Could not find an available camera.")
    return camera_id

class VideoRecorder:
    def __init__(self, camera_id:int=0, width:float=640, height:float=480, wait_time:int=60):
        self.camera_id = camera_id
        self.width = width
        self.height = height
        self.is_running = False
        self.cap = self.__enable_video_capture()
        if not self.cap.isOpened() or self.cap is None:
            raise Exception(f"Error: Could not open video device for camera ID {camera_id}")
        self.video_writer = self.__create_video_writer()
        self.start_time = time.time()
        self.wait_time = wait_time

    def __enable_video_capture(self):
        cap = None
        try:
            cap = cv2.VideoCapture(self.camera_id)
        except Exception as error:
            raise Exception(f"Failed to start video capture with camera {self.camera_id} (Error: {error})")
        return cap

    def __set_cap_size(self, height:float=None, width:float=None):
        if height is None:
            height = self.height
        if width is None:
            width = self.width

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    def __create_video_writer(self):
        filename = os.path.join(ROOT_PATH, f'{datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")}.mp4')
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video_writer = cv2.VideoWriter(filename, fourcc, 20.0, (int(self.width), int(self.height)))
        return video_writer

    def start_recording(self):
        self.__set_cap_size()

        self.is_running = True
        threading.Thread(target=self.__record).start()

    def __record(self):
        while self.is_running:
            ret, frame = self.cap.read()
            if not ret:
                print("Error: Could not read frame.")
                self.is_running = False
                break
                # continue  # Instead of breaking, we continue to try reading the next frame

            current_time = time.time()
            if current_time - self.start_time >= self.wait_time:  # Check if wait_time seconds have passed
                self.video_writer.release()  # Release the current video writer
                self.video_writer = self.__create_video_writer()  # Create a new video writer
                self.start_time = current_time  # Reset the start time

            self.video_writer.write(frame)  # Write the frame to the video file

    def stop_recording(self):
        self.is_running = False
        self.cap.release()
        self.video_writer.release()  # Release the video writer

    def display_feed(self, height:float=None, width:float=None):
        self.__set_cap_size(height=height, width=width)
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Error: Could not read frame.")
                continue

            cv2.imshow('Video Feed', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break


def main():
    parse = argparse.ArgumentParser()
    parse.add_argument('--camera-id', type=int, default=get_default_camera_id(), help='Camera ID')
    parse.add_argument('--width', type=float, default=640, help='Live feed screen ratio width')
    parse.add_argument('--height', type=float, default=480, help='Live feed screen ratio height')
    parse.add_argument('--cut-video', type=int, default=10, help='Video size (in seconds)')
    args = parse.parse_args()

    video_recorder = VideoRecorder(camera_id=args.camera_id, width=args.width, height=args.height, wait_time=args.cut_video)
    video_recorder.start_recording()

    try:
        while True:
            command = input("Command (o to open feed, q to quit, h to update height, w to update width): ").strip()
            if command == 'o':
                video_recorder.display_feed(height=args.height, width=args.width)
            if command == 'q':  # Quit
                break
            elif command == 'h':  # Update height
                args.height = float(input("Updated height: "))
            elif command == 'w':  # Update width
                args.width = float(input("Updated width: "))
            else:
                print(f"Invalid option {command}")
    except KeyboardInterrupt:
        print("\nInterrupted by user. Stopping...")
    except Exception as error:
        print(f"\nError: {error}")
    finally:
        video_recorder.stop_recording()

if __name__ == "__main__":
    main()
