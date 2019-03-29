import datetime 
import os 

from get_sensors_data.py import get_sensor_data

def create_file(sensor:str, data_dir:str): 
   """
   create new file 
   :param: 
      sensor:str - sensor name 
      data_dir_in:str - directory where data is generated in
   :return: 
      file_name is success, else False 
   """ 
   file_name = "%s/%s_%s_sensor.txt" % (data_dir, datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%s'), sensor)   
   try: 
      open(file_name, 'w').close() 
   except: 
      return False 
   return file_name 

def store_in_file(sensor:str, file_name:str):
   """
   store data in file
   :param: 
      sensor:str - sensor name 
      file_name:str - file to store data in 
   :return: 
      if succeed return True, else False 
   """
   # get data 
   data =  get_sensor_data(sensor) 
   if data is False: 
      return False 

   # store in file 
   try:
      with open(file_name, 'a') as f: 
         f.write(data+"\n")
   except:
      return False 
   return  True  

def move_data(file_name_in, file_name_out): 
   """
   Move data to dir ready to be sent to AnyLog 
   :param: 
      file_name_in:str - source where data was generated 
      file_name_out:str - location where data is stored while waiting to be sent to DB
   :return: 
      return True if succeed else False 
   """
   try: 
      os.rename(file_name_in,file_name_out)
   except: 
      return False 
   return True 

def generate_data_main(sensor:str, iterations:int, num_lines:int, data_dir_in:str, data_dir_out:str):
   """
   generate data main
   :param:
      sensor:str - sensor name 
      iterations:int - number of iterations 
      num_lines:int - number of lines in file 
      data_dir_in:str - directory where data is generated in
      data_dir_out:str - rdirectory where data ready to be sent is stored
   :return: 
      if success return True 
      Else return False 
   """
   # creat3e in/out  dirs 
   data_dir_in = os.path.expanduser(os.path.expandvars(data_dir_in))
   if os.path.isdir(data_dir) is False:
      return False 
   data_dir_out = os.path.expanduser(os.path.expandvars(data_dir_out))
   if os.path.isdir(data_dir) is False: 
      return False
   
   # iterate 
   for iteration in range(iterations):
      # create file 
      file_name_in = create_file(sensor, data_dir_in)
      if file_name_in is False:
         return False 
      file_name_out = file_name_in.replace(data_dir_in, data_dir_out)

      # store data in file 
      for num_line in range(num_lines):
         status = store_in_file(sensor, file_name) 
         if status is False: 
            return False 
      move_data(file_name_in, file_name_out) 
      
   return True 

if __name__ == '__main__':
   """
   Code to allow user to run code manually
   """
   import argparse
   parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
   parser.add_argument('-sensor',       "--sensor",      type=str,  default="light",       help="sensor name")
   parser.add_argument("-iterations",   "--iterations",  type=int,  default=1,             help="number of iterations")
   parser.add_argument("-num-lines",    "--num-lines",    type=int, default=10,            help="number of lines in file ")  
   parser.add_argument("-data-dir-in",  "--data-dir-in",  type=str, default="$HOME/test",  help="directory where data is generated in")
   parser.add_argument("-data-dir-out", "--data-dir-out", type=str, default="$HOME/test2", help="directory where data ready to be sent is stored") 
   args = parser.parse_args()
   print(generate_data_main(args.sensor, args.iterations, args.num_lines, args.data_dir_in, args.data_dir_out))
