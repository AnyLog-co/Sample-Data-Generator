import argparse
import datetime 
import json 
import os 
import random
import requests 
import time 

import send_protocols
import write_file

DEVICE_UUIDS = {
   'machine': [
      'df064fb5-4266-4994-8d24-408af6ab96e6', 
      '94d0c54f-c182-4463-af2f-758342ac9189', 
      '7f580287-56bc-44e9-8018-4338d088a2d0',
      'c97cddd9-d63e-4c3e-bfc0-0319801488d4'
   ],
   'ping': [
      'd311cde1-bfa1-478f-bedb-d00f457d70cf', 
      '876cfe26-6575-4f30-af90-f6595a5dec40', 
      '7f580287-56bc-44e9-8018-4338d088a2d0',
      'c97cddd9-d63e-4c3e-bfc0-0319801488d4'
   ],
   'sin': [
      'a4e772f1-78c2-4bee-8737-5a26d4b0496b',
      '3bc62a84-5082-447b-9c9c-417c89c8cc33',
      '7f580287-56bc-44e9-8018-4338d088a2d0'
   ], 
   'cos': [
      '30663c80-0228-4684-8c16-31f1f93d370b',
      '3bc62a84-5082-447b-9c9c-417c89c8cc33',
      '7f580287-56bc-44e9-8018-4338d088a2d0'
   ],  
   'rand': [
      '3645f6aa-2f80-4cb3-99e9-aa0000d62d0b', 
      '3bc62a84-5082-447b-9c9c-417c89c8cc33',
      '7f580287-56bc-44e9-8018-4338d088a2d0'
   ] 
}
def get_machine_data(dbms:str, mode:str)->(dict, dict):
   """
   machine data     
   :args: 
      conn:str - connection info
      dbms:str - database name 
      mode:str - insert mode
   :param: 
      header:dict - info regarding insert 
      payload:dict - data to insert  
   """
   import machine_info  
   header = { 
       'type': 'json', 
       'dbms': dbms, 
       'table': 'machine_data', 
       'mode': mode, 
       'Content-Type': 'text/plain'
   } 
   payload = machine_info.get_device_data() 
   return header, payload 

def get_ping_sensor(dbms:str, mode:str)->(dict, dict):
   """
   ping sensor data     
   :args: 
      conn:str - connection info
      dbms:str - database name 
      mode:str - insert mode
   :param: 
      header:dict - info regarding insert 
      payload:dict - data to insert  
   """
   import ping_sensor
   header = {
       'type': 'json',
       'dbms': dbms,
       'table': 'ping_sensor',
       'mode': mode,
       'Content-Type': 'text/plain'
   }
   payload = ping_sensor.get_ping_data()
   return header, payload 

def get_trig(dbms:str, sensor:str, mode:str, sleep:float)->(list, dict): 
   """
   trig (sin/cos) data      
   :args: 
      conn:str - connection info
      dbms:str - database name 
      mode:str - insert mode
      sensor:str - sensor name (sin/cos) 
      sleep:float - wait between each get 
   :param: 
      header:dict - info regarding insert 
      payloads:list - list of payload (dict) values 
   """
   import trig 
   header = {
       'type': 'json',
       'dbms': dbms,
       'table': '%s_data' % sensor,
       'mode': mode,
       'Content-Type': 'text/plain'
   }
   payloads = [] 
   if sensor == 'sin': 
      payloads = trig.sin_value(sleep)
   elif sensor == 'cos': 
      payloads = trig.cos_value(sleep) 
   else: 
      payloads = trig.rand_value(sleep) 
   return header, payloads
      

def switch_get_data(dbms:str, sensor:str, mode:str, sleep:float)->(dict, list):
   """
   Switch to get data based on sensor
   :args:
      dbms:str - logical database name 
      sensor:str - sensor to get data from 
      mode:str - mode to store data 
      sleep:float - wait time between each row
   :param:
      data_list:list - list of data values 
      header:dict - header value  
      payload - payload for device 
   :return:
      data_list 
   """
   data_list = [] 
   header = {} 
   if sensor == 'machine' or sensor == 'ping':
      for i in range(10): 
         paylaod = None 
         if sensor == 'machine': 
            header, payload = get_machine_data(dbms, mode)         
         elif sensor == 'ping': 
            header, payload = get_ping_sensor(dbms, mode)
         data_list.append(payload) 
         time.sleep(1) 
   else: 
      header, data_list = get_trig(dbms, sensor, mode, sleep)
 
   return header, data_list

def switch_store_data(store_format:str, location:str, sensor:str, conn:str, header:dict, payloads:list): 
   """
   Switch to store data
   :args:
      store_format:str - format to store data 
      location:str - Directory 
      conn:str - connection info 
      header:dict - header for query
      payload:dict - data to store in operator
   """
   if store_format == 'rest': 
      if send_protocols.validate_connection(conn) == True: 
         for payload in payloads: 
            send_protocols.send_data(conn, header, payload) 
   elif store_format == 'file': 
      device_id = random.choice(DEVICE_UUIDS[sensor])
      write_file.write_data(location, device_id, header, payloads) 
   else: 
      for payload in payloads: 
         write_file.print_data(payload)

def main(): 
   """
   Generate data into database via REST / print / file  
   * For ping and machine data generate 10 rows for each iteration 
   * For sin/cos data generate 30 rows for each iteraton, between -π and π   
   :positional arguments:
      conn:str   - REST host and port
      dbms:str   - database name
      sensor:str - type of sensor to get data from 
         * machine - boot time, cpu useage, swap memory percentage, disk useage percentege 
         * ping    - information regarding a PING sensor randomly selected form list 
         * sin     - sinsign values over time 
         * cos     - cossign values over time  
         * rand    - random value between -π and π 
   :optional arguments:
      -h, --help                            - show this help message and exit

      -f, --stroe-format  INSERT_FORMAT:str - format to get data               (default: rest)
         * rest - send data via REST 
      -m, --mode MODE:str - insert type (default: streaming) 
         * streaming - insert data in memory once memory is full or after N seconds (configrured on AnyLog) 
         * file - insert data one by one 
      -r, --repeat REPEAT:int - number of iterations. If set to 0 run continuesly (default: 1)
      -s, --sleep SLEEP:float - wait between insert (default: 0)
   """
   parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
   parser.add_argument('conns',  type=str, default='127.0.0.1:2049', help='REST host and port')
   parser.add_argument('dbms',   type=str, default='sample_data',    help='database name') 
   parser.add_argument('sensor', type=str, default='ping',  choices=['machine', 'ping', 'sin', 'cos', 'rand'], help='type of sensor to get data from') 
   parser.add_argument('-f', '--store-format', type=str,    default='rest',       choices=['rest', 'file', 'print'], help='format to get data') 
   parser.add_argument('-l', '--location',     type=str,    default='$HOME/AnyLog-Network/data/prep', help='For file format, location where data will be stored')
   parser.add_argument('-m', '--mode',         type=str,    default='streaming',  choices=['file', 'streaming'],     help='insert type') 
   parser.add_argument('-r', '--repeat',       type=int,    default=1,            help='number of iterations. IF set to 0 run continuesly') 
   parser.add_argument('-s', '--sleep',        type=float,  default=0,            help='wait between insert') 
   args = parser.parse_args()

   args.location = os.path.expanduser(os.path.expandvars(args.location))
   if not os.path.isdir(args.location):
      os.makedirs(args.location) 

   if args.repeat == 0: 
      while True: 
         conn = random.choice(args.conns.split(','))
         header, payloads = switch_get_data(args.dbms, args.sensor, args.mode,  args.sleep)
         switch_store_data(args.store_format, args.location, args.sensor, conn, header, payloads)
         time.sleep(args.sleep) 
   else: 
      for i in range(args.repeat): 
         conn = random.choice(args.conns.split(','))
         header, payloads = switch_get_data(args.dbms, args.sensor, args.mode, args.sleep)
         switch_store_data(args.store_format, args.location, args.sensor, conn, header, payloads)

         time.sleep(args.sleep) 

if __name__ == '__main__': 
   main() 

