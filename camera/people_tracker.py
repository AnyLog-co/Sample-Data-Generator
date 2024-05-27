import cv2
import os
import torch

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
BLOB = os.path.join(ROOT_DIR, 'edgex5.mp4')
YOLOV7_REPO = 'WongKinYiu/yolov7'
YOLOV7_MODEL = 'yolov7'

model = torch.hub.load(YOLOV7_REPO, YOLOV7_MODEL)
model.eval()

def read_video(blob):
    try:
        cap = cv2.VideoCapture(blob)
    except Exception as error:
        print(f"Failed to open {blob} (Error: {error})")
        exit(1)
    else:
        if not cap.isOpened():
            print(f"Error opening video file {blob}")
            exit(1)

    # Read until video is completed
    while cap.isOpened():
        # Capture frame-by-frame
        ret, frame = cap.read()
        if ret:
            # Display the resulting frame
            cv2.imshow('Frame', frame)

            # Press Q on keyboard to exit
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        else:
            break

    # When everything done, release
    # the video capture object
    cap.release()
    # Closes all the frames
    cv2.destroyAllWindows()

if __name__ == '__main__':
    read_video(BLOB)
import cv2
import os
import torch

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
BLOB = os.path.join(ROOT_DIR, 'edgex5.mp4')
YOLOV7_REPO = 'WongKinYiu/yolov7'
YOLOV7_MODEL = 'yolov7'

model = torch.hub.load(YOLOV7_REPO, YOLOV7_MODEL)
model.eval()

def read_video(blob):
    try:
        cap = cv2.VideoCapture(blob)
    except Exception as error:
        print(f"Failed to open {blob} (Error: {error})")
        exit(1)
    else:
        if not cap.isOpened():
            print(f"Error opening video file {blob}")
            exit(1)

    # Read until video is completed
    while cap.isOpened():
        # Capture frame-by-frame
        ret, frame = cap.read()
        if ret:
            # Display the resulting frame
            cv2.imshow('Frame', frame)

            # Press Q on keyboard to exit
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        else:
            break

    # When everything done, release
    # the video capture object
    cap.release()
    # Closes all the frames
    cv2.destroyAllWindows()

if __name__ == '__main__':
    read_video(BLOB)
