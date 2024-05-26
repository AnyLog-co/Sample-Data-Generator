import cv2
import os
# import torch

ROOT_DIR = os.path.expanduser(os.path.expandvars(__file__)).split("people")[0]
BLOB = os.path.join(ROOT_DIR, 'edgex5.mp4')

# model = torch.hub.load('WongKinYiu/yolov7', 'custom', 'yolov7.pt')
# model.eval()

def read_video(blob):
    try:
        cap = cv2.VideoCapture(BLOB)
    except Exception as error:
        print(f"Failed to open {BLOB} (Error: {error})")
        exit(1)
    else:
        if cap.isOpened() is False:
            print(f"Error opening video file {BLOB}")
            exit(1)

    # Read until video is completed
    while (cap.isOpened()):
        # Capture frame-by-frame
        ret, frame = cap.read()
        if ret == True:
            # Display the resulting frame
            cv2.imshow('Frame', frame)

            # Press Q on keyboard to exit
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

        # Break the loop
        else:
            break

    # When everything done, release
    # the video capture object
    cap.release()

    # Closes all the frames
    cv2.destroyAllWindows()


if __name__ == '__main__':
    read_video(blob=BLOB)