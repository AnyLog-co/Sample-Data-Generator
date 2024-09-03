from flask import Flask, jsonify
import random
import time
import psutil
import datetime
from threading import Lock

app = Flask(__name__)
cache_lock = Lock()
cache = {
    'cpu_percent': None,
    'disk_io': None,
    'net_io': None,
    'virtual_memory': None,
    'swap_memory': None
}
CACHE_EXPIRY = 10  # seconds


def __generate_data(db_name: str) -> dict:
    current_time = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%fZ')

    # Cache results
    with cache_lock:
        cache_time = time.time()
        if cache['cpu_percent'] is None or (cache_time - cache.get('timestamp', 0) > CACHE_EXPIRY):
            cache['cpu_percent'] = psutil.cpu_percent(interval=1)
            cache['disk_io'] = psutil.disk_io_counters()
            cache['net_io'] = psutil.net_io_counters()
            cache['virtual_memory'] = psutil.virtual_memory().percent
            cache['swap_memory'] = psutil.swap_memory().percent
            cache['timestamp'] = cache_time

    uptime = int(time.time() - psutil.boot_time())
    days, remainder = divmod(uptime, 24 * 3600)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    uptime_formatted = f"{days}:{hours:02}:{minutes:02}:{seconds:02}"

    load_avg = psutil.getloadavg()
    disk_io = cache['disk_io']
    net_io = cache['net_io']

    return {
        "dbms": db_name,
        "table": 'machine_info',
        'timestamp': current_time,
        'uptime': uptime_formatted,
        'node_id': random.choice(range(1, 11)),
        'load_avg_5min': load_avg[1],
        'disk_space': psutil.disk_usage('/').percent,
        'cpu_percent': cache['cpu_percent'],
        'virtual_memory': cache['virtual_memory'],
        'swap_memory': cache['swap_memory'],
        'disk_write': disk_io.write_count,
        'disk_read': disk_io.read_count,
        'packets_recv': net_io.packets_recv,
        'packets_sent': net_io.packets_sent,
        'load_avg_15min': load_avg[2]
    }

@app.route('/data', methods=['GET'])
def get_data():
    db_name = "example_db"  # Change as needed
    data = __generate_data(db_name)
    return jsonify(data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5100)
