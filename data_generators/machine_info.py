import datetime 
import psutil 
import requests
import socket
import time 

def machine_credentials()->(str, str, str): 
   """
   Get Hostname, local IP and remote IP (if avilable) 
   :param: 
      hostname:str - hostname
      local_ip:ip4 - local ip
      remote_ip:ip4 - remote ip 
   :return: 
       hostname and remote ip 
   """
   try:
      with open('/etc/hostname', 'r')  as f: 
         hostname = f.read().split('\n')[0]
   except: 
      hostname = 'localhost' 

   try: 
      remote_ip = requests.get('https://ipinfo.io/json').json()['ip']
   except: 
      remote_ip = '127.0.0.1' 

   try: 
      s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
      s.connect(("8.8.8.8", 80))
   except: 
      s = None 

   if s != None: 
      try: 
         local_ip = s.getsockname()[0]
      except: 
         local_ip = '127.0.0.1' 
   try: 
      s.close()
   except: 
      pass 

   return hostname, local_ip, remote_ip 

def boot_time()->float: 
   """
   Get time machine is running in seconds
   """
   try:
      return time.time() - psutil.boot_time() 
   except: 
      return 0.0 

def cpu_percentage()->float: 
   """
   Get CPU percentage
   """
   try: 
      return psutil.cpu_percent(interval=None) 
   except: 
      return 0.0  

def swap_memory()->float: 
   """
   Get SWAP memory usage
   """
   try:
      return psutil.swap_memory().percent
   except: 
      return 0.0 

def disk_usage()->float: 
   """
   Get disk usage percentage 
   """
   try: 
      return psutil.disk_usage().percenet 
   except: 
      return 0.0 

def get_device_data()->dict:
   """
   Get device_info
   :param: 
      timestamp:str 
      boot:float 
      cpu:float 
      swap:float 
      disk:float 
      data:dict - dict of generated values 
   :Sample:
      {
         "boot_time": 9103.919608592987,
         "cpu_percentage": 2.0,
         "disk_usage": 0.0,
         "hostname": "al-live-publisher",
         "local_ip": "172.104.180.110/32",
         "remote_ip": "172.104.180.110/32",
         "swap_memory": 4.8,
         "timestamp": "2021-01-01 00:00:19.695053"
      }
   :return: 
      dict
   """
   timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
   hostname, local_ip, remote_ip = machine_credentials() 
   boot = boot_time() 
   cpu = cpu_percentage() 
   swap = swap_memory() 
   disk = disk_usage() 


   data = {
      'timestamp': timestamp, 
      'hostname': hostname, 
      'local_ip': local_ip, 
      'remote_ip': remote_ip, 
      'boot_time': boot, 
      'cpu_percentage': cpu, 
      'swap_memory': swap, 
      'disk_usage': disk
   }

   return data 
