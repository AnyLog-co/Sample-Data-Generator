import datetime
import time
import random
import psutil

def random_machine_data(db_name: str) -> dict:
    current_time = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    uptime = int(time.time() - psutil.boot_time())
    days, remainder = divmod(uptime, 24 * 3600)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    uptime_formatted = f"{days}:{hours:02}:{minutes:02}:{seconds:02}"

    data = {
        "dbms": db_name,
        "table": 'machine_info',
        'timestamp': current_time,
        'uptime': uptime_formatted,
        'node_id': random.choice(range(1, 11)),
    }

    for key in ['load_avg_1min', 'load_avg_5min', 'load_avg_15min', 'disk_space', 'cpu_percent', 'virtual_memory',
                'swap_memory', 'disk_write', 'disk_read', 'packets_recv', 'packets_sent']:
        data[key] = round(random.random() * 30, 3)

        return data


def machine_data(db_name: str) -> dict:
    current_time = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    uptime = int(time.time() - psutil.boot_time())
    days, remainder = divmod(uptime, 24 * 3600)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    uptime_formatted = f"{days}:{hours:02}:{minutes:02}:{seconds:02}"

    load_avg = psutil.getloadavg()
    disk_io = psutil.disk_io_counters()
    net_io = psutil.net_io_counters()

    return {
        "dbms": db_name,
        "table": 'machine_info',
        'timestamp': current_time,
        'uptime': uptime_formatted,
        'node_id': random.choice(range(1, 11)),
        'load_avg_1min': load_avg[0],
        'load_avg_5min': load_avg[1],
        'load_avg_15min': load_avg[2],
        'disk_space': psutil.disk_usage('/').percent,
        'cpu_percent': psutil.cpu_percent(interval=1),
        'virtual_memory': psutil.virtual_memory().percent,
        'swap_memory': psutil.swap_memory().percent,
        'disk_write': disk_io.write_count,
        'disk_read': disk_io.read_count,
        'packets_recv': net_io.packets_recv,
        'packets_sent': net_io.packets_sent,

    }