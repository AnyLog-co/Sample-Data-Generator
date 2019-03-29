import os 
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
   if not os.path.isdir(data_dir):
      return False 
   data_dir_out = os.path.expanduser(os.path.expandvars(data_dir_out))
   if not os,path.isdir(data_dir): 
      return False
   
   # iterate 
   for iteration in range(iterations):
      # create file 
      file_name_in = create_file(sensor, data_dir_in)
      if file_name_in is False:
         return False 
      file_name_out = file_name_in.replace(data_dir_in, data_dir, out)

      # store data in file 
      for num_line in range(num_lines):
         status = store_in_file(sensor, file_name) 
         if status is False: 
            return False 
      move_data(file_name_in, file_name_out) 
      
   return True 

if __name__ == '__main__':
   import argparse
   parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
   parser.add_argument('-sensor',       "--sensor",      type=str,  default="light",       help="sensor name")
   parser.add_argument("-iterations",   "--iterations",  type=int,  default=1,             help="number of iterations")
   parser.add_argument("-num-lines",    "--num-lines",    type=int, default=10,            help="number of lines in file ")  
   parser.add_argument("-data-dir-in",  "--data-dir-in",  type=str, default="$HOME/test",  help="directory where data is generated in")
   parser.add_argument("-data-dir-out", "--data-dir-out", type=str, default="$HOME/test2", help="directory where data ready to be sent is stored") 
   args = parser.parse_args()
   print(generate_data_main(args.sensor, args.iterations, args.num_lines, args.data_dir_in, args.data_dir_out)) `
