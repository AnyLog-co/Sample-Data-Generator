# Data Generator 

**Data Sets**: 
* [Random](source/southbound/random_data.py) - timestamp / value logic 
  * PUT 
  * POST
  * MQTT
* [Wind Turbine](data_generators/wind_turbine.py) - wind turbine data, split into multiple tables 
  * POST
  * MQTT
* [Rig Data](data_generators/rig_data.py) - rig data, one large table for different rig(s)
  * POST 
  * MQTT
* [Boats](data_generators/vessels_main.py) - Vesel data split into DLB (Port) and DLT (Starborn)
  * POST
  * MQTT
* [Proveit](data_generators/proveit_data.py) - Factory data from Proveit 2026 conference 
  * MQTT 
  * OPC-UA 
  * POST
