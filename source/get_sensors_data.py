import datetime
import grovepi 
import socket 
import  uuid 

DHT_GROVE_PIN = 7
DHT_VERSION = 0 

LIGHT_GROVE_PIN = 2 
SOUND_GROVE_PIN = 0 
BUTTON_GROVE_PIN = 3

def get_ip()->str:
   """
   Get IP address of given node to know source of sensor
   :return: 
      IP Address 
   """
   s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

   s.connect(("8.8.8.8", 80))

   return str(s.getsockname()[0])

def get_dht():
   try:  
      return grovepi.dht(DHT_GROVE_PIN, DHT_VERSION)
   except: 
      return False

def get_dht_f():
   try: 
      temp, humidity = grovepi.dht(DHT_GROVE_PIN, DHT_VERSION)
   except: 
      return False 

   return (temp * 1.8) + 32, humidity 

def get_light_levels():
   """
   Get light sensor value and resistence 
   :return: 
      sensor value
      resistance level
   """
   grovepi.pinMode(LIGHT_GROVE_PIN,"INPUT")
   try:
      sensor_value = grovepi.analogRead(LIGHT_GROVE_PIN)
   except: 
      return False

   resistance = (float)(1023 - sensor_value) * 10 / sensor_value

   return sensor_value, resistance

def get_sound_levels():
   grovepi.pinMode(SOUND_GROVE_PIN, "INPUT")
   try:
      return grovepi.analogRead(SOUND_GROVE_PIN)
   except: 
      return False 

def get_button():
   grovepi.pinMode(BUTTON_GROVE_PIN, "INPUT") 
   try: 
      return grovepi.digitalRead(BUTTON_GROVE_PIN)
   except: 
      return 0

def main(sensor:str): 
   sensors = {
      'dht': get_dht,
      'dht_f': get_dht_f, 
      'light': get_light_levels, 
      'sound': get_sound_levels 
   }

   try:
      sensor_cmd = sensors[sensor]
   except KeyError: 
      return False 

   data = {} 
   data['key'] = str(uuid.uuid4())
   data['timestamp'] = str(datetime.datetime.now())
   data['sensor'] = sensor 
   data['location'] = get_ip() 
   if sensor == "dht" or sensor == "dht_f": 
      try: 
         temp, humidity = sensor_cmd()
      except: 
         return False 
      data['readings'] = {
         'humidity': humidity, 
         'temp': temp
      } 
   elif sensor == "light": 
      try: 
          sensor_value, resistance = sensor_cmd()
      except:
         return False 

      data['readings'] = {
         'level': sensor_value, 
         'resistance': resistance 
      }

   else: 
      try: 
          data[sensor]  = sensor_cmd()
      except: 
         return False 

   return data 
   
if __name__ == '__main__': 
   main('sound') 
