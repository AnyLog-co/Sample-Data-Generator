"""
# sample cURL request
curl --location --request POST 'http://10.31.1.197/v3/predict/e99aefb2-abfc-4ab0-88fb-59e3e8f2b47f' \
    --header 'Content-Type: multipart/form-data' \
    --header 'predictApiKey: 8KK7aDH5fttoV.Dd' \
    --header 'Authorization: Basic b3JpOnRlc3Q=' \
    --form 'imageFile=@"./deeptector/images/20200306202533614.jpg"' \
    --form 'type="image/jpeg"' \
    --form 'filename="./deeptector/images/20200306202533614.jpg"'
"""
import argparse
import os
import requests

URL = "http://10.31.1.197/v3/predict/e99aefb2-abfc-4ab0-88fb-59e3e8f2b47f"
HEADERS = {
    # 'Content-Type': 'multipart/form-data',
    'predictApiKey': '8KK7aDH5fttoV.Dd',
    'Authorization': 'Basic b3JpOnRlc3Q=',
}

FILES = {
    'imageFile': None, # open('/home/anylog/deeptector/images/20200306202533614.jpg', 'rb')
    'type': (None, '"image/jpeg"'),
    'filename': None, # (None, '/home/anylog/deeptector/images/20200306202533614.jpg')
}

def __get_data(url, headers, files, exception:bool=False)->dict:
    output = {}
    try:
        r = requests.post(url=url, headers=headers, files=files)
    except Exception as error:
        if exception is True:
            print(f'Failed to get data from Deeptector (Error: {error})')
    else:
        if int(r.status_code) != 200:
            print(f'Failed to get data from Deeptector (Network Error: {r.status_code})')
        else:
            try:
                output = r.json()
            except Exception as error:
                output = r.text
    return output

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('dir_name', type=str, default=DIRECTORY_PATH, help='image directory path')
    parser.add_argument('conn', type=str, default='127.0.0.1:32149',
                        help='{user}:{password}@{ip}:{port} for sending data either via REST or MQTT')
    parser.add_argument('protocol', type=str, choices=['post', 'mqtt'], default='post', help='format to save data')
    parser.add_argument('--topic', type=str, default='anylog-data-gen', help='topic to send data agaisnt')
    parser.add_argument('--dbms', type=str, default='ntt', help='Logical database to store data in')
    parser.add_argument('--table', type=str, default='deeptechtor', help='Logical database to store data in')
    parser.add_argument('--sleep', type=int, default=30, help='wait time between each round of inserts')
    parser.add_argument('--exception', type=bool, nargs='?', const=True, default=False,
                        help='whether or not to print exceptions to screen')
    args = parser.parse_args()

    full_path = os.path.expandvars(os.path.expanduser(args.dir_name))
    for image in os.listdir(dir_name):
        file_path = os.path.join(full_path, image)
        FILES['imageFile'] = open(file_path, 'rb')
        FILES['filename'] = (None, file_path)

        data = __get_data(url=URL, headers=HEADERS, files=FILES, exception=args.exception)
        print(image, data)
