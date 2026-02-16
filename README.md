# Data Generator 

**Data Sets**: 
* [Random](mains/random_data.py) - timestamp / value logic 
  * PUT 
  * POST
  * MQTT
* [Wind Turbine](mains/wind_turbine.py) - wind turbine data, split into multiple tables 
  * POST
  * MQTT
* [Rig Data](mains/rig_data.py) - rig data, one large table for different rig(s)
  * POST 
  * MQTT
* [Boats](mains/veselles_data.py) - Vesel data split into DLB (Port) and DLT (Starborn)
  * POST
  * MQTT
* [Proveit](mains/proveit_data.py) - Factory data from Proveit 2026 conference 
  * MQTT 
  * OPC-UA 
  * POST
