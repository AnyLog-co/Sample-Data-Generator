import grovepi 

DHT_GROVE_PIN = 8
DHT_VERSION = 0 

LIGHT_GROVE_PIN = 2 
SOUND_GROVE_PIN = 0 
BUTTON_GROVE_PIN = 3

def get_humidity():
   """
   Get Humidity Percentage 
   :return: 
      humidity as a percentage 
   """
   try: 
      return grovepi.dht(DHT_GROVE_PIN, DHT_VERSION)[1]
   except: 
      return None

def get_temp_c():
   """
   Get Temperature in Celcius
   :return: 
      temperature in celcius
   """
   try: 
      return grovepi.dht(DHT_GROVE_PIN, DHT_VERSION)[0]
   except: 
      return None

def get_temp_f():
   """
   Get Temperature in Fahrenheit
   :return: 
      temp in fahrenheit
   """
   try: 
      temp = grovepi.dht(DHT_GROVE_PIN, DHT_VERSION)[0]
   except: 
       return None 

   return (temp * 1.8) + 32

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
      return None

   resistance = (float)(1023 - sensor_value) * 10 / sensor_value

   return sensor_value, round(resistance, 2)


def get_sound_levels():
   grovepi.pinMode(SOUND_GROVE_PIN, "INPUT")
   try:
      print(grovepi.analogRead(SOUND_GROVE_PIN))
   except: 
      print(False) 

def get_button():
   grovepi.pinMode(BUTTON_GROVE_PIN, "INPUT") 
   try: 
      return grovepi.digitalRead(BUTTON_GROVE_PIN)
   except: 
      return 0

if __name__ == '__main__': 
   print(get_button())
