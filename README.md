# Sample Data Generator
Sample data generators used to insert data into AnyLog. 

At AnyLog we use this package (in addition to third-party partners) to generate our demos.   

## Requirements  
**Manual Deployment**: 
* python3 
  * pytz
  * requests
  * paho-mqtt (installed only when sending data via MQTT)
  * opencv (installed only when sending video data _or_ conversion type if OpenCV)
  * numpy (installed only when sending video data _or_ conversion type if OpenCV)
  * tensorflow (installed only when sending video data)
  
**Docker**: In a Docker deployment, packages get installed based on the user configurations, as such the final image 
size can range from XXX to XXX. 

## Data


