# trig
<run mqtt client where broker=rest and port=!anylog_rest_port and user-agent=anylog and log=false and topic=(
    name=trig_data and
    dbms="bring [dbms]" and
    table="bring [table]" and
    column.timestamp.timestamp="bring [timestamp]" and
    column.value=(value="bring [value]" and type=float) and
    column.sin=(value="bring [sin]" and type=float) and
    column.cos=(value="bring [cos]" and type=float) and
    column.tan=(value="bring [tan]" and type=float)
)>

# performance
<run mqtt client where broker=rest and port=!anylog_rest_port and user-agent=anylog and log=false and topic=(
    name=performance_data and
    dbms="bring [dbms]" and
    table="bring [table]" and
    column.timestamp.timestamp="bring [timestamp]" and
    column.value=(value="bring [value]" and type=float)
)>

# Ping / PercentageCPU
<run mqtt client where broker=rest and port=!anylog_rest_port and user-agent=anylog and log=false and topic=(
    name=lsl_data and
    dbms="bring [dbms]" and
    table="bring [table]" and
    column.timestamp.timestamp="bring [timestamp]" and
    column.device_name=(value="bring [device_name]" and type=str ) and
    column.parentelement=(value="bring [parentelement]" and type=str ) and
    column.webid=(value="bring [webid]" and type=str) and
    column.value=(value="bring [value]" and type=float)
)>

# OPCUA
<run mqtt client where broker=rest and port=!anylog_rest_port and user-agent=anylog log=false and topic=(
    name=opcua_data and
    dbms="bring [dbms]" and
    table="bring [table]" and
    column.timestamp.timestamp="bring [timestamp]" and
    column.fic1_pv=(type=float and value="bring [fic1_pv]") and
    column.fic1_mv=(type=float and value="bring [fic1_mv]") and
    column.fic1_sv=(type=float and value="bring [fic1_sv]") and
    column.lic1_pv=(type=float and value="bring [lic1_pv]") and
    column.lic1_mv=(type=float and value="bring [lic1_mv]") and
    column.lic1_sv=(type=float and value="bring [lic1_sv]") and
    column.fic2_pv=(type=float and value="bring [fic2_pv]") and
    column.fic2_mv=(type=float and value="bring [fic2_mv]") and
    column.fic2_sv=(type=float and value="bring [fic2_sv]") and
    column.lic2_pv=(type=float and value="bring [lic2_pv]") and
    column.lic2_mv=(type=float and value="bring [lic2_mv]") and
    column.lic2_sv=(type=float and value="bring [lic2_sv]") and
    column.fic3_pv=(type=float and value="bring [fic3_pv]") and
    column.fic3_mv=(type=float and value="bring [fic3_mv]") and
    column.fic3_sv=(type=float and value="bring [fic3_sv]") and
    column.lic3_pv=(type=float and value="bring [lic3_pv]") and
    column.lic3_mv=(type=float and value="bring [lic3_mv]") and
    column.lic3_sv=(type=float and value="bring [lic3_sv]") and
    column.fic4_pv=(type=float and value="bring [fic4_pv]") and
    column.fic4_mv=(type=float and value="bring [fic4_mv]") and
    column.fic4_sv=(type=float and value="bring [fic4_sv]") and
    column.lic4_pv=(type=float and value="bring [lic4_pv]") and
    column.lic4_mv=(type=float and value="bring [lic4_mv]") and
    column.lic4_sv=(type=float and value="bring [lic4_sv]") and
    column.fic5_pv=(type=float and value="bring [fic5_pv]") and
    column.fic5_mv=(type=float and value="bring [fic5_mv]") and
    column.fic5_sv=(type=float and value="bring [fic5_sv]") and
    column.lic5_pv=(type=float and value="bring [lic5_pv]") and
    column.lic5_mv=(type=float and value="bring [lic5_mv]") and
    column.lic5_sv=(type=float and value="bring [lic5_sv]")
)>

# Power - this combines 2 types of data sets into a single run MQTT client
<run mqtt client where broker=rest and port=!anylog_rest_port and user-agent=anylog and log=false and topic=(
    name=power_data and
    dbms="bring [dbms]" and
    table="bring [table]" and
    column.timestamp.timestamp="bring [timestamp]" and
    column.location=(type=str and value="bring [location]") and
    column.value=(type=float and value="bring [value]" and optional=true) and
    column.phasor=(type=str and value="bring [phasor]" and optional=true) and
    column.frequency=(type=float and value="bring [frequency]" and optional=true) and
    column.dfreq=(type=float and value="bring [dfreq]" and optional=true) and
    column.analog=(type=float and value="bring [analog]" and optional=true)
)>