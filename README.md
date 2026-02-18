# Data Generator 

```tree
├── source
│   ├── northbound - publish funcctions (POST, PUT, MQTT, OPC-UA)
│   ├── policies   - uns and `run msg client` policies + commands  
│   └── southbound - data generators (rand, wind_turbine, rig, vessels, proveit) 
├── support.py - reusable support functions
├── data_generator_main.py - data generator main 
├── uns_policies.py - UNS generator main
└── mapping_polciies.py - `run msg client` main
```

**Todo**
1. northbound data publishing 
2. ~~southbound data generator~~
3. `run msg client` per data generator 
4. `uns` policies generator for each data generator


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
