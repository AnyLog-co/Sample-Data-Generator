import argparse
import cv2
import numpy
import os

from sample_data_generator.video_processing.__support__ import read_csv_to_dict

def __load_frames(video_file):
    return cv2.VideoCapture(video_file)
def __get_video_size(cap):
    width = int(cap.get(3))
    height = int(cap.get(4))
    cap.release()
    return width, height

def __calculate_number_of_sequences(cap):
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    duration_in_seconds = total_frames / fps
    frames_per_sequence = int(fps)

    number_of_sequences = total_frames // frames_per_sequence

    cap.release()

    return number_of_sequences


def load_video(cap):
    frames = []
    width, height = __get_video_size(cap)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Resize frames if needed
        frame = cv2.resize(frame, (width, height))

        # Normalize pixel values to be between 0 and 1
        frame = frame / 255.0

        frames.append(frame)

    cap.release()
    return numpy.array(frames)


def load_and_preprocess_all_data(video_file):
    cap = __load_frames(video_file=video_file)
    # Load video frames
    frames = load_video(cap)

    # Ensure that the sequence length is 10 (adjust as needed)
    target_sequence_length = __calculate_number_of_sequences(cap)
    current_sequence_length = len(frames)

    if current_sequence_length < target_sequence_length:
        # Pad with zeros along the first axis to achieve the desired sequence length
        padding_width = ((0, target_sequence_length - current_sequence_length), (0, 0), (0, 0), (0, 0))
        frames = numpy.pad(frames, padding_width, mode='constant', constant_values=0)

    # Append to data and labels lists
    return frames




def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--csv-file', type=str, default=None, help='CSV information file')
    parser.add_argument('--data-dir', type=str, default=None, help='Directory with videos')
    args = parser.parse_args()

    csv_file = os.path.expandvars(os.path.expanduser(args.csv_file))
    data_dir = os.path.expandvars(os.path.expanduser(args.data_dir))

    video_data = []
    values = []

    if not os.path.isfile(csv_file):
        print(f"Failed to locate CSV file - {csv_file}")
        exit(1)
    if not os.path.isdir(data_dir):
        print(f"Failed to locate data dir - {data_dir}")
        exit(1)

    # read content in file
    data = read_csv_to_dict(csv_file)

    for fn in data:
        file_path = os.path.join(data_dir, fn)
        if os.path.isfile(file_path):
            print(load_and_preprocess_all_data(video_file=file_path))
            values.append(data[fn])



if __name__ == '__main__':
    main()