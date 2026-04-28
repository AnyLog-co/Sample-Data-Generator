#--------------------------------------------------------------------------------------------------------------#
# Hardcoded call to the data generator for random data
#
# :Sample Data (published):
# {"timestamp": "2026-04-05T05:23:49.997386", "value": 0.18598355032073355, "dbms": "mydb", "table": "rand_data"}
#--------------------------------------------------------------------------------------------------------------#
# process !local_scripts/data-generator/rand_data.al

on error ignore

<run msg client where
    broker=172.104.228.251 and port=1883 and
    user=anyloguser and password=mqtt4AnyLog! and
    log=false and topic=(
        name=anylog-demo and
        dbms=!default_dbms and
        table = "bring [table]" and
        column.timestamp.timestamp = "bring [timestamp]" and
        column.value = (type=float and value="bring [value]")
    )>

get msg client

:end-script:
end script