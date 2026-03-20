#!/bin/bash

# Vessel Data
/root/Sample-Data-Generator/venv/bin/python3 $HOME/Sample-Data-Generator/data_generator_main.py \
  --data-conn anyloguser:mqtt4AnyLog!@172.104.228.251:1883 \
  --db-name anotherpeak \
  --skip-msg-client \
  --repeat 0 vessel mqtt &

# Rig Data
/root/Sample-Data-Generator/venv/bin/python3 $HOME/Sample-Data-Generator/data_generator_main.py \
  --data-conn anyloguser:mqtt4AnyLog!@172.104.228.251:1883 \
  --db-name timbergrove_rigs \
  --skip-msg-client \
  --repeat 0 rig mqtt &

# Wind Turbine
/root/Sample-Data-Generator/venv/bin/python3 $HOME/Sample-Data-Generator/data_generator_main.py \
  --data-conn anyloguser:mqtt4AnyLog!@172.104.228.251:1883 \
  --db-name wind_turbine \
  --skip-msg-client \
  --repeat 0 wind-turbine mqtt &

# Random Data
/root/Sample-Data-Generator/venv/bin/python3 $HOME/Sample-Data-Generator/data_generator_main.py \
  --data-conn anyloguser:mqtt4AnyLog!@172.104.228.251:1883 \
  --db-name mydb \
  --skip-msg-client \
  --repeat 0 random mqtt &

# IMPORTANT: keep service running
wait
