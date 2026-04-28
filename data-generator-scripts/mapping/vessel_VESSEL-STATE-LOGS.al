#--------------------------------------------------------------------------------------------------------------------#
# Mapping policy for vessel data
#--------------------------------------------------------------------------------------------------------------------#
# process !local_scripts/data-generator/mapping/vessel_VESSEL-STATE-LOGS.al
on error ignore

set create_policy = false

:check-policy:
is_policy = blockchain get (mapping, transform) where id = VESSEL-STATE-LOGS
if not !is_policy and !create_policy == false then goto declare-policy
else if !is_policy then goto end-script
else if not !is_policy and !create_policy == true then goto declare-policy-error


:declare-policy:
<new_policy = {
    "mapping" : {
        "id" : "VESSEL-STATE-LOGS",
        "dbms" : !default_dbms,
        "table" : "vessel_state_logs",
        "readings" : "",
        "schema" : {
            "timestamp" : {
                "type" : "timestamp",
                "default" : "now()",
                "bring" : "[timestamp]"
            },
            "boat_name" : {
                "type" : "string",
                "bring" : "[boat_name]",
                "default" : ""
            },
            "side" : {
                "type" : "string",
                "bring" : "[side]",
                "default" : ""
            },
            "ip_index" : {
                "type" : "int",
                "bring" : "[ip_index]",
                "default" : Null
            },
            "motor_id" : {
                "type" : "int",
                "bring" : "[motor_id]",
                "default" : Null
            },
            "__start__" : {"script" : ["set VESSEL-STATE-LOGS_counter = 0"]
            },
            "hmiYear" : {
                "type" : "int",
                "bring" : "[hmiYear]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [hmiYear] then VESSEL-STATE-LOGS_counter = incr !VESSEL-STATE-LOGS_counter"]
            },
            "hmiMonth" : {
                "type" : "int",
                "bring" : "[hmiMonth]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [hmiMonth] then VESSEL-STATE-LOGS_counter = incr !VESSEL-STATE-LOGS_counter"]
            },
            "hmiDay" : {
                "type" : "int",
                "bring" : "[hmiDay]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [hmiDay] then VESSEL-STATE-LOGS_counter = incr !VESSEL-STATE-LOGS_counter"]
            },
            "hmiHour" : {
                "type" : "int",
                "bring" : "[hmiHour]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [hmiHour] then VESSEL-STATE-LOGS_counter = incr !VESSEL-STATE-LOGS_counter"]
            },
            "hmiMinute" : {
                "type" : "int",
                "bring" : "[hmiMinute]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [hmiMinute] then VESSEL-STATE-LOGS_counter = incr !VESSEL-STATE-LOGS_counter"]
            },
            "hmiSecond" : {
                "type" : "int",
                "bring" : "[hmiSecond]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [hmiSecond] then VESSEL-STATE-LOGS_counter = incr !VESSEL-STATE-LOGS_counter"]
            },
            "systemState" : {
                "type" : "string",
                "bring" : "[systemState]",
                "default" : "",
                "optional" : True,
                "script" : ["if [systemState] then VESSEL-STATE-LOGS_counter = incr !VESSEL-STATE-LOGS_counter"]
            },
            "vesselState" : {
                "type" : "string",
                "bring" : "[vesselState]",
                "default" : "",
                "optional" : True,
                "script" : ["if [vesselState] then VESSEL-STATE-LOGS_counter = incr !VESSEL-STATE-LOGS_counter"]
            },
            "selectSystemMode" : {
                "type" : "string",
                "bring" : "[selectSystemMode]",
                "default" : "",
                "optional" : True,
                "script" : ["if [selectSystemMode] then VESSEL-STATE-LOGS_counter = incr !VESSEL-STATE-LOGS_counter"]
            },
            "gCommand" : {
                "type" : "string",
                "bring" : "[gCommand]",
                "default" : "",
                "optional" : True,
                "script" : ["if [gCommand] then VESSEL-STATE-LOGS_counter = incr !VESSEL-STATE-LOGS_counter"]
            },
            "gCommandState" : {
                "type" : "string",
                "bring" : "[gCommandState]",
                "default" : "",
                "optional" : True,
                "script" : ["if [gCommandState] then VESSEL-STATE-LOGS_counter = incr !VESSEL-STATE-LOGS_counter"]
            },
            "portDriveState" : {
                "type" : "string",
                "bring" : "[portDriveState]",
                "default" : "",
                "optional" : True,
                "script" : ["if [portDriveState] then VESSEL-STATE-LOGS_counter = incr !VESSEL-STATE-LOGS_counter"]
            },
            "stbdDriveState" : {
                "type" : "string",
                "bring" : "[stbdDriveState]",
                "default" : "",
                "optional" : True,
                "script" : ["if [stbdDriveState] then VESSEL-STATE-LOGS_counter = incr !VESSEL-STATE-LOGS_counter"]
            },
            "portBatteryConnectionState" : {
                "type" : "string",
                "bring" : "[portBatteryConnectionState]",
                "default" : "",
                "optional" : True,
                "script" : ["if [portBatteryConnectionState] then VESSEL-STATE-LOGS_counter = incr !VESSEL-STATE-LOGS_counter"]
            },
            "stbdBatteryConnectionState" : {
                "type" : "string",
                "bring" : "[stbdBatteryConnectionState]",
                "default" : "",
                "optional" : True,
                "script" : ["if [stbdBatteryConnectionState] then VESSEL-STATE-LOGS_counter = incr !VESSEL-STATE-LOGS_counter"]
            },
            "portThrottleGearState" : {
                "type" : "string",
                "bring" : "[portThrottleGearState]",
                "default" : "",
                "optional" : True,
                "script" : ["if [portThrottleGearState] then VESSEL-STATE-LOGS_counter = incr !VESSEL-STATE-LOGS_counter"]
            },
            "stbdThrottleGearState" : {
                "type" : "string",
                "bring" : "[stbdThrottleGearState]",
                "default" : "",
                "optional" : True,
                "script" : ["if [stbdThrottleGearState] then VESSEL-STATE-LOGS_counter = incr !VESSEL-STATE-LOGS_counter"]
            },
            "recoveryState" : {
                "type" : "string",
                "bring" : "[recoveryState]",
                "default" : "",
                "optional" : True,
                "script" : ["if [recoveryState] then VESSEL-STATE-LOGS_counter = incr !VESSEL-STATE-LOGS_counter"]
            },
            "serverCpuLoad" : {
                "type" : "float",
                "bring" : "[serverCpuLoad]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [serverCpuLoad] then VESSEL-STATE-LOGS_counter = incr !VESSEL-STATE-LOGS_counter"]
            },
            "serverMemoryUsage" : {
                "type" : "int",
                "bring" : "[serverMemoryUsage]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [serverMemoryUsage] then VESSEL-STATE-LOGS_counter = incr !VESSEL-STATE-LOGS_counter"]
            },
            "serverSoftwareVersion" : {
                "type" : "int",
                "bring" : "[serverSoftwareVersion]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [serverSoftwareVersion] then VESSEL-STATE-LOGS_counter = incr !VESSEL-STATE-LOGS_counter"]
            },
            "serverCompilationTime" : {
                "type" : "int",
                "bring" : "[serverCompilationTime]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [serverCompilationTime] then VESSEL-STATE-LOGS_counter = incr !VESSEL-STATE-LOGS_counter"]
            },
            "updateRateMs" : {
                "type" : "int",
                "bring" : "[updateRateMs]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [updateRateMs] then VESSEL-STATE-LOGS_counter = incr !VESSEL-STATE-LOGS_counter"]
            },
            "scuConnectionState" : {
                "type" : "string",
                "bring" : "[scuConnectionState]",
                "default" : "",
                "optional" : True,
                "script" : ["if [scuConnectionState] then VESSEL-STATE-LOGS_counter = incr !VESSEL-STATE-LOGS_counter"]
            },
            "boxLinkEnable" : {
                "type" : "int",
                "bring" : "[boxLinkEnable]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [boxLinkEnable] then VESSEL-STATE-LOGS_counter = incr !VESSEL-STATE-LOGS_counter"]
            },
            "nightModeActive" : {
                "type" : "int",
                "bring" : "[nightModeActive]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [nightModeActive] then VESSEL-STATE-LOGS_counter = incr !VESSEL-STATE-LOGS_counter"]
            },
            "displayEnable" : {
                "type" : "int",
                "bring" : "[displayEnable]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [displayEnable] then VESSEL-STATE-LOGS_counter = incr !VESSEL-STATE-LOGS_counter"]
            },
            "__end__" : {"script" : ["if !VESSEL-STATE-LOGS_counter == 0 then streaming data ignore event"]}
        }
   }
}>

:publish-policy:
process !local_scripts/node-deployment/policies/publish_policy.al
if not !error_code.int then
do set create_policy = true
goto check-policy

if !error_code == 1 then goto sign-policy-error
else if !error_code == 2 then goto prepare-policy-error
else if !error_code == 3 then goto declare-policy-error

:end-script:
end script

:terminate-scripts:
exit scripts

:sign-policy-error:
print "Failed to sign mapping policy"
goto terminate-scripts

:prepare-policy-error:
print "Failed to prepare mapping policy for publishing on blockchain"
goto terminate-scripts

:declare-policy-error:
print "Failed to declare mapping policy on blockchain"
goto terminate-scripts
