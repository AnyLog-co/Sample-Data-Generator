import grovepi 

GROVE_PIN_NUM = 8
DHT_VERSION = 0 

def get_humidity():
   """
   Get Humidity Percentage 
   :return: 
      humidity as a percentage 
   """
   try: 
      return grovepi.dht(GROVE_PIN_NUM, DHT_VERSION)[1]
   except: 
      return None

def get_temp_c():
   """
   Get Temperature in Celcius
   :return: 
      temperature in celcius
   """
   try: 
      return grovepi.dht(GROVE_PIN_NUM, DHT_VERSION)[0]
   except: 
      return None

def get_temp_f():
   """
   Get Temperature in Fahrenheit
   :return: 
      temp in fahrenheit
   """
   try: 
      temp = grovepi.dht(GROVE_PIN_NUM, DHT_VERSION)[0]
   except: 
       return None 

   return (temp * 1.8) + 32

if __name__ == '__main__': 
   print(get_temp_f())
