import ast 
import json 
import os 

def read_file(file_name:str)->list:
   """
   Read data from file
   :args:
      file_name:str - file to read 
   :params: 
      data:list - data from file
   """
   data = [] 
   status = True
   try:
      file_name = os.path.expandvars(os.path.expanduser(file_name)) 
   except Exception as e:
      print('Failed to generate path for %s (Error: %s)' % (file_name, e))
      status = False  

   if not os.path.isfile(file_name): 
      print('Error: File %s not found' % file_name)
      status = False 
   
   if status is True: 
      with open(file_name, 'r') as f: 
         for line in f.read().split('\n'): 
            if line != '\n' and isinstance(ast.literal_eval(line), dict):
               data.append(line)
   return data
