"""
The following generatees data between -pi and pi in terms of 
- sin 
- cos 
- random value between the two 
"""
import datetime 
import math 
import random 
import time 

VALUE_ARRAY = [
   -1 * math.pi, -1 * math.pi/2, -1 * math.pi/3,
   -1,
   -1 * math.pi/4, -1 * math.pi/6, -1 * math.pi/8, 
   0, 
   math.pi/8, math.pi/6, math.pi/4, 
   1, 
   math.pi/3, math.pi/2, math.pi, 
   math.pi, math.pi/2, math.pi/3, 
   1, 
   math.pi/4, math.pi/6, math.pi/8, 
   0, 
   -1 * math.pi/8, -1 * math.pi/6, -1 * math.pi/4, 
   -1, 
   -1 * math.pi/3, -1 * math.pi/2, -1 * math.pi 
]

def sin_value(frequency:float, sleep:float)->list: 
   """
   Get SIN values 
   :args: 
      frequency:float - multiplication of generated value 
      sleep:float - wait time between each insert
   :param:
      timestamp:str
      value:float - value from VALUE_ARRAY 
      data:dict - data 
   :return: 
      list of values to insert
   """
   data_list = [] 
   for value in VALUE_ARRAY: 
      timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
      value = math.sin(value) * frequency  
      data_list.append({'timestamp': timestamp, 'value': value}) 
      time.sleep(sleep) 
   return data_list 

def cos_value(frequency:float, sleep:float)->list: 
   """
   Get COS values 
   :args: 
      frequency:float - multiplication of generated value 
      sleep:float - wait time between each insert
   :param:
      timestamp:str
      value:float - value from VALUE_ARRAY 
      data:dict - data 
   :return: 
      list of values to insert
   """
   data_list = [] 
   for value in VALUE_ARRAY: 
      timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
      value = math.cos(value) * frequency 
      data_list.append({'timestamp': timestamp, 'value': value}) 
      time.sleep(sleep) 
   return data_list  

def rand_value(frequency:float, sleep:float)->list: 
   """
   Get RAND values 
   :args: 
      frequency:float - multiplication of generated value 
      sleep:float - wait time between each insert
   :param:
      timestamp:str
      value:float - value from VALUE_ARRAY 
      data:dict - data 
   :return: 
      list of values to insert
   """
   data_list = [] 
   for value in VALUE_ARRAY: 
      timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
      value = value * random.random() * frequency 
      data_list.append({'timestamp': timestamp, 'value': value}) 
      time.sleep(sleep) 
   return data_list
