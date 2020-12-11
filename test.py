from data_generators import machine_info, percentagecpu_sensor, ping_sensor, trig
from protocols import rest_protocol,  store_data_options,  write_file


print(ping_sensor.get_ping_data()) 
print(percentagecpu_sensor.get_percentagecpu_data())

print(machine_info.get_device_data())

print(trig.sin_value(0))
print(trig.cos_value(0))
print(trig.rand_value(0))





