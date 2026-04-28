#--------------------------------------------------------------------------------------------------------------#
# Hardcoded call to the data generator for vessl (DLT + DLB)
#
# :Sample Data:
# {
#   "turbine_id": 6, "timestamp": "2026-04-05T17:48:40.156037", "wind_avg": 6.7, "wind_max": 10.8, "wind_min": 3.5,
#   "rpm_avg": 0.85, "rpm_max": 1.01, "rpm_min": 0.71, "power_avg": -8, "power_max": -4, "power_min": -12,
#   "avail_wind": 2.276, "avail_tech": 2.276, "avail_external": 2.276, "reactive_avg": 2, "reactive_max": 2,
#   "reactive_min": 2, "pitch_avg": 56.7, "precip_avg": 4, "precip_max": 4, "precip_min": 4, "ambient_avg": 244,
#   "icing_rate_avg": 21.6, "pressure_avg": 932, "humidity_avg": 2, "operating_hours": "786:27:00",
#   "nacelle_position": 107, "dbms": "wind_turbine", "table": "wind_turbine"
# }
#--------------------------------------------------------------------------------------------------------------#
# process !local_scripts/data-generator/wind_turbine_data.al

set debug on

on error ignore

:publish-policies:

process !local_scripts/data-generator/mapping/wind_turbine_available-power.al
process !local_scripts/data-generator/mapping/wind_turbine_blade-pitch.al
process !local_scripts/data-generator/mapping/wind_turbine_energy.al
process !local_scripts/data-generator/mapping/wind_turbine_reactive-power.al

:msg-client:
on error goto msg-client-error
<run msg client where
    broker=172.104.228.251 and port=1883 and
    user=anyloguser and password=mqtt4AnyLog! and
    log=false and topic=(
        name=wind-turbine/turbine-1 and
        policy = available-power and
        policy = blade-pitch and
        policy = energy and
        policy = reactive-power
    ) and topic=(
        name=wind-turbine/turbine-2 and
        policy = available-power and
        policy = blade-pitch and
        policy = energy and
        policy = reactive-power
    ) and topic=(
        name=wind-turbine/turbine-3 and
        policy = available-power and
        policy = blade-pitch and
        policy = energy and
        policy = reactive-power
    ) and topic=(
        name=wind-turbine/turbine-5 and
        policy = available-power and
        policy = blade-pitch and
        policy = energy and
        policy = reactive-power
    ) and topic=(
        name=wind-turbine/turbine-6 and
        policy = available-power and
        policy = blade-pitch and
        policy = energy and
        policy = reactive-power
    ) and topic=(
        name=wind-turbine/turbine-7 and
        policy = available-power and
        policy = blade-pitch and
        policy = energy and
        policy = reactive-power
    ) and topic=(
        name=wind-turbine/turbine-8 and
        policy = available-power and
        policy = blade-pitch and
        policy = energy and
        policy = reactive-power
    ) and topic=(
        name=wind-turbine/turbine-9 and
        policy = available-power and
        policy = blade-pitch and
        policy = energy and
        policy = reactive-power
    ) and topic=(
        name=wind-turbine/turbine-10 and
        policy = available-power and
        policy = blade-pitch and
        policy = energy and
        policy = reactive-power
    ) and topic=(
        name=wind-turbine/turbine-11 and
        policy = available-power and
        policy = blade-pitch and
        policy = energy and
        policy = reactive-power
    )>

get msg client

:end-script:
end script