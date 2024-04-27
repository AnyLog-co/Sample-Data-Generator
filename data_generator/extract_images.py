import requests
import os

ROOT_DIR = os.path.dirname(os.path.expanduser(os.path.expandvars(__file__))).split("data_generator")[0]
IMAGE_DIR = os.path.join(ROOT_DIR, 'blobs', 'ibm_imgs')

IMG_URL = "http://35.223.210.200:3002/static/video"
IMGS = [
    "image_1.jpg?1714167592685",
    "image_2.jpg?1714167592685",
    "image_3.jpg?1714167592685",
    "image_1.jpg?1714167824508",
    "image_2.jpg?1714167824508",
    "image_3.jpg?1714167824508",
    "image_1.jpg?1714169448707",
    "image_2.jpg?1714169448708",
    "image_3.jpg?1714169448708"
]

VID_URL = "http://35.223.210.200:3002/static/backup"
VIDEOS = [
    "video-old.mp4?1714167813150",
]

def download_imgs():
    for image in IMGS:
        try:
            r = requests.get(url=f"{IMG_URL}/{image}")
        except Exceptionn as error:
            print(error)
        else:
            if 200 <= int(r.status_code) <= 299:
                source = image.split(".")[0]
                id = image.split("?")[-1]
                print(os.path.join(IMAGE_DIR, f'{source}_{id}.jpg'))
                with open(os.path.join(IMAGE_DIR, f'{source}_{id}.jpg'), 'wb') as f:
                    f.write(r.content)
            else:
                print(r.status_code)

def download_vids():
    for vid in VIDEOS:
        try:
            r = requests.get(url=f"{VID_URL}/{vid}")
        except Exceptionn as error:
            print(error)
        else:
            if 200 <= int(r.status_code) <= 299:
                source = vid.split(".")[0]
                id = vid.split("?")[-1]
                print(os.path.join(IMAGE_DIR, f'{source}_{id}.mp4'))
                with open(os.path.join(IMAGE_DIR, f'{source}_{id}.mp4'), 'wb') as f:
                    f.write(r.content)
            else:
                print(r.status_code)


if __name__ == '__main__':
    download_imgs()
    download_vids()
