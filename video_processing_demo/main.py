import argparse
import os

def main():
    """
    The following demo demonstrate processing files into AnyLog and associating them     
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('dir_name', type=str, default='$HOME/Sample-Data-Generator/data/videos',
                        help='directory containing videos and/or images to be processed')
    parser.add_argument('--reverse', type=bool, nargs='?', const=True, default=False, help='reverse file order in video/image directory')
    args = parser.parse_args()

    dir_name = os.path.expandvars(os.path.expanduser(args.dir_name))
    if not os.path.isdir(dir_name):
        print(f'Failed to locate {dir_name}. Cannot continue')
        exit(1)
    else:
        list_dir = os.listdir(dir_name)
        if args.reverse is True:
            list_dir.reverse()

:
    for file_name in list_dir:
        start_ts, end_ts = __generate_timestamp(now=now)
        speed, cars = __car_counter(timestamp=start_ts)

        full_name = os.path.join(dir_name, file_name)
        # processed_data = # process the file


if __name__ == '__main__':
    main()
