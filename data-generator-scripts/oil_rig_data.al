#--------------------------------------------------------------------------------------------------------------#
# Hardcoded call to the data generator for vessl (DLT + DLB)
#
# :Sample Data:
# {
#   "timestamp": "2026-04-05T21:33:38.592496", "rig_id": "RIG-TX-001", "rig_name": "Permian Star",
#   "location": "West Texas", "activity": "circulating", "measured_depth": "12518.66", "true_vertical_depth": "11036.81",
#   "rop": "0.0", "wob": "0.0", "rpm": "69.94", "torque": "8729.09", "standpipe_pressure": "3012.69",
#   "choke_pressure": "701.1", "flow_rate": "674.61", "hookload": "639.49", "bit_depth": "12518.66", "hole_depth":
#   "12521.27", "mud_weight_in": "9.88", "mud_weight_out": "9.83", "mud_temp_in": "88.18", "mud_temp_out": "112.04",
#   "total_gas": "50.02", "block_height": "47.52", "status": "idle", "dbms": "timbergrove_rigs", "table": "rig_data"
# }
#--------------------------------------------------------------------------------------------------------------#
# process !local_scripts/data-generator/oil_rig_data.al

on error ignore

:publish-policies:

process !local_scripts/data-generator/mapping/rig_rig-data.al

:msg-client:
on error goto msg-client-error
<run msg client where
    broker=172.104.228.251 and port=1883 and
    user=anyloguser and password=mqtt4AnyLog! and
    log=false and topic=(
        name=rig-data/rig-1 and
        policy = rig-data
    ) and topic=(
        name=rig-data/rig-7 and
        policy = rig-data
    ) and topic=(
        name=rig-data/rig-12 and
        policy = rig-data
    ) and topic=(
        name=rig-data/rig-23 and
        policy = rig-data
    ) and topic=(
        name=rig-data/rig-31 and
        policy = rig-data
    ) and topic=(
        name=rig-data/rig-44 and
        policy = rig-data
    )>

get msg client

:end-script:
end script