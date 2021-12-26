"""
The following generatees data between -pi and pi in terms of 
- sin 
- cos 
- random value between the two 
"""
import datetime 
import math 
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


def trig_value(sleep:float, repeat:int)->dict:
   """
   Calculate the sin/cos values between -π to π and π to -π
   :args:
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
         timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
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