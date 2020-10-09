import argparse
import datetime 
import json 
import os 
import random
import requests 
import time 
import rest_commands

def get_machine_data(conn:str, dbms:str, mode:str): 
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
   rest_commands.send_data(conn, header, payload) 
   #print(payload) 

def get_ping_sensor(conn:str, dbms:str, mode:str):
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
   rest_commands.send_data(conn, header, payload) 
   #print(payload) 

def get_trig(conn:str, dbms:str, mode:str, sensor:str, sleep:float): 
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

   if len(payloads) > 0: 
      for payload in payloads: 
         rest_commands.send_data(conn, header, payload) 
         #print(payload) 

def switch(conn:str, dbms:str, mode:str, sensor:str, sleep:float=None): 
   """
   Based on if/else cases get data
   :args:
      conn:str - connection info
      dbms:str - database name 
      mode:str - insert mode
      sensor:str - sensor name
      sleep:float - wait between each get [get_trig only] 
   """
   if sensor == "machine": 
      get_machine_data(conn, dbms, mode)
   elif sensor == "ping": 
      get_ping_sensor(conn, dbms, mode) 
   else: 
      get_trig(conn, dbms, mode, sensor, sleep) 
       
def main(): 
   """
   Generate data into database via REST 
   :positional arguments:
      conn:str - REST host and port
      dbms:str - database name
      sensor:str - type of sensor to get data from 
         * machine - boot time, cpu useage, swap memory percentage, disk useage percentege 
         * ping - information regarding a PING sensor randomly selected form list 
         * sin - sinsign values over time 
         * cos - cossign values over time 
   :optional arguments:
      -h, --help  - show this help message and exit
      -m, --mode MODE:str - insert type (default: streaming) 
         * streaming - insert data in memory once memory is full or after N seconds (configrured on AnyLog) 
         * file - insert data one by one 
      -r, --repeat REPEAT:int - number of iterations. If set to 0 run continuesly (default: 1)
      -s, --sleep SLEEP:float - wait between insert (default: 0)
   """
   parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
   parser.add_argument('conn',           type=str,   default='127.0.0.1:2049',                                  help='REST host and port')
   parser.add_argument('dbms',           type=str,   default='alioi',                                           help='database name') 
   parser.add_argument('sensor',         type=str,   default='ping', choices=['machine', 'ping', 'sin', 'cos'], help='type of sensor to get data from') 
   parser.add_argument('-m', '--mode',   type=str,   default='streaming',  choices=['file', 'streaming'], help='insert type') 
   parser.add_argument('-r', '--repeat', type=int,   default=1,                                           help='number of iterations. IF set to 0 run continuesly') 
   parser.add_argument('-s', '--sleep',  type=float, default=0,                                           help='wait between insert') 
   args = parser.parse_args()

   conns = [] 
   for conn in args.conn.split(','):
       try: 
          status = rest_commands.validate(conn) 
       except: 
          pass 
       else: 
          if status == True: 

             conns.append(conn)
   if len(conns) == 0:
      print('Unable to accses any node') 
      exit(1) 

   if args.repeat == 0: 
      while True: 
         conn = random.choice(conns)
         switch(conn, args.dbms, args.mode, args.sensor, args.sleep)
         time.sleep(args.sleep)

   for i in range(args.repeat): 
      conn = random.choice(conns)
      switch(conn, args.dbms, args.mode, args.sensor, args.sleep)
      time.sleep(args.sleep)
 
if __name__ == '__main__': 
   main() 

