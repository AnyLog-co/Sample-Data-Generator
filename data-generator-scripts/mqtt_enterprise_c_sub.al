#----------------------------------------------------------------------------------------------------------------------
# The following provides an example for data coming in from Topic - Enterprise_C/#
# unlike the other examples, "Enterprise C" is dynamic which means it automatically creates a UNS structure
# based on the data flowing in and then inserts it into AnyLog.
#
# Data is stored in timestamp / value logic with the sensor/device acting as the table name
#
# The following example uses dynamic against topic = Enterprise C/sub/#
#
# :sample UNS:
# {"uns" : {
#   "name" : "sic_250_002_sp_eu_1",
#   "namespace" : "enterprise_c/sub/sic_250_002_sp_eu_1",
#   "source_node" : "anylog-standalone-operator@192.168.65.3:32148",
#   "dbms" : "mydb",
#   "table" : "sic_250_002_sp_eu_1_1",
#   "parent" : "4cd16d1dc635952a3c51b8a3050eb112",
#   "id" : "4ebd336a3278f19bdc6fa399129cfa70",
#   "date" : "2026-04-06T01:45:30.173110Z",
#   "ledger" : "local"
# }}
#----------------------------------------------------------------------------------------------------------------------
# process !local_scripts/data-generator/mqtt_enterprise_c_sub.al

:msg-client:
on error goto msg-client-error
<run msg client where
    broker=172.104.228.251 and port=1883 and
    user=anyloguser and password=mqtt4AnyLog! and
    master_node = !ledger_conn and log=false and
    topic=(
        name=Enterprise C/sub/# and
        dbms = !default_dbms and
        dynamic = true
    )>

:end-script:
end script

:msg-client-error:
echo "Failed to declare msg client"
goto end-script
