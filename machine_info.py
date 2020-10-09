import datetime 
import psutil 
import time 

def boot_time()->float: 
   """
   Get time machine is running in seconds
   """
   try:
      return time.time() - psutil.boot_time() 
   except: 
      return 0.0 

def cpu_percentge()->float: 
   """
   Get CPU percentage
   """
   try: 
      return psutil.cpu_percent(interval=None) 
   except: 
      return 0.0  

def swap_memory()->float: 
   """
   Get SWAP memory useage
   """
   try:
      return psutil.swap_memory().percent
   except: 
      return 0.0 

def disk_useage()->float: 
   """
   Get disk useage percentage 
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
   :return: 
      dict
   """
   timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
   boot = boot_time() 
   cpu = cpu_percentge() 
   swap = swap_memory() 
   disk = disk_useage() 

   data = {'timestamp': timestamp, 'boot_time': boot, 'cpu_percentge': cpu, 'swap_memory': swap, 'disk_useage': disk}
   return data 
