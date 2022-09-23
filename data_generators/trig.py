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


def trig_value(array_counter:int)->dict:
   """
   Calculate sin, cosin and tangent value for VALUE_ARRAY[array_counter]
   :args:
      array_counter:int - placeholder in VALUE_ARRAY
   :return:
      dict object sin, cosin and tangent for VALUE_ARRAY[array_counter]
   """
   return {
      'sin': math.sin(VALUE_ARRAY[row_counter]),
      'cos': math.cos(VALUE_ARRAY[row_counter]),
      'tan': math.tan(VALUE_ARRAY[row_counter])
   }

