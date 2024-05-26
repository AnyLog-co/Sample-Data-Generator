import cv2
import multiprocessing as mp


def capture_frames(queue, camera_id=0, width=640, height=480):
    cap = cv2.VideoCapture(camera_id)
    if not cap.isOpened():
        print(f"Error: Could not open video device with camera ID {camera_id}.")
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame. Exiting capture loop.")
            break

        if not queue.full():
            queue.put(frame)

    cap.release()


def display_frames(queue, show_event):
    while show_event.is_set() or not queue.empty():
        if not queue.empty() and show_event.is_set():
            frame = queue.get()
            cv2.imshow('Video Feed', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                show_event.clear()
                break
        else:
            cv2.destroyAllWindows()

    cv2.destroyAllWindows()


def main():
    frame_queue = mp.Queue(maxsize=10)
    show_event = mp.Event()
    camera_id = 0
    width = 640
    height = 480

    capture_process = mp.Process(target=capture_frames, args=(frame_queue, camera_id, width, height))
    display_process = mp.Process(target=display_frames, args=(frame_queue, show_event))

    try:
        show_event.set()
        capture_process.start()
        display_process.start()

        # Wait for the display process to finish
        display_process.join()
    except KeyboardInterrupt:
        pass
    finally:
        show_event.clear()
        capture_process.join()
        display_process.terminate()


if __name__ == '__main__':
    main()
