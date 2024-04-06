import argparse
import time

from data_generator.blobs_video_imgs import get_data as video_imgs
from data_publisher.publisher_rest import publish_via_post

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('conn', type=str, default='127.0.0.1:32149',
                        help='connection information (example: [user]:[passwd]@[ip]:[port])')
    parser.add_argument('--batch-size', type=int, default=10, help='number of rows per insert batch')
    parser.add_argument('--total-rows', type=int, default=10,
                        help='total rows to insert - if set to 0 then run continuously')
    parser.add_argument('--sleep', type=float, default=0.5, help='wait time between each row to insert')
    parser.add_argument('--db-name', type=str, default='test', help='logical database name')
    parser.add_argument('--topic', type=str, default='image-mapping', help='topic name for POST, MQTT and Kafka')
    parser.add_argument('--timeout', type=float, default=30, help='REST timeout')
    parser.add_argument('--exception', type=bool, nargs='?', const=True, default=False,
                        help='Whether to print exceptions')
    args = parser.parse_args()

    total_rows = 0
    payloads = []

    while True:
        payload, last_blob = video_imgs(db_name='test', last_blob=None, exception=args.exception)

        payloads.append(payload)
        if len(payloads) == args.batch_size or (args.total_rows <= len(payloads) + total_rows and args.total_rows != 0):
            publish_via_post(conn=args.conn, payload=payloads, topic=args.topic, auth=(), timeout=args.timeout,
                             exception=args.exception)

            total_rows += len(payloads)
            payloads = []

        if total_rows >= args.total_rows:
            exit(1)
        time.sleep(args.sleep)


if __name__ == '__main__':
    main()