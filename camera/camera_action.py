import argparse
import cv2

class VideoDisplay:
    def __init__(self, camera_id:int=0, width:float=640, height:float=480):
        self.camera_id = camera_id
        self.width = width
        self.height = height
        self.is_running = False
        self.cap = self.__enable_video_capure()
        if not self.cap.isOpened() or self.cap is None:
            print("Error: Could not open video device.")
            exit()

    def __enable_video_capure(self):
        cap = None
        try:
            cap = cv2.VideoCapture(self.camera_id)
        except Exception as error:
            print(f"Failed to start video capture with cemra {self.camera_id} (Error: {error})")
        return cap

    def __set_cap_size(self, height:float=None, width:float=None):
        if height is None:
            height = self.height
        if width is None:
            width = self.width

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    def start(self, height:float=None, width:float=None):
        self.__set_cap_size(height=height, width=width)

        self.is_running = True
        while self.is_running:
            ret, frame = self.cap.read()
            if not ret:
                print("Error: Could not read frame.")
                break

            cv2.imshow('Video Feed', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.stop()

    def stop(self):
        self.is_running = False
        # self.cap.release()
        cv2.destroyAllWindows()

    def destory_windows(self):
        self.cap.release()


def main():
    parse = argparse.ArgumentParser()
    parse.add_argument('--camera-id', type=int, default=0, help='Camera ID')
    parse.add_argument('--width', type=float, default=640, help='livefeed screen ratio width')
    parse.add_argument('--height', type=float, default=480, help='livefeed screen ratio height')
    parse.add_argument('--show-video', type=bool, nargs='?', const=True, default=False, help='begin with an active livefeed')
    args = parse.parse_args()

    video_display = VideoDisplay(camera_id=args.camera_id, width=args.width, height=args.height)
    command = None
    if args.show_video is True:
        command = 'o'

    while True:
        if command == 'o':  # show video
            video_display.start(height=args.height, width=args.width)
        elif command == 'q':  # quit
            video_display.destory_windows()
            break
        elif command == 'h': # update height
            args.height = float(input("Updated height: "))
        elif command == 'w':
            args.width = float(input("Updated width: "))
        elif command is not None:
            print(f"Invalid option {command}")
        command = input("Command: ").strip()


if __name__ == "__main__":
    main()
