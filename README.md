The following is a support script to generate data for  AnyLog. A user has an option to recieve data via REST, print and file 
   * For ping and machine data generate 10 rows for each iteration 
   * For sin/cos data generate 30 rows for each iteraton, between -π and π   

# Requirements 
   * [psutil](https://pypi.org/project/psutil/)
   * [requests](https://pypi.org/project/requests/) 

# Sample Data 
   * machine (**Table Name**: `machine_data`) - using psutil, provide information regarding a machine 
   ```
   {"timestamp": "2020-10-11 03:25:53.698126", "boot_time": 2739.6981489658356, "cpu_percentge": 0.0, "swap_memory": 0.0, "disk_useage": 0.0}    
   ```
   
   * ping (**Table Name**: `ping_sensor`) - values from an array of devices that generate ping sensor data 
   ```
   {"timestamp": "2020-10-11 03:15:11.078921", "device_name": "Ubiquiti OLT", "parentelement": "9a62728a-1a14-42e1-8c79-16fa7b37223f", "webid": "F1AbEfLbwwL8F6EiShvDV-QH70Ay9wV1b5Y6hG0bdSFZFT0ugxACfpGU7d1ojPpadLPwI4gWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxVQklRVUlUSSBPTFR8UElORw", "value": 0}
   {"timestamp": "2020-10-11 03:15:11.078978", "device_name": "VM Lit SL NMS", "parentelement": "031eabf8-740f-4f8f-bcaf-cf0fc75a0a12", "webid": "F1AbEfLbwwL8F6EiShvDV-QH70ATrGzGrGT6RG0ZdSFZFT0ugQW05a2rwdFojNpadLPwI4gWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxGLk8gTU9OSVRPUklORyBTRVJWRVJcVk0gTElUIFNMIE5NU3xQSU5H", "value": 1}
   {"timestamp": "2020-10-11 03:15:11.078992", "device_name": "ADVA FSP3000R7", "parentelement": "d4157fd9-1c34-4a0e-a55a-5ba3035d4590", "webid": "F1AbEfLbwwL8F6EiShvDV-QH70AkxjnYuCS6RG0ZdSFZFT0ugnMRtEzvxdFojNpadLPwI4gWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxBRFZBIEZTUDMwMDBSN3xQSU5H", "value": 1}
   {"timestamp": "2020-10-11 03:15:11.079002", "device_name": "Catalyst 3500XL", "parentelement": "ee3cd571-019e-4ef6-b64a-4529c637fcb3", "webid": "F1AbEfLbwwL8F6EiShvDV-QH70A74uuaOGS6RG0ZdSFZFT0ug4FckGTrxdFojNpadLPwI4gWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxDQVRBTFlTVCAzNTAwWEx8UElORw", "value": 9}
   {"timestamp": "2020-10-11 03:16:29.612628", "device_name": "GOOGLE_PING", "parentelement": "c98f8555-32ac-4bb4-8acd-f39c1201174a", "webid": "F1AbEfLbwwL8F6EiShvDV-QH70AMgi98B6o6hG0bdSFZFT0ugPdQ3gcXLd1ojPpadLPwI4gWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xHT09HTEVfUElOR3xQSU5H", "value": 23}  
   ```

   * sin (**Table Name**: `sin_data`) - sin values betweeen -π and π 
   ```
   {"timestamp": "2020-10-11 03:35:51.893689", "value": -1.2246467991473532e-16}
   {"timestamp": "2020-10-11 03:35:51.893723", "value": -1.0}
   {"timestamp": "2020-10-11 03:35:51.893730", "value": -0.8660254037844386}
   {"timestamp": "2020-10-11 03:35:51.893735", "value": -0.8414709848078965}
   {"timestamp": "2020-10-11 03:35:51.893739", "value": -0.7071067811865475}
   {"timestamp": "2020-10-11 03:35:51.893743", "value": -0.49999999999999994}
   {"timestamp": "2020-10-11 03:35:51.893747", "value": -0.3826834323650898}
   {"timestamp": "2020-10-11 03:35:51.893809", "value": 0.0}
   {"timestamp": "2020-10-11 03:35:51.893817", "value": 0.3826834323650898}
   {"timestamp": "2020-10-11 03:35:51.893822", "value": 0.49999999999999994}
   {"timestamp": "2020-10-11 03:35:51.893826", "value": 0.7071067811865475}
   {"timestamp": "2020-10-11 03:35:51.893830", "value": 0.8414709848078965}
   {"timestamp": "2020-10-11 03:35:51.893834", "value": 0.8660254037844386}
   {"timestamp": "2020-10-11 03:35:51.893838", "value": 1.0}
   {"timestamp": "2020-10-11 03:35:51.893842", "value": 1.2246467991473532e-16}
   {"timestamp": "2020-10-11 03:35:51.893847", "value": 1.2246467991473532e-16}
   {"timestamp": "2020-10-11 03:35:51.893851", "value": 1.0}
   {"timestamp": "2020-10-11 03:35:51.893855", "value": 0.8660254037844386}
   {"timestamp": "2020-10-11 03:35:51.893859", "value": 0.8414709848078965}
   {"timestamp": "2020-10-11 03:35:51.893863", "value": 0.7071067811865475}
   {"timestamp": "2020-10-11 03:35:51.893867", "value": 0.49999999999999994}
   {"timestamp": "2020-10-11 03:35:51.893871", "value": 0.3826834323650898}
   {"timestamp": "2020-10-11 03:35:51.893875", "value": 0.0}
   {"timestamp": "2020-10-11 03:35:51.893879", "value": -0.3826834323650898}
   {"timestamp": "2020-10-11 03:35:51.893883", "value": -0.49999999999999994}
   {"timestamp": "2020-10-11 03:35:51.893890", "value": -0.7071067811865475}
   {"timestamp": "2020-10-11 03:35:51.893894", "value": -0.8414709848078965}
   {"timestamp": "2020-10-11 03:35:51.893899", "value": -0.8660254037844386}
   {"timestamp": "2020-10-11 03:35:51.893903", "value": -1.0}
   {"timestamp": "2020-10-11 03:35:51.893907", "value": -1.2246467991473532e-16}
   ```

   * cos (**Table Name**: `cos_data`) - cosin valus between -π and π 
   ```
   {"timestamp": "2020-10-11 03:40:37.720501", "value": -1.0}
   {"timestamp": "2020-10-11 03:40:37.720531", "value": 6.123233995736766e-17}
   {"timestamp": "2020-10-11 03:40:37.720543", "value": 0.5000000000000001}
   {"timestamp": "2020-10-11 03:40:37.720548", "value": 0.5403023058681398}
   {"timestamp": "2020-10-11 03:40:37.720552", "value": 0.7071067811865476}
   {"timestamp": "2020-10-11 03:40:37.720557", "value": 0.8660254037844387}
   {"timestamp": "2020-10-11 03:40:37.720561", "value": 0.9238795325112867}
   {"timestamp": "2020-10-11 03:40:37.720565", "value": 1.0}
   {"timestamp": "2020-10-11 03:40:37.720569", "value": 0.9238795325112867}
   {"timestamp": "2020-10-11 03:40:37.720573", "value": 0.8660254037844387}
   {"timestamp": "2020-10-11 03:40:37.720577", "value": 0.7071067811865476}
   {"timestamp": "2020-10-11 03:40:37.720580", "value": 0.5403023058681398}
   {"timestamp": "2020-10-11 03:40:37.720584", "value": 0.5000000000000001}
   {"timestamp": "2020-10-11 03:40:37.720588", "value": 6.123233995736766e-17}
   {"timestamp": "2020-10-11 03:40:37.720592", "value": -1.0}
   {"timestamp": "2020-10-11 03:40:37.720596", "value": -1.0}
   {"timestamp": "2020-10-11 03:40:37.720600", "value": 6.123233995736766e-17}
   {"timestamp": "2020-10-11 03:40:37.720605", "value": 0.5000000000000001}
   {"timestamp": "2020-10-11 03:40:37.720608", "value": 0.5403023058681398}
   {"timestamp": "2020-10-11 03:40:37.720612", "value": 0.7071067811865476}
   {"timestamp": "2020-10-11 03:40:37.720616", "value": 0.8660254037844387}
   {"timestamp": "2020-10-11 03:40:37.720620", "value": 0.9238795325112867}
   {"timestamp": "2020-10-11 03:40:37.720624", "value": 1.0}
   {"timestamp": "2020-10-11 03:40:37.720628", "value": 0.9238795325112867}
   {"timestamp": "2020-10-11 03:40:37.720632", "value": 0.8660254037844387}
   {"timestamp": "2020-10-11 03:40:37.720638", "value": 0.7071067811865476}
   {"timestamp": "2020-10-11 03:40:37.720642", "value": 0.5403023058681398}
   {"timestamp": "2020-10-11 03:40:37.720646", "value": 0.5000000000000001}
   {"timestamp": "2020-10-11 03:40:37.720650", "value": 6.123233995736766e-17}
   {"timestamp": "2020-10-11 03:40:37.720654", "value": -1.0}
   ```

# How to use 
```
python3 data_generator.py  --help
   :positional arguments:
      conn:str   - REST host and port
      dbms:str   - database name
      sensor:str - type of sensor to get data from 
         * machine - boot time, cpu useage, swap memory percentage, disk useage percentege 
         * ping    - information regarding a PING sensor randomly selected form list 
         * sin     - sinsign values over time 
         * cos     - cossign values over time 
   :optional arguments:
      -h, --help                        show this help message and exit
      -f --store-format FILE_FORMAT     format to get data 
                                            choices: {rest,file,print}
                                            default: rest
      -l, --location    LOCATION        location where script is located, used for import
                                            default: /home/anylog/Sample-Data-Generator
      -m, --mode        MODE            insert type
                                            choices: {file,streaming}
                                            default: streaming
      -r, --repeat      REPEAT          number of iterations. If set to 0 run continuesly
                                            default: 1
      -s, --sleep       SLEEP           wait between insert 
                                            default: 0
      -p, --prep        PREP            Directoy where data is prepped when writing to fle
                                            default: $HOME/AnyLog-Network/data/prep
      -w, --watch       WATCH           When data in file is ready to be sent into AnyLog transfer from prep into this directory. 
                                        If set to 'None', file doesen't get sent. 
                                            default: None```
