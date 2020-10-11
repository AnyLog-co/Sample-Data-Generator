import argparse
import datetime 
import json 
import os 
import random
import requests 
import time 
import store_data_options

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

   return header, payloads
      

def switch_get_data(dbms:str, sensor:str, mode:str, insert_size:int, sleep:float)->(dict, list):
   """
   Switch to get data based on sensor
   :args:
      dbms:str - logical database name 
      sensor:str - sensor to get data from 
      mode:str - mode to store data 
      insert_size:float - number of rows to generate
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
   for i in range(insert_size): 
      paylaod = None 
      if sensor == 'machine': 
         header, payload = get_machine_data(dbms, mode)         
      elif sensor == 'ping': 
         header, payload = get_ping_sensor(dbms, mode)
      else: 
         header, payload = get_trig(dbms, sensor, mode, sleep)

      if sensor == 'sin' or sensor == 'cos': 
         for val in payload: 
             data_list.append(payload)
      else: 
         data_list.append(payload) 
   return header, data_list

def switch_store_data(store_format:str, sensor:str, conn:str, header:dict, payloads:list): 
   """
   Switch to store data
   :args:
      store_format:str - format to store data 
      conn:str - connection info 
      header:dict - header for query
      payload:dict - data to store in operator
   """
   if store_format == 'rest': 
      if store_data_options.validate_connection(conn) == True: 
         for payload in payloads: 
            if sensor == 'sin' or sensor == 'cos': 
               for pyload in payload: 
                  store_data_options.send_data(conn, header, pyload) 
            else:
               store_data_options.send_data(conn, header, payload) 
   elif store_format == 'file': 
      for payload in payloads: 
         if sensor == 'sin' or sensor == 'cos': 
               for pylaod in payload: 
                  store_data_options.write_data(header, pyload) 
         else:
            store_data_options.write_data(header, payload)
   else: 
      for payload in payloads: 
         if sensor == 'sin' or sensor == 'cos': 
            for pyload in payload: 
               store_data_options.print_data(pyload) 
         else:
            store_data_options.print_data(payload)

def main(): 
   """
   Generate data into database via REST 
   :positional arguments:
      conn:str   - REST host and port
      dbms:str   - database name
      sensor:str - type of sensor to get data from 
         * machine - boot time, cpu useage, swap memory percentage, disk useage percentege 
         * ping    - information regarding a PING sensor randomly selected form list 
         * sin     - sinsign values over time 
         * cos     - cossign values over time 
   :optional arguments:
      -h, --help                            - show this help message and exit
      -i, --insert-size INSERT_SIZE:int     - number of row set per iterattion (default: 10)
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
   parser.add_argument('sensor', type=str, default='ping',  choices=['machine', 'ping', 'sin', 'cos'], help='type of sensor to get data from') 
   parser.add_argument('-i', '--insert-size',  type=int,    default=10,           help='number of row set per iterattion')  
   parser.add_argument('-f', '--store-format', type=str,    default='rest',       choices=['rest', 'file', 'print'], help='format to get data') 
   parser.add_argument('-m', '--mode',         type=str,    default='streaming',  choices=['file', 'streaming'],     help='insert type') 
   parser.add_argument('-r', '--repeat',       type=int,    default=1,            help='number of iterations. IF set to 0 run continuesly') 
   parser.add_argument('-s', '--sleep',        type=float,  default=0,            help='wait between insert') 
   args = parser.parse_args()

   if args.repeat == 0: 
      while True: 
         conn = random.choice(args.conns.split(','))
         header, payloads = switch_get_data(args.dbms, args.sensor, args.mode, args.insert_size, args.sleep)
         switch_store_data(args.sensor, rgs.store_format, conn, header, payload)
         time.sleep(args.sleep) 
   else: 
      for i in range(args.repeat): 
         conn = random.choice(args.conns.split(','))
         header, payloads = switch_get_data(args.dbms, args.sensor, args.mode, args.insert_size, args.sleep)
         switch_store_data(args.sensor, args.store_format, conn, header, payloads)
         time.sleep(args.sleep) 

if __name__ == '__main__': 
   main() 

