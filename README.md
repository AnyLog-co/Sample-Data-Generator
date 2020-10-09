```
python3 rest_data_generator.py  --help
:positional arguments:
  conn:str - REST host and port   [ex. 10.0.0.96:2049] 
  dbms:str - database name        [ex. sample_data] 
  sensor:str - type of sensor to get data from 
     * machine - general data regarding the machine 
     * ping - data from random devices generating "ping" data 
     * sin - SIN-sign values 
     * cos - COS-sign values  
:optional arguments:
  -h, --help - show this help message and exit
  -m, --mode - insert type (default: streaming)
     * streaming - store batches of data 
     * file - store data as it comese 
  -r, --repeat - number of iterations. IF set to 0 run continuesly (default: 1)
  -s, --sleep - wait between insert (default: 0)
```
