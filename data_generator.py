import argparse

from data_generator.blobs_video_imgs import get_data as video_imgs
from data_generator.blobs_factory_images import get_data as factory_imgs


def main():
    output = video_imgs(db_name='test', last_blob=None, exception=True)
    print("video")


    # output = factory_imgs(db_name='test', last_blob=None, exception=True)
    # print("factory")


if __name__ == '__main__':
    main()