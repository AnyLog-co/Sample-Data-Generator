# Vessel Data
python3 $HOME/Sample-Data-Generator/venv/data_generator_main.py \
  --data-conn anyloguser:mqtt4AnyLog!@172.104.228.251:1883 \
  --db-name anotherpeak \
  --skip-msg-client \
  --repeat 0 vessel mqtt

# Rig Data
python3 $HOME/Sample-Data-Generator/venv/data_generator_main.py \
  --data-conn anyloguser:mqtt4AnyLog!@172.104.228.251:1883 \
  --db-name anotherpeak \
  --skip-msg-client \
  --repeat 0 rig mqtt

python3 $HOME/Sample-Data-Generator/venv/data_generator_main.py \
  --data-conn anyloguser:mqtt4AnyLog!@172.104.228.251:1883 \
  --db-name anotherpeak \
  --skip-msg-client \
  --repeat 0 wind-turbine mqtt

