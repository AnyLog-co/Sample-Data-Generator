import argparse
import json
import os.path

import requests

def post_data(conn:str, payload:str, topic:str):
    headers = {
        "command": "data",
        "topic":topic,
        'User-Agent': 'AnyLog/1.23',
        'Content-Type': 'text/plain'
    }

    try:
        r = requests.post(url=f"http://{conn}", headers=headers, data=payload)
    except Exception as error:
        print(error)
    else:
        if int(r.status_code) != 200:
            print(r.status_code)
        else:
            print("Success!")


def read_file(file_path:str):
    content = None
    json_content = None
    try:
        with open(file_path)  as f:
            try:
                content = json.load(f)
            except Exception as error:
                print(error)
    except Exception as error:
        print(error)
    else:
        try:
            json_content = json.dumps(content, indent=4)
        except Exception as error:
            print(error)
    return json_content

def main():
    args = argparse.ArgumentParser()
    args.add_argument('conn', type=str, default=None, help='REST conn')
    args.add_argument('json_file', type=str, default=None, help='JSON file')
    args.add_argument('topic', type=None, default=None, help='topic name')
    parser = args.parse_args()

    file_path = os.path.expanduser(os.path.expandvars(parser.json_file))
    if not os.path.isfile(file_path):
        print(f"Failed to locate file {parser.json_file}")
        exit(1)

    content = read_file(file_path)
    post_data(conn=parser.conn, payload=content, topic=parser.topic)

if __name__ == '__main__':
    main()


