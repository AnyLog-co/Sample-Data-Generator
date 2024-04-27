import argparse
import time

from data_generator.blobs_video_imgs import get_data as video_imgs
from data_generator.blobs_live_data import get_data as live_data
from data_publisher.publisher_rest import publish_via_post
from data_publisher.publisher_rest import publish_via_put


def __file_blobs(conn:str, db_name:str='test', grand_total:int=10, batch_size:int=10, sleep:float=0.5, topic:str='image-mapping',
                 timeout:float=30, exception:bool=False):
    total_rows = 0
    payloads = []
    last_blob = None
    while True:
        payload, last_blob = video_imgs(db_name=db_name, last_blob=last_blob, exception=exception)
        payloads.append(payload)
        if len(payloads) == batch_size or (grand_total <= len(payloads) + total_rows and grand_total != 0):
            publish_via_post(conn=conn, payloads=payloads, topic=topic, auth=(), timeout=timeout,
                             exception=exception)

            total_rows += len(payloads)
            payloads = []

        if total_rows >= grand_total:
            exit(1)
        time.sleep(sleep)

def __live_blobs(conn:str, data_ip:str, db_name:str='test', grand_total:int=10, batch_size:int=10, sleep:float=0.5, topic:str='image-mapping',
                 timeout:float=30, exception:bool=False):
    total_rows = 0
    payloads = []
    last_blob = None
    while True:
        payload, last_blob = live_data(db_name=db_name, url=data_ip, last_blob=last_blob, exception=exception)
        payloads.append(payload)
        if len(payloads) == batch_size or (grand_total <= len(payloads) + total_rows and grand_total != 0):
            publish_via_post(conn=conn, payloads=payloads, topic=topic, auth=(), timeout=timeout,
                             exception=exception)

            total_rows += len(payloads)
            payloads = []

        if total_rows >= grand_total:
            exit(1)
        time.sleep(sleep)


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
    parser.add_argument('--data-ip', type=str, default=None, help='OpenHorizon AI IP:Port address')
    parser.add_argument('--exception', type=bool, nargs='?', const=True, default=False,
                        help='Whether to print exceptions')
    args = parser.parse_args()

    if args.data_ip is None:
        __file_blobs(conn=args.conn, db_name=args.db_name, grand_total=args.total_rows, batch_size=args.batch_size,
                     sleep=args.sleep, topic=args.topic, timeout=args.timeout, exception=args.exception)

    __live_blobs(conn=args.conn, data_ip=args.data_ip, db_name=args.db_name, grand_total=args.total_rows,
                 batch_size=args.batch_size, sleep=args.sleep, topic=args.topic, timeout=args.timeout,
                 exception=args.exception)





if __name__ == '__main__':
    main()