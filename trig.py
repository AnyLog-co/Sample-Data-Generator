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

def sin_value(sleep:float)->list: 
   """
   Get SIN values 
   :args: 
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
      value = math.sin(value) 
      data_list.append({'timestamp': timestamp, 'value': value}) 
      time.sleep(sleep) 
   return data_list 

def cos_value(sleep:float)->list: 
   """
   Get COS values 
   :args: 
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
      value = math.cos(value) 
      data_list.append({'timestamp': timestamp, 'value': value}) 
      time.sleep(sleep) 
   return data_list  

def rand_value(sleep:float)->list: 
   """
   Get RAND values 
   :args: 
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
      value = value * random.random()  
      data_list.append({'timestamp': timestamp, 'value': value}) 
      time.sleep(sleep) 
   return data_list
