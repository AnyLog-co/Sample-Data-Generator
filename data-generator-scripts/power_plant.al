#--------------------------------------------------------------------------------------------------------------------
# Extract PowerPlant  data from MQTT
# {
#   "monitor_id":"BSP","timestamp":"2026-04-09T00:58:48.1528120Z","A_Current":1,"A_N_Voltage":729,"B_Current":0,
#   "B_N_Voltage":733,"C_Current":0,"C_N_Voltage":733,"CommsStatus":"true","EnergyMultiplier":1,"Frequency":5999,
#   "PowerFactor":99,"ReactivePower":1,"RealPower":4
# }
#
# {"monitor_id":"InconLoadTapChangerAI","timestamp":"2026-04-09T01:04:22.5542990Z","PV":-1.9600000381469727}
#--------------------------------------------------------------------------------------------------------------------

<run msg client where
    broker=172.104.228.251 and port=1883 and
    user=anyloguser and password=mqtt4AnyLog! and
    log=false and topic=(
        name=power-plant and
        dbms=!default_dbms and
        table=pp_pm and
        column.timestamp.timestamp = "bring [timestamp]" and
        column.monitor_id.string = "bring [monitor_id]" and
        column.a_current.float = "bring [A_Current]" and
        column.a_n_voltage.float = "bring [A_N_Voltage]" and
        column.b_current.float = "bring [B_Current]" and
        column.b_n_voltage.float = "bring [B_N_Voltage]" and
        column.c_current.float = "bring [C_Current]" and
        column.c_n_voltage.float = "bring [C_N_Voltage]" and
        column.comms_status.bool = "bring [CommsStatus]" and
        column.energy_multiplier.float = "bring [EnergyMultiplier]" and
        column.frequency.float = "bring [Frequency]" and
        column.power_factor.float = "bring [PowerFactor]" and
        column.reactive_power.float = "bring [ReactivePower]" and
        column.real_power.float = "bring [RealPower]"
    ) and topic = (
        name = power-plant-pv and
        dbms = !default_dbms and
        table = pv and
        column.timestamp.timestamp = "bring [timestamp]" and
        column.monitor_id.string = "bring [monitor_id]" and
        column.pv.float = "bring [PV]"
    )>


