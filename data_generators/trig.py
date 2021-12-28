"""
The following generatees data between -pi and pi in terms of 
- sin 
- cos 
- random value between the two 
"""

import math
import os
import sys
import time

ROOT_PATH = os.path.dirname(os.path.abspath(__file__)).rsplit('data_generators', 1)[0]
PROTOCOLS = os.path.join(ROOT_PATH, 'protocols')
sys.path.insert(0, PROTOCOLS)
from support import generate_timestamp


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


def trig_value(timezone:str, sleep:float, repeat:int)->dict:
   """
   Calculate the sin/cos values between -π to π and π to -π
   :args:
      timezone:str - timezone for generated timestamp(s)
      sleep:float - wait time between each iteration
      repeat:int - number of iterations
   :params:
      payloads:dict - sin/cos data to store
   :return:
      payloads
   """
   payloads = {'sin': [], 'cos': []}
   for i in range(repeat):
      for value in VALUE_ARRAY:
         timestamp = generate_timestamp(timezone=timezone)
         payloads['sin'].append({
               'timestamp': timestamp,
               'value': math.sin(value)
         })
         payloads['cos'].append({
            'timestamp': timestamp,
            'value': math.sin(value)
         })
         time.sleep(sleep)

   return payloads



if __name__ == '__main__':
   print(trig_value(0.5, 10))